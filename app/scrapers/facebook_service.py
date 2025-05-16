from datetime import datetime, timedelta
import time
from abstractions.base_scraper import SocialScraper
import requests

class FacebookService(SocialScraper):
    def __init__(self, output_folder='output/facebook', config=None):
        super().__init__(output_folder)
        self.config = config

    def scrape_profile(self, group_url: str) -> list:

        url = "https://api.brightdata.com/datasets/v3/trigger"
        headers = {
            "Authorization": f"Bearer {self.config['brightdata_key']}",
            "Content-Type": "application/json",
        }
        params = {
            "dataset_id": "gd_lz11l67o2cb3r0lkj3",
            "include_errors": "true",
        }
        yesterday = datetime.utcnow() - timedelta(days=1)
        start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_yesterday = yesterday.replace(hour=23, minute=59, second=0, microsecond=0)
        data = [
            {"url":f"{group_url}","start_date":f"{start_of_yesterday}","end_date":f"{end_of_yesterday}"},
        ]

        response = requests.post(url, headers=headers, params=params, json=data)
        print(response.json())

        response = requests.post(url, headers=headers, params=params, json=data)
        print(response.json())

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
                print('Response:', response.json())
                time.sleep(30)
                continue
            elif response.status_code == 200:
                print('Response:', response.json())
                returnresponse = response.json()
                break
            else:
                print('Error:', response.status_code, response.text)
                time.sleep(30)
                break            
        return returnresponse
