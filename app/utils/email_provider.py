import os
import requests
import random
import string
import json

class EmailProvider:
    """
    A class to interact with the Mail.tm API for temporary email account automation.
    """

    def __init__(self, base_url="https://api.mail.tm"):
        self.base_url = base_url
        self.token = None
        self.email = None
        self.password = None
        self.account_id = None

    def get_domains(self):
        """Fetch available domains from Mail.tm."""
        response = requests.get(f"{self.base_url}/domains")
        response.raise_for_status()
        data = response.json()
        return [d["domain"] for d in data["hydra:member"]]

    def generate_random_username(self, length=10):
        """Generate a random username."""
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_secure_password(self, length=12):
        """Generate a secure password with letters, digits, and punctuation."""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

    def create_account(self, address, password):
        """Create a new email account on Mail.tm."""
        data = {"address": address, "password": password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{self.base_url}/accounts", headers=headers, data=json.dumps(data)
        )
        if response.status_code == 201:
            account_data = response.json()
            self.email = address
            self.password = password
            self.account_id = account_data["id"]
            return account_data
        elif response.status_code == 422:
            raise Exception("Email already exists.")
        else:
            raise Exception(f"Failed to create account: {response.text}")

    def get_account_token(self):
        """Obtain a JWT token for the created account."""
        if not self.email or not self.password:
            raise Exception("Email and password must be set before getting a token.")
        data = {"address": self.email, "password": self.password}
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{self.base_url}/token", headers=headers, data=json.dumps(data)
        )
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["token"]
            return self.token
        else:
            raise Exception(f"Failed to get token: {response.text}")

    def create_email_with_credentials(self, password=None):
        """
        Create a new email account and return both email address and password.
        Args:
            password (str, optional): Custom password for the account.
        Returns:
            tuple: (email_address, password)
        """
        domains = self.get_domains()
        if not domains:
            raise Exception("No domains available.")

        domain = domains[0]
        username = self.generate_random_username()
        if not password:
            password = self.generate_secure_password(12)

        email_address = f"{username}@{domain}"
        self.create_account(email_address, password)
        self.get_account_token()

        # Save the generated email and password to a file
        output_dir = "output/emails"
        os.makedirs(output_dir, exist_ok=True)
        with open(f"{output_dir}/newemails.txt", "a") as file:
            file.write(f"{email_address}:{password}\n")
            
        return email_address, password

    def get_messages(self, page=1):
        """Retrieve messages from the inbox."""
        if not self.token:
            raise Exception("Token must be set before getting messages.")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(
            f"{self.base_url}/messages?page={page}", headers=headers
        )
        response.raise_for_status()
        data = response.json()
        return data.get("hydra:member", [])

    def get_message(self, message_id):
        """Retrieve a specific message by ID."""
        if not self.token:
            raise Exception("Token must be set before getting a message.")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(
            f"{self.base_url}/messages/{message_id}", headers=headers
        )
        response.raise_for_status()
        return response.json()

    def delete_message(self, message_id):
        """Delete a specific message by ID."""
        if not self.token:
            raise Exception("Token must be set before deleting a message.")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(
            f"{self.base_url}/messages/{message_id}", headers=headers
        )
        return response.status_code == 204

    def delete_account(self):
        """Delete the created account."""
        if not self.token or not self.account_id:
            raise Exception("Token and account ID must be set before deleting the account.")
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.delete(
            f"{self.base_url}/accounts/{self.account_id}", headers=headers
        )
        if response.status_code == 204:
            self.token = None
            self.email = None
            self.password = None
            self.account_id = None
            return True
        return False

    def dispose(self):
        """Cleanup method to delete the account."""
        if self.account_id:
            self.delete_account()

    @classmethod
    def generate_credentials(cls, password=None):
        """
        Class method to directly generate email/password credentials.
        Returns:
            tuple: (email, password)
        """
        instance = cls()
        return instance.create_email_with_credentials(password)

# Example usage:
if __name__ == "__main__":
    mail_api = EmailProvider()
    email, password = mail_api.create_email_with_credentials()
    print("Email:", email)
    print("Password:", password)
    # Use email and password as needed, e.g., for social media registration
    # mail_api.dispose()  # Cleanup when done
