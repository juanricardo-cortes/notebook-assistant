from google.oauth2.service_account import Credentials # type: ignore

class CredentialsProvider:
    def __init__(self, config):
        self.config = config

    def get_credentials(self, email):
        return Credentials.from_service_account_file(
            'config/service-account.json',
            scopes=[
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/bigquery",
                'https://www.googleapis.com/auth/drive',
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.send",
                "https://www.googleapis.com/auth/gmail.compose",
                "https://www.googleapis.com/auth/gmail.modify"
            ],
            subject=email
        )