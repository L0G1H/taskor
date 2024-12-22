import argparse
import json
import os
import pyperclip
from rich.console import Console
from rich.markdown import Markdown
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from taskor.utils.file_extractor import extract_text_from_file
from taskor.utils import get_file_paths
from taskor.utils.assistant_api import get_completion


RESOURCES_PATH = Path(__file__).parent.parent / "resources"
RESPONSES_PATH = RESOURCES_PATH / "responses.json"
SYSTEM_PROMPT_PATH = RESOURCES_PATH / "system_prompt.txt"
DEFAULT_MODEL_PATH = RESOURCES_PATH / "default_model.txt"

console = Console()

with open(DEFAULT_MODEL_PATH, encoding="utf-8") as f:
    DEFAULT_MODEL = f.read()


def save_response(prompt: str, response: str) -> None:
    try:
        with open(RESPONSES_PATH, encoding="utf-8") as f:
            data = json.load(f)
        data.append({"nr": len(data) + 1, "prompt": prompt, "response": response})
        with open(RESPONSES_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except FileNotFoundError:
        console.print(f"Error: Cannot find responses file at {RESPONSES_PATH}", style="bold red")
    except json.JSONDecodeError:
        console.print("Error: Malformed JSON in responses file", style="bold red")
    except Exception as e:
        console.print(f"Error saving response: {str(e)}", style="bold red")


def get_response_str(prompt: str) -> str:
    try:
        with open(RESPONSES_PATH, encoding="utf-8") as f:
            data = json.load(f)

        if len(data) == 0:
            console.print("Responses file is empty", style="bold red")
            return ""

        if not prompt:
            return data[-1]["response"]

        try:
            response_nr = int(prompt)
            if not (0 < response_nr <= len(data)):
                console.print("Given response nr is out of bounds", style="bold red")
                return ""
            return data[response_nr - 1]["response"]
        except ValueError:
            console.print("Given response nr is out of bounds", style="bold red")
            return ""

    except FileNotFoundError:
        console.print(f"Error: Cannot find responses file at {RESPONSES_PATH}", style="bold red")
        return ""
    except json.JSONDecodeError:
        console.print("Error: Malformed JSON in responses file", style="bold red")
        return ""
    except Exception as e:
        console.print(f"Error reading response: {str(e)}", style="bold red")
        return ""


def print_response(response_str: str) -> None:
    console.print(Markdown(response_str))


def search_responses(term: str) -> None:
    with open(RESPONSES_PATH, encoding="utf-8") as f:
        data = json.load(f)

    term = term.lower()
    matches = [
        item
        for item in data
        if term in (item["prompt"] + "\n" + item["response"]).lower()
    ]

    if matches:
        console.print(f"Found {len(matches)} match(es):", style="bold green")

        for match in matches:
            console.print(f"[Prompt nr] {match['nr']}. [Prompt]: {match['prompt']}")
            print_response(match["response"])
    else:
        console.print("No matches found", style="bold red")
    return


def get_clipboard_content():
    try:
        return pyperclip.paste()
    except Exception as e:
        console.print(f"Error accessing clipboard: {str(e)}", style="bold red")
    return ""


def main():
    parser = argparse.ArgumentParser(description="Taskor CLI Tool")

    parser.add_argument(
        "prompt",
        nargs="*",
        help="input",
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"model to use (default - {DEFAULT_MODEL})",
    )

    parser.add_argument(
        "-f",
        "--add-files",
        action="store_true",
        help="add external files",
    )

    parser.add_argument(
        "-i",
        "--incognito",
        action="store_true",
        help="not to save response",
    )

    parser.add_argument(
        "-p",
        "--paste",
        action="store_true",
        help="include current paste in the prompt",
    )

    parser.add_argument(
        "-n",
        "--no-prompt",
        action="store_true",
        help="pass request without a system prompt",
    )

    parser.add_argument(
        "-s",
        "--search",
        action="store_true",
        help="search for a specific term in saved responses",
    )

    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="copy a specific response (default - last)",
    )

    parser.add_argument(
        "--change-system-prompt",
        action="store_true",
        help="change system prompt",
    )

    parser.add_argument(
        "--change-default-model",
        action="store_true",
        help="change default model",
    )

    parser.add_argument(
        "--delete-history",
        action="store_true",
        help="delete request history",
    )

    args = parser.parse_args()
    prompt = " ".join(args.prompt)

    if args.delete_history:
        with open(RESPONSES_PATH, "w", encoding="utf-8") as f:
            f.write("[]")

        console.print("Successfully deleted history", style="bold green")
        return

    if args.change_system_prompt:
        if prompt or prompt == "":
            with open(SYSTEM_PROMPT_PATH, "w", encoding="utf-8") as f:
                f.write(prompt)

            console.print("Successfully changed system prompt", style="bold green")
        else:
            console.print("System prompt not given", style="bold red")
        return

    if args.change_default_model:
        if prompt:
            with open(DEFAULT_MODEL_PATH, "w", encoding="utf-8") as f:
                f.write(prompt)

            console.print("Successfully changed default model", style="bold green")
        else:
            console.print("Default model not given", style="bold red")
        return

    if args.search:
        if prompt:
            search_responses(prompt)
        else:
            console.print("Search prompt not given", style="bold red")
        return

    if args.copy:
        try:
            response = get_response_str(prompt)
            if response:
                pyperclip.copy(response)
                console.print("Response copied to clipboard", style="bold green")
        except Exception as e:
            console.print(f"Error copying to clipboard: {str(e)}", style="bold red")
        return

    if prompt:
        resources = ""
        is_system_prompt = not args.no_prompt

        if args.add_files:
            file_paths = get_file_paths()

            if not file_paths:
                console.print("No files selected", style="bold red")
                return

            for file_path in file_paths:
                resources += extract_text_from_file(file_path) + "\n\n"

        if args.paste:
            clipboard_content = get_clipboard_content()

            if clipboard_content:
                paste_str = "Clipboard\n" + clipboard_content + "\n\n"
                resources += paste_str

        response = get_completion(
            model=args.model,
            prompt=prompt,
            resources=resources,
            is_system_prompt=is_system_prompt,
            SYSTEM_PROMPT_PATH=SYSTEM_PROMPT_PATH)

        print_response(response)

        if not args.incognito:
            save_response(prompt, response)
        return

    console.print("Invalid syntax", style="bold red")
    return


if __name__ == "__main__":
    main()
