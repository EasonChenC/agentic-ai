"""
Example: request deletion when delete tool is NOT available.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import email_tools
from examples.common import run_agent


def main():
    tools = [
        email_tools.search_unread_from_sender,
        email_tools.list_unread_emails,
        email_tools.search_emails,
        email_tools.get_email,
        email_tools.mark_email_as_read,
        email_tools.send_email,
    ]

    run_agent("Delete emails from alice@work.com", tools=tools, max_turns=5)


if __name__ == "__main__":
    main()
