import json
from google.cloud import storage
from google.oauth2 import service_account

class StorageManager:
    """
    Utility for saving and loading data to and from Google Cloud Storage.
    """

    def __init__(self, bucket_name):
        """
        Initialize the StorageManager with a bucket name and hardcoded service account credentials.
        :param bucket_name: Name of the Google Cloud Storage bucket.
        """
        # Hardcoded path to the service account JSON key file
        credentials_path = "config/service-account.json"
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = storage.Client(credentials=credentials)
        self.bucket = self.client.bucket(bucket_name)

    def save_json(self, data, filename):
        """
        Saves a Python object as a JSON file in the specified Google Cloud Storage bucket.
        """
        blob = self.bucket.blob(filename)
        blob.upload_from_string(json.dumps(data, indent=2), content_type='application/json')
        print(f"Saved data to {filename} in bucket {self.bucket.name}")

    def load_json(self, filename):
        """
        Loads a JSON file from the specified Google Cloud Storage bucket and returns the data.
        """
        blob = self.bucket.blob(filename)
        if not blob.exists():
            raise FileNotFoundError(f"File {filename} does not exist in bucket {self.bucket.name}")
        data = blob.download_as_text()
        return json.loads(data)
