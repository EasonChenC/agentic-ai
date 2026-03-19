"""
Quick sanity checks for email_tools without LLM.
"""

import json
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import email_tools


def _print_json(label: str, payload) -> None:
    print(f"\n{label}")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main():
    load_dotenv()

    new_email = email_tools.send_email(
        "test@example.com",
        "Lunch plans",
        "Shall we meet at noon?",
    )
    _print_json("Sent email:", new_email)

    fetched = email_tools.get_email(new_email["id"])
    _print_json("Fetched email:", fetched)

    unread = email_tools.list_unread_emails()
    _print_json("Unread emails:", unread[:3])


if __name__ == "__main__":
    main()
