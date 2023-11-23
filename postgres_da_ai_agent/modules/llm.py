"""
Purpose:
    Interact with the UPDATED OpenAI API Supports 1.2.3+
    Provide supporting prompt engineering functions.
"""
"""
Purpose:
    Interact with the OpenAI API.
    Provide supporting prompt engineering functions.
"""

from dataclasses import dataclass
import json
import sys
from dotenv import load_dotenv
import os
from typing import Any, Dict, List, Callable
import openai
import tiktoken

# load .env file
load_dotenv()

assert os.environ.get("OPENAI_API_KEY")

# get openai api key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# ------------------ helpers ------------------


@dataclass
class TurboTool:
    name: str  # function name
    config: dict  # open ai config
    function: Callable  # function


def safe_get(data, dot_chained_keys):
    """
    {'a': {'b': [{'c': 1}]}}
    safe_get(data, 'a.b.0.c') -> 1
    """
    keys = dot_chained_keys.split(".")
    for key in keys:
        try:
            if isinstance(data, list):
                data = data[int(key)]
            else:
                data = data[key]
        except (KeyError, TypeError, IndexError):
            return None
    return data


def response_parser(response: Dict[str, Any]):
    return safe_get(response, "choices.0.message.content")


# ------------------ content generators ------------------


def prompt(
    prompt: str,
    model: str = "gpt-3.5-turbo-1106",
    instructions: str = "You are a helpful assistant.",
) -> str:
    """
    Generate a response from a prompt using the OpenAI API.
    """

    if not openai.api_key:
        sys.exit(
            """
ERORR: OpenAI API key not found. Please export your key to OPENAI_API_KEY
Example bash command:
    export OPENAI_API_KEY=<your openai apikey>
            """
        )

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": instructions,  # Added instructions as a system message
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response_parser(response.model_dump())

def add_cap_ref(
    prompt: str, prompt_suffix: str, cap_ref: str, cap_ref_content: str
) -> str:
    """
    Attaches a capitalized reference to the prompt.
    Example
        prompt = 'Refactor this code.'
        prompt_suffix = 'Make it more readable using this EXAMPLE.'
        cap_ref = 'EXAMPLE'
        cap_ref_content = 'def foo():\n    return True'
        returns 'Refactor this code. Make it more readable using this EXAMPLE.\n\nEXAMPLE\n\ndef foo():\n    return True'
    """

    new_prompt = f"""{prompt} {prompt_suffix}\n\n{cap_ref}\n\n{cap_ref_content}"""

    return new_prompt
