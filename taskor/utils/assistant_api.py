from __future__ import annotations
import os
from pathlib import Path
import dotenv
from anthropic import Anthropic
from openai import OpenAI


def get_completion(
    model: str,
    prompt: str,
    system_prompt_path: Path,
    resources: str = "",
    is_system_prompt: bool = True,
) -> str | tuple[None, str]:

    dotenv.load_dotenv()

    request_text = f"TASK: {prompt} \n\n"

    if resources:
        request_text += "RESOURCE FILES\n" + resources + "\n\n"

    if is_system_prompt:
        with Path.open(system_prompt_path, encoding="utf-8") as f:
            system_prompt = f.read().upper()

        if system_prompt:
            request_text += f"RULES: {system_prompt}"

    if "claude" in model:
        key = os.getenv("ANTHROPIC_API_KEY")

        if not key:
            return None, "environmental variable `ANTHROPIC_API_KEY` not set"

        try:
            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            completion = client.messages.create(
                model=model,
                messages=[{"role": "user", "content": request_text}],
                max_tokens=8192,
            )

            response = completion.content[0].text
        except Exception as e:
            return None, str(e)

    else:
        key = os.getenv("OPENAI_API_KEY")

        if not key:
            return None, "environmental variable `OPENAI_API_KEY` not set"

        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": request_text}],
            )

            response = completion.choices[0].message.content
        except Exception as e:
            return None, str(e)

    return response
