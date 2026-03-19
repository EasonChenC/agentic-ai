from dotenv import load_dotenv
import requests
import os

load_dotenv()

BASE_URL = os.getenv("M3_EMAIL_SERVER_API_URL")

def list_all_emails() -> dict:
    """
    Fetch all emails stored in the system, ordered from newest to oldest.

    Returns:
        dict: A dictionary with key 'emails' containing a list of all emails
        including read and unread, each represented as a dictionary with keys:
        - id
        - sender
        - recipient
        - subject
        - body
        - timestamp
        - read (boolean)
    """
    try:
        emails = requests.get(f"{BASE_URL}/emails").json()
        return {"emails": emails}
    except Exception as e:
        return {"error": str(e), "emails": []}


def list_unread_emails() -> dict:
    """
    Fetch all unread emails only.

    Returns:
        dict: A dictionary with key 'emails' containing a list of unread emails
        (where `read == False`), ordered from newest to oldest.
    """
    try:
        emails = requests.get(f"{BASE_URL}/emails/unread").json()
        return {"emails": emails}
    except Exception as e:
        return {"error": str(e), "emails": []}


def search_emails(query: str) -> dict:
    """
    Search emails containing the query in subject, body, or sender.
    You can search by keywords, phrases, or email addresses.

    Examples:
    - search_emails("report") - finds emails with "report" in subject/body/sender
    - search_emails("alice@work.com") - finds all emails from alice@work.com
    - search_emails("Happy Hour") - finds emails with "Happy Hour" in subject/body

    Args:
        query (str): A keyword, phrase, or email address to search for.

    Returns:
        dict: A dictionary with key 'results' containing a list of emails matching the query string.
    """
    try:
        results = requests.get(f"{BASE_URL}/emails/search", params={"q": query}).json()
        return {"results": results}
    except Exception as e:
        return {"error": str(e), "results": []}


def filter_emails(recipient: str = None, date_from: str = None, date_to: str = None) -> dict:
    """
    Filter emails based on recipient and/or a date range.

    Args:
        recipient (str): Email address to filter by (optional).
        date_from (str): Start date in 'YYYY-MM-DD' format (optional).
        date_to (str): End date in 'YYYY-MM-DD' format (optional).

    Returns:
        dict: A dictionary with key 'emails' containing a list of emails matching the given filters.
    """
    try:
        params = {}
        if recipient:
            params["recipient"] = recipient
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to

        emails = requests.get(f"{BASE_URL}/emails/filter", params=params).json()
        return {"emails": emails}
    except Exception as e:
        return {"error": str(e), "emails": []}


def get_email(email_id: int) -> dict:
    """
    Retrieve a specific email by its ID.

    Args:
        email_id (int): The unique ID of the email to fetch.

    Returns:
        dict: A single email record if found, else raises HTTP 404.
    """
    return requests.get(f"{BASE_URL}/emails/{email_id}").json()


def mark_email_as_read(email_id: int) -> dict:
    """
    Mark a specific email as read.

    Args:
        email_id (int): The ID of the email to mark as read.

    Returns:
        dict: The updated email record with `read: true`.
    """
    return requests.patch(f"{BASE_URL}/emails/{email_id}/read").json()


def mark_email_as_unread(email_id: int) -> dict:
    """
    Mark a specific email as unread.

    Args:
        email_id (int): The ID of the email to mark as unread.

    Returns:
        dict: The updated email record with `read: false`.
    """
    return requests.patch(f"{BASE_URL}/emails/{email_id}/unread").json()


def send_email(recipient: str, subject: str, body: str) -> dict:
    """
    Send an email (simulated). The sender is set automatically by the server.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The message body content.

    Returns:
        dict: The created email record.
    """
    payload = {
        "recipient": recipient,
        "subject": subject,
        "body": body
    }
    return requests.post(f"{BASE_URL}/send", json=payload).json()


def delete_email(email_id: int) -> dict:
    """
    Delete an email by its ID. This permanently removes the email from the system.

    Args:
        email_id (int): The ID of the email to delete.

    Returns:
        dict: A confirmation message: {"message": "Email deleted", "success": true}
    """
    try:
        response = requests.delete(f"{BASE_URL}/emails/{email_id}")
        response.raise_for_status()
        result = response.json()
        result["success"] = True
        return result
    except Exception as e:
        return {"error": str(e), "success": False, "message": "Failed to delete email"}


def search_unread_from_sender(sender: str) -> dict:
    """
    Return all unread emails from a specific sender (case-insensitive match).

    Args:
        sender (str): The email address of the sender to search for.

    Returns:
        dict: A dictionary with key 'emails' containing a list of unread emails
        where the sender matches the given address.
    """
    try:
        unread_result = list_unread_emails()
        if "error" in unread_result:
            return unread_result

        unread = unread_result.get("emails", [])
        filtered = [e for e in unread if e['sender'].lower() == sender.lower()]
        return {"emails": filtered}
    except Exception as e:
        return {"error": str(e), "emails": []}


# ========================================
# Tool Registry
# ========================================

ALL_TOOLS = [
    list_all_emails,
    list_unread_emails,
    search_emails,
    filter_emails,
    get_email,
    mark_email_as_read,
    mark_email_as_unread,
    send_email,
    delete_email,
    search_unread_from_sender,
]
