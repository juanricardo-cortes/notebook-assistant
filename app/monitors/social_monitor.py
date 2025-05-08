from typing import List
import json
from abstractions.base_scraper import SocialScraper

class SocialMonitor:
    def __init__(self, scraper: SocialScraper, profile_urls: List[str]):
        self.scraper = scraper
        self.profile_urls = profile_urls
    
    def execute_monitoring(self):
        processed_data = []
        for url in self.profile_urls:
            try:
                profile_handle = self._extract_handle(url)
                print(f"Monitoring {profile_handle}...")
                data = self.scraper.scrape_profile(url)
                if data:
                    self.data = data
                    self.filename = self.scraper.save_content(profile_handle, data, self.scraper.output_folder.split('/')[-2])
                    self.upload_to_gcs("bhtech")  # Replace with your GCS bucket name
                    processed_data.append(f"C:/pinokio/api/notebook-assistant/app/{self.filename}")  # Append data as a JSON string
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
        return processed_data
                
    def upload_to_gcs(self, bucket_name: str):
        from utils.storage_manager import StorageManager
        storage_manager = StorageManager(bucket_name)
        print(f"Uploading {self.filename} to GCS bucket {bucket_name}...")
        try:
            storage_manager.save_json(self.data, self.filename)
            print(f"Uploaded {self.filename} to GCS bucket {bucket_name}.")
        except Exception as e:
            print(f"Error uploading to GCS: {str(e)}")

    def _extract_handle(self, url: str) -> str:
        return url.split('/')[-1]

