from typing import List
import json
from abstractions.base_scraper import SocialScraper

class SocialMonitor:
    def __init__(self, scraper: SocialScraper, profile_urls: List[str], config):
        self.scraper = scraper
        self.profile_urls = profile_urls
        self.config = config

    def execute_monitoring(self):
        processed_data1 = []
        important_links1 = []
        generated_titles1 = []

        processed_data2 = []
        important_links2 = []
        generated_titles2 = []

        processed_data3 = []
        important_links3 = []
        generated_titles3 = []

        processed_data4 = []
        important_links4 = []
        generated_titles4 = []

        for url in self.profile_urls:
            try:
                profile_handle = self._extract_handle(url)
                print(f"Monitoring {profile_handle}...")
                data = self.scraper.scrape_profile(url)
                if data:
                    print(f"Scraped data for {profile_handle}")
                    #data1 = new ai tools
                    #data2 = new ai updates and improvements
                    #data3 = new ai business innovations and applications
                    #data4 = new ai discussions and debates

                    self.data1 = self.scraper.check_content(data, config=self.config, valuation=self.config["new_ai_tools_prompt"])
                    if self.data1.__len__() > 0:
                        print(f"Content is relevant for {profile_handle}.")
                        filename = self.scraper.save_content(profile_handle, self.data1, self.scraper.output_folder.split('/')[-2])
                        self.upload_to_gcs(data=self.data1, filename = filename, bucket_name="bhtech")  # Replace with your GCS bucket name
                        processed_data1.append(f"C:/pinokio/api/notebook-assistant/app/{filename}")  # Append data as a JSON string
                        generated_titles1.append(self.scraper.generate_title(self.data1, config=self.config))
                        important_links1.append(self.scraper.extract_important_links(self.data1, config=self.config))
                        print(f"Important links extracted: {important_links1}")
                    else:
                        print(f"Content is not relevant for {profile_handle}.")

                    self.data2 = self.scraper.check_content(data, config=self.config, valuation=self.config["new_ai_updates_and_improvements_prompt"])
                    if self.data2.__len__() > 0:
                        print(f"Content is relevant for {profile_handle}.")
                        filename = self.scraper.save_content(profile_handle, self.data2, self.scraper.output_folder.split('/')[-2])
                        self.upload_to_gcs(data=self.data2, filename = filename, bucket_name="bhtech")  # Replace with your GCS bucket name
                        processed_data2.append(f"C:/pinokio/api/notebook-assistant/app/{filename}")  # Append data as a JSON string
                        generated_titles2.append(self.scraper.generate_title(self.data2, config=self.config))
                        important_links2.append(self.scraper.extract_important_links(self.data2, config=self.config))
                        print(f"Important links extracted: {important_links2}")
                    else:
                        print(f"Content is not relevant for {profile_handle}.")

                    self.data3 = self.scraper.check_content(data, config=self.config, valuation=self.config["new_ai_business_innovations_and_applications_prompt"])
                    if self.data3.__len__() > 0:
                        print(f"Content is relevant for {profile_handle}.")
                        filename = self.scraper.save_content(profile_handle, self.data3, self.scraper.output_folder.split('/')[-2])
                        self.upload_to_gcs(data=self.data3, filename = filename, bucket_name="bhtech")  # Replace with your GCS bucket name
                        processed_data3.append(f"C:/pinokio/api/notebook-assistant/app/{filename}")  # Append data as a JSON string
                        generated_titles3.append(self.scraper.generate_title(self.data3, config=self.config))
                        important_links3.append(self.scraper.extract_important_links(self.data3, config=self.config))
                        print(f"Important links extracted: {important_links3}")
                    else:
                        print(f"Content is not relevant for {profile_handle}.")

                    self.data4 = self.scraper.check_content(data, config=self.config, valuation=self.config["new_ai_discussions_and_trends_prompt"])
                    if self.data4.__len__() > 0:
                        print(f"Content is relevant for {profile_handle}.")
                        filename = self.scraper.save_content(profile_handle, self.data4, self.scraper.output_folder.split('/')[-2])
                        self.upload_to_gcs(data=self.data4, filename = filename, bucket_name="bhtech")  # Replace with your GCS bucket name
                        processed_data4.append(f"C:/pinokio/api/notebook-assistant/app/{filename}")  # Append data as a JSON string
                        generated_titles4.append(self.scraper.generate_title(self.data4, config=self.config))
                        important_links4.append(self.scraper.extract_important_links(self.data4, config=self.config))
                        print(f"Important links extracted: {important_links4}")
                    else:
                        print(f"Content is not relevant for {profile_handle}.")
                else:
                    print(f"No data found for {profile_handle}.")
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")

        return (processed_data1, important_links1, generated_titles1, 
                processed_data2, important_links2, generated_titles2, 
                processed_data3, important_links3, generated_titles3, 
                processed_data4, important_links4, generated_titles4)
                
    def upload_to_gcs(self, data, filename, bucket_name: str):
        from utils.storage_manager import StorageManager
        storage_manager = StorageManager(bucket_name)
        print(f"Uploading {filename} to GCS bucket {bucket_name}...")
        try:
            storage_manager.save_json(data, filename)
            print(f"Uploaded {filename} to GCS bucket {bucket_name}.")
        except Exception as e:
            print(f"Error uploading to GCS: {str(e)}")

    def _extract_handle(self, url: str) -> str:
        return url.split('/')[-1]

