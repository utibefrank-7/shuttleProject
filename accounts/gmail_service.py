import os
import json
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_gmail_credentials():
    token_json = os.environ.get("GOOGLE_TOKEN")

    if not token_json:
        raise Exception("GOOGLE_TOKEN not found in environment variables")

    creds = Credentials.from_authorized_user_info(
        json.loads(token_json)
    )

    return creds


def send_gmail(to_email, subject, message_text):
    creds = get_gmail_credentials()

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(message_text)
    message['to'] = to_email
    message['subject'] = subject

    # ✅ FIXED: use encode, not decode
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message_body = {'raw': raw}

    service.users().messages().send(
        userId='me',
        body=message_body
    ).execute()