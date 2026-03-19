"""
Email Assistant Agent using AISuite + Google Gemini via API key.
"""

import os
from dotenv import load_dotenv

import aisuite as ai

from email_tools import ALL_TOOLS
from display_functions import pretty_print_chat_completion


SYSTEM_PROMPT = (
    "You are an email assistant. Use tools to read, search, filter, and manage emails. "
    "Ask for missing details when needed. Keep responses concise."
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


def run_email_agent(user_prompt: str, model: str = "google:gemini-2.5-flash-lite", max_turns: int = 8):
    client = ai.Client()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=ALL_TOOLS,
        max_turns=max_turns,
    )

    pretty_print_chat_completion(response)
    return response


def main():
    load_dotenv()
    _apply_proxy_settings()

    prompt = (
        "Check unread emails, summarize any urgent items in bullets, "
        "and mark the emails you used as read."
    )
    response = run_email_agent(prompt)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
