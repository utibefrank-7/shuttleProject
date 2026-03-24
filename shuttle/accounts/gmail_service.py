# gmail_service.py
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

GMAIL_CLIENT_ID = os.environ.get("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = os.environ.get("GMAIL_CLIENT_SECRET")
GMAIL_REFRESH_TOKEN = os.environ.get("GMAIL_REFRESH_TOKEN")
GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")

creds = Credentials(
    None,
    refresh_token=GMAIL_REFRESH_TOKEN,
    client_id=GMAIL_CLIENT_ID,
    client_secret=GMAIL_CLIENT_SECRET,
    token_uri="https://oauth2.googleapis.com/token"
)

service = build('gmail', 'v1', credentials=creds)

def send_gmail(to_email, subject, body):
    from email.mime.text import MIMEText
    import base64

    message = MIMEText(body)
    message['to'] = to_email
    message['from'] = GMAIL_EMAIL
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={'raw': raw_message}).execute()