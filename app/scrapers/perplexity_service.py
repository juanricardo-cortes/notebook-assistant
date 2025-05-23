from datetime import datetime, timedelta
import time
from abstractions.base_scraper import SocialScraper
import requests

class PerplexityService(SocialScraper):
    def __init__(self, output_folder='output/perplexity', config=None):
        super().__init__(output_folder)
        self.config = config
        print("Starting PerplexityService")

    def scrape_profile(self, prompt: str) -> list:
        url = "https://api.brightdata.com/datasets/v3/trigger"
        headers = {
            "Authorization": f"Bearer {self.config['brightdata_key']}",
            "Content-Type": "application/json",
        }
        params = {
            "dataset_id": "gd_m7dhdot1vw9a7gc1n",
            "include_errors": "true",
        }
        data = [
            {"url":"https://www.perplexity.ai","prompt": f"{prompt}","country":"US"},
        ]

        response = requests.post(url, headers=headers, params=params, json=data)

        SNAPSHOT_ID = response.json().get('snapshot_id')
        print('Snapshot ID:', SNAPSHOT_ID)

        headers = {
            'Authorization': f'Bearer {self.config["brightdata_key"]}',
            'Content-Type': 'application/json'
        }

        url = f"https://api.brightdata.com/datasets/v3/snapshot/{SNAPSHOT_ID}"
        params = {
            "format": "json",
        }

        returnresponse = None
        while True:
            response = requests.get(url, headers=headers, params=params)
            print('Checking status...')
            print('Response:', response)
            if response.status_code == 202:
                time.sleep(30)
                continue
            elif response.status_code == 200:
                returnresponse = response.json()
                break
            else:
                print('Error:', response.status_code, response.text)
                time.sleep(30)
                break            
        return returnresponse