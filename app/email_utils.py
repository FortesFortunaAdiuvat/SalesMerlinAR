import imaplib
import email
from email.header import decode_header
from typing import List, Dict

import httpx


def fetch_imap_emails(host: str, username: str, password: str, folder: str = "INBOX", limit: int = 10) -> List[Dict[str, str]]:
    """Fetch latest email subject lines from an IMAP server."""
    with imaplib.IMAP4_SSL(host) as imap:
        imap.login(username, password)
        imap.select(folder)
        status, messages = imap.search(None, "ALL")
        if status != "OK":
            return []
        ids = messages[0].split()[-limit:]
        results = []
        for num in reversed(ids):
            _, data = imap.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            subject, encoding = decode_header(msg.get("Subject"))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")
            results.append({"subject": subject})
    return results


def fetch_mailhog_emails(base_url: str = "http://mailhog:8025", limit: int = 10) -> List[Dict[str, str]]:
    """Fetch email subjects from a MailHog server."""
    resp = httpx.get(f"{base_url}/api/v2/messages")
    resp.raise_for_status()
    items = resp.json().get("items", [])[:limit]
    return [
        {"subject": item["Content"]["Headers"].get("Subject", [""])[0]}
        for item in items
    ]
