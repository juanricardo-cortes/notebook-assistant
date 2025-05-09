import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GmailService:
    def __init__(self, credentials):
        """
        Initialize the GmailService using configuration settings.
        """
        self.credentials = credentials
        # Build Gmail API service
        self.service = build("gmail", "v1", credentials=self.credentials)

    def fetch_unread_emails(self):
        """
        Fetch unread emails from the Gmail account.

        :return: List of unread emails with 'from', 'subject', and 'body'.
        """
        results = self.service.users().messages().list(userId="me", q="is:unread").execute()
        messages = results.get("messages", [])

        emails = []
        for message in messages:
            msg = self.service.users().messages().get(userId="me", id=message["id"]).execute()
            payload = msg.get("payload", {})
            headers = payload.get("headers", [])

            # Extract the email body
            body_data = ""
            if payload.get("body", {}).get("data"):
                body_data = payload["body"]["data"]
            elif payload.get("parts"):
                for part in payload["parts"]:
                    if part.get("body", {}).get("data"):
                        body_data = part["body"]["data"]
                        break

            email_data = {
                "from": next((header["value"] for header in headers if header["name"] == "From"), None),
                "subject": next((header["value"] for header in headers if header["name"] == "Subject"), None),
                "body": base64.urlsafe_b64decode(body_data).decode("utf-8") if body_data else ""
            }
            emails.append(email_data)

        return emails

    def send_email(self, to, subject, body):
        """
        Send an email using the Gmail API.

        :param to: Recipient email address.
        :param subject: Subject of the email.
        :param body: Body of the email.
        """
        message = {
            "raw": base64.urlsafe_b64encode(
                f"From: me\nTo: {to}\nSubject: {subject}\n\n{body}".encode("utf-8")
            ).decode("utf-8")
        }
        self.service.users().messages().send(userId="me", body=message).execute()

    def save_draft(self, to, subject, body):
        """
        Save an email as a draft in Gmail.

        :param to: Recipient email address.
        :param subject: Subject of the email.
        :param body: Body of the email.
        """
        message = {
            "raw": base64.urlsafe_b64encode(
                f"To: {to}\nSubject: {subject}\n\n{body}".encode("utf-8")
            ).decode("utf-8")
        }

        self.service.users().drafts().create(
            userId="me",
            body={"message": message}
        ).execute()