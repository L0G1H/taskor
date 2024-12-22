import os
from anthropic import Anthropic
from openai import OpenAI
import dotenv
from pathlib import Path


def get_completion(model: str, prompt: str, SYSTEM_PROMPT_PATH: Path, resources: str = "",
                   is_system_prompt: bool = True) -> str:
    dotenv.load_dotenv()

    request_text = f"TASK: {prompt} \n\n"

    if resources:
        request_text += "RESOURCE FILES\n" + resources + "\n\n"

    if is_system_prompt:
        with open(SYSTEM_PROMPT_PATH, encoding="utf-8") as f:
            system_prompt = f.read().upper()

        if system_prompt:
            request_text += f"RULES: {system_prompt}"


    if "claude" in model:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        completion = client.messages.create(
            model=model,
            messages=[{
                "role": "user",
                "content": request_text
            }],
            max_tokens=8192
        )
        
        response = completion.content[0].text
        
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": request_text}],
        )

        response = completion.choices[0].message.content
    
    return response
