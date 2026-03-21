import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def send_gmail(to_email, subject, message_text):
    creds =Credentials.from_authorized_user_file('token.json')

    service =build('gmail', 'v1', credentials=creds)

    message =MIMEText(message_text)
    message['to']=to_email
    message['subject']=subject

    raw=base64.urlsafe_b64decode(message.as_bytes()).decode()
    message_body ={'raw':raw}

    service.users().messages().send(userId='me', body=message_body).execute()