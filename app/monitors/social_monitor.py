from typing import List
import json
from abstractions.base_scraper import SocialScraper
from concurrent.futures import ThreadPoolExecutor

class SocialMonitor:
    def __init__(self, scraper: SocialScraper, profile_urls: List[str], config):
        self.scraper = scraper
        self.profile_urls = profile_urls
        self.config = config

    def execute_monitoring(self):
        # Initialize lists for each category
        processed_data1, important_links1, generated_titles1, generated_summaries1 = [], [], [], []
        processed_data2, important_links2, generated_titles2, generated_summaries2 = [], [], [], []
        processed_data3, important_links3, generated_titles3, generated_summaries3 = [], [], [], []
        processed_data4, important_links4, generated_titles4, generated_summaries4 = [], [], [], []

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
                    def check_and_process(valuation_key, processed_data, generated_titles, important_links, generated_summaries):
                        data_checked = self.scraper.check_content(content=data, config=self.config, valuation=self.config[valuation_key])
                        if len(data_checked) > 0:
                            print(f"Valuation: Content is relevant for {profile_handle}.")
                            filename = self.scraper.save_content(profile_handle, data_checked, self.scraper.output_folder.split('/')[-2])
                            self.upload_to_gcs(data=data_checked, filename = filename, bucket_name="bhtech")  # Replace with your GCS bucket name
                            processed_data.append(f"C:/pinokio/api/notebook-assistant/app/{filename}")
                            # generated_titles.append(self.scraper.generate_title(data_checked, config=self.config))
                            # important_links.append(self.scraper.extract_important_links(data_checked, config=self.config))
                            generated_summaries.append(self.scraper.generate_summary(data_checked, config=self.config))
                        else:
                            print(f"Valuation: Content is not relevant for {profile_handle}.")

                    with ThreadPoolExecutor(max_workers=4) as executor:
                        futures = [
                            executor.submit(check_and_process, "new_ai_tools_prompt", processed_data1, generated_titles1, important_links1, generated_summaries1),
                            executor.submit(check_and_process, "new_ai_updates_and_improvements_prompt", processed_data2, generated_titles2, important_links2, generated_summaries2),
                            executor.submit(check_and_process, "new_ai_business_innovations_and_applications_prompt", processed_data3, generated_titles3, important_links3, generated_summaries3),
                            executor.submit(check_and_process, "new_ai_discussions_and_trends_prompt", processed_data4, generated_titles4, important_links4, generated_summaries4),
                        ]
                        for future in futures:
                            future.result()
                else:
                    print(f"No data found for {profile_handle}.")
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")

        return (
            processed_data1, processed_data2, processed_data3, processed_data4,
            generated_summaries1, generated_summaries2, generated_summaries3, generated_summaries4
        )
                
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

