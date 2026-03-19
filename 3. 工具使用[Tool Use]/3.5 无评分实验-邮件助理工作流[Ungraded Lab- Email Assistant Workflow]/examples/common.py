"""
Shared helpers for email assistant examples.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import aisuite as ai

_PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from display_functions import pretty_print_chat_completion


SYSTEM_PROMPT = (
    "You are an email assistant. Use the available tools to read, search, filter, manage, and delete emails. "
    "When a task requires information you don't have (like an email ID), use the appropriate tools to find it first. "
    "For example, if asked to delete an email by subject, first search for it, then delete it using the ID. "
    "Important: When the user gives you a clear instruction (like 'Delete emails from X'), execute it directly. "
    "Do not ask for confirmation unless the instruction is ambiguous or could affect a large number of emails (>10). "
    "Be proactive and complete tasks without unnecessary questions. "
    "Keep responses concise."
)




def _apply_proxy_settings() -> None:
    http_proxy = os.getenv("HTTP_PROXY")
    https_proxy = os.getenv("HTTPS_PROXY")

    if http_proxy:
        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["http_proxy"] = http_proxy
    if https_proxy:
        os.environ["HTTPS_PROXY"] = https_proxy
        os.environ["https_proxy"] = https_proxy


def run_agent(user_prompt: str, tools: list, model: str = "google:gemini-2.5-flash-lite", max_turns: int = 6):
    load_dotenv()
    _apply_proxy_settings()
    client = ai.Client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        max_turns=max_turns,
    )

    pretty_print_chat_completion(response)
    print(response.choices[0].message.content)
    return response
