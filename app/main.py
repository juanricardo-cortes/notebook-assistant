import sys
import json
import os
import time
from core.driver import AntiDetectDriver
from scrapers.youtube_service import YouTubeService
from scrapers.twitter_service import TwitterScraper
from scrapers.instagram_service import InstagramScraper
from scrapers.linkedin_service import LinkedInScraper
from scrapers.facebook_service import FacebookService
from scrapers.newsletter_service import NewsletterService
from monitors.social_monitor import SocialMonitor
from core.proxy_manager import FreeProxyManager
from core.rate_limiter import RateLimiter

from utils.drive_manager import GoogleDriveUploader
from utils.gmail_manager import GmailService
from utils.credentials_provider import CredentialsProvider
from utils.email_provider import EmailProvider
from features.notebook_default import NotebookDefault
from utils.openai_manager import OpenAIService

from utils.bigquery_manager import BigQueryManager


# Load configuration from the config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "config.json")
with open(CONFIG_PATH, "r") as config_file:
    CONFIG = json.load(config_file)

def main(args=None):
    if args is None:
        args = []
    else: 
        # Log the received arguments
        print(f"Received arguments: {args}")

        # start_proxy_rotation()        
        # start_email_provider()

        # test()
        start_monitoring()
        # start_bigquery()
    
    return

def start_monitoring():
    print("Starting monitoring...")
    #1 new_ai_tools
    #2 new_ai_updates_and_improvements
    #3 new_ai_business_innovations_and_applications
    #4 new_ai_discussions_and_trends

    all_files1 = [] 
    all_links1 = []
    all_titles1 = []

    all_files2 = []
    all_links2 = []
    all_titles2 = []

    all_files3 = []
    all_links3 = []
    all_titles3 = []

    all_files4 = []
    all_links4 = []
    all_titles4 = []

    (linkedin_data1, linkedin_links1, linkedin_titles1, 
    linkedin_data2, linkedin_links2, linkedin_titles2, 
    linkedin_data3, linkedin_links3, linkedin_titles3,
    linkedin_data4, linkedin_links4, linkedin_titles4) = monitor_linkedin_profiles()
    all_files1.extend(linkedin_data1)
    all_links1.extend(linkedin_links1)
    all_titles1.extend(linkedin_titles1)

    all_files2.extend(linkedin_data2)
    all_links2.extend(linkedin_links2)
    all_titles2.extend(linkedin_titles2)

    all_files3.extend(linkedin_data3)
    all_links3.extend(linkedin_links3)
    all_titles3.extend(linkedin_titles3)

    all_files4.extend(linkedin_data4)
    all_links4.extend(linkedin_links4)
    all_titles4.extend(linkedin_titles4)

    (instagram_data1, instagram_links1, instagram_titles1,
    instagram_data2, instagram_links2, instagram_titles2,
    instagram_data3, instagram_links3, instagram_titles3,
    instagram_data4, instagram_links4, instagram_titles4) = monitor_instagram_profiles()
    all_files1.extend(instagram_data1)
    all_links1.extend(instagram_links1)
    all_titles1.extend(instagram_titles1)

    all_files2.extend(instagram_data2)
    all_links2.extend(instagram_links2)
    all_titles2.extend(instagram_titles2)

    all_files3.extend(instagram_data3)
    all_links3.extend(instagram_links3)
    all_titles3.extend(instagram_titles3)

    all_files4.extend(instagram_data4)
    all_links4.extend(instagram_links4)
    all_titles4.extend(instagram_titles4)

    (newsletter_data1, newsletter_links1, newsletter_titles1,
    newsletter_data2, newsletter_links2, newsletter_titles2,
    newsletter_data3, newsletter_links3, newsletter_titles3,
    newsletter_data4, newsletter_links4, newsletter_titles4) = monitor_newsletters()
    all_files1.extend(newsletter_data1)
    all_links1.extend(newsletter_links1)
    all_titles1.extend(newsletter_titles1)

    all_files2.extend(newsletter_data2)
    all_links2.extend(newsletter_links2)
    all_titles2.extend(newsletter_titles2)

    all_files3.extend(newsletter_data3)
    all_links3.extend(newsletter_links3)
    all_titles3.extend(newsletter_titles3)

    all_files4.extend(newsletter_data4)
    all_links4.extend(newsletter_links4)
    all_titles4.extend(newsletter_titles4)

    (youtube_data1, youtube_links1, youtube_titles1,
    youtube_data2, youtube_links2, youtube_titles2,
    youtube_data3, youtube_links3, youtube_titles3,
    youtube_data4, youtube_links4, youtube_titles4) = monitor_youtube_channels()
    all_files1.extend(youtube_data1)
    all_links1.extend(youtube_links1)
    all_titles1.extend(youtube_titles1)

    all_files2.extend(youtube_data2)
    all_links2.extend(youtube_links2)
    all_titles2.extend(youtube_titles2)

    all_files3.extend(youtube_data3)
    all_links3.extend(youtube_links3)
    all_titles3.extend(youtube_titles3)

    all_files4.extend(youtube_data4)
    all_links4.extend(youtube_links4)
    all_titles4.extend(youtube_titles4)

    (twitter_data1, twitter_links1, twitter_titles1,
    twitter_data2, twitter_links2, twitter_titles2,
    twitter_data3, twitter_links3, twitter_titles3,
    twitter_data4, twitter_links4, twitter_titles4) = monitor_twitter_profiles()
    all_files1.extend(twitter_data1)
    all_links1.extend(twitter_links1)
    all_titles1.extend(twitter_titles1)

    all_files2.extend(twitter_data2)
    all_links2.extend(twitter_links2)
    all_titles2.extend(twitter_titles2)

    all_files3.extend(twitter_data3)
    all_links3.extend(twitter_links3)
    all_titles3.extend(twitter_titles3)

    all_files4.extend(twitter_data4)
    all_links4.extend(twitter_links4)
    all_titles4.extend(twitter_titles4)

    (facebook_data1, facebook_links1, facebook_titles1,
    facebook_data2, facebook_links2, facebook_titles2,
    facebook_data3, facebook_links3, facebook_titles3,
    facebook_data4, facebook_links4, facebook_titles4) = monitor_facebook_groups()
    all_files1.extend(facebook_data1)
    all_links1.extend(facebook_links1)
    all_titles1.extend(facebook_titles1)

    all_files2.extend(facebook_data2)
    all_links2.extend(facebook_links2)
    all_titles2.extend(facebook_titles2)

    all_files3.extend(facebook_data3)
    all_links3.extend(facebook_links3)
    all_titles3.extend(facebook_titles3)

    all_files4.extend(facebook_data4)
    all_links4.extend(facebook_links4)
    all_titles4.extend(facebook_titles4)

    # Process and upload for all_files1
    if not all_files1:
        print("No data to process for category 1. Stopping execution.")
    else:
        start_notebook_assistant(all_files1)
        print("Monitoring for category 1 completed.")
        start_google_drive(all_links1, all_titles1, subject="NEW TOOLS")
        print("Google Drive upload for category 1 completed.")

    # Process and upload for all_files2
    if not all_files2:
        print("No data to process for category 2. Stopping execution.")
    else:
        start_notebook_assistant(all_files2)
        print("Monitoring for category 2 completed.")
        start_google_drive(all_links2, all_titles2, subject="UPDATES AND IMPROVEMENTS")
        print("Google Drive upload for category 2 completed.")

    # Process and upload for all_files3
    if not all_files3:
        print("No data to process for category 3. Stopping execution.")
    else:
        start_notebook_assistant(all_files3)
        print("Monitoring for category 3 completed.")
        start_google_drive(all_links3, all_titles3, subject="BUSINESS INNOVATIONS")
        print("Google Drive upload for category 3 completed.")

    # Process and upload for all_files4
    if not all_files4:
        print("No data to process for category 4. Stopping execution.")
    else:
        start_notebook_assistant(all_files4)
        print("Monitoring for category 4 completed.")
        start_google_drive(all_links4, all_titles4, subject="DISCUSSIONS")
        print("Google Drive upload for category 4 completed.")

    

def monitor_newsletters():
    newsletter_scraper = NewsletterService(config=CONFIG)
    newsletter_urls = CONFIG["newsletter_urls"]
    monitor = SocialMonitor(newsletter_scraper, newsletter_urls, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_youtube_channels():
    api_key = CONFIG["youtube_api_key"]
    channel_urls = CONFIG["youtube_channels"]
    youtube_service = YouTubeService(api_key)
    monitor = SocialMonitor(youtube_service, channel_urls, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_twitter_profiles():
    driver = AntiDetectDriver().get_driver()
    twitter_scraper = TwitterScraper(driver)
    twitter_profiles = CONFIG["twitter_profiles"]
    monitor = SocialMonitor(twitter_scraper, twitter_profiles, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_instagram_profiles():
    instagram_scraper = InstagramScraper(config=CONFIG)
    instagram_profiles = CONFIG["instagram_profiles"]
    monitor = SocialMonitor(instagram_scraper, instagram_profiles, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_linkedin_profiles():
    linkedin_scraper = LinkedInScraper(config=CONFIG)
    linkedin_profiles = CONFIG["linkedin_profiles"]
    monitor = SocialMonitor(linkedin_scraper, linkedin_profiles, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_facebook_groups():
    facebook_scraper = FacebookService(config=CONFIG)
    facebook_groups = CONFIG["facebook_groups"]
    monitor = SocialMonitor(facebook_scraper, facebook_groups, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def start_proxy_rotation():
    proxy_manager = FreeProxyManager()
    all_proxies = proxy_manager.get_proxy_list()
    print(f"Found {len(all_proxies)} proxies")
    working_proxy = proxy_manager.get_random_proxy()
    print(f"Random working proxy: {working_proxy}")

def start_email_provider():
    mail_api = EmailProvider()
    for _ in range(3):
        email, password = mail_api.create_email_with_credentials()
        print("Generated Email:", email)
        print("Generated Password:", password)
        RateLimiter.random_delay()

def start_notebook_assistant(processed_data):
    driver = AntiDetectDriver().get_driver()
    notebook_assistant = NotebookDefault(driver=driver)
    notebook_assistant.generate_audio_podcast_from_profiles(processed_data)

def start_google_drive(all_links, all_titles, subject):
    time.sleep(10)  # Wait for the file to be ready
    
    titles_text = "\n".join(all_titles)
    openai_service = OpenAIService(config=CONFIG)
    instructions = CONFIG["title_prompt"]
    prompt = f"Content: {titles_text}"
    response = openai_service.generate_response(prompt, instructions)

    credentials_provider = CredentialsProvider(CONFIG)
    credentials = credentials_provider.get_credentials(CONFIG["drive_email"])
    uploader = GoogleDriveUploader(credentials=credentials)
    uploader.authenticate()
    file_metadata = uploader.upload_file(title=response, emails_to_share=CONFIG["emails_to_share"])

    RateLimiter.random_delay(5,10)
    links_text = "\n".join(all_links)
    openai_service = OpenAIService(config=CONFIG)
    instructions = CONFIG["summarize_prompt"]
    prompt = f"Content: {links_text}"
    response = openai_service.generate_response(prompt, instructions)

    body_with_links = f"{subject}: Daily podcast update has been uploaded to Google Drive. Link: {file_metadata['webViewLink']}\n\nAdditional Links:\n{response}"
    for email in CONFIG["emails_to_share"]:
        gmail_service = GmailService(credentials=credentials)
        gmail_service.send_email(
            to=email,
            subject=f'[{subject}]: Daily Ai Podcast Updates',
            body=body_with_links
        )

def start_bigquery():
    credentials_provider = CredentialsProvider(CONFIG)
    credentials = credentials_provider.get_credentials(CONFIG["bigquery_email"])
    project_id = CONFIG["project_id"]
    dataset_id = CONFIG["dataset_id"]
    
    bigquery_manager = BigQueryManager(project_id, dataset_id, credentials)
    print(f"BigQuery dataset {dataset_id} initialized successfully.")

def test():
    print("Testing...")

    import requests

    mapurl = "https://www.google.com/maps/place/SM+City+Marikina/@14.626017,121.0812158,17z/data=!3m1!4b1!4m6!3m5!1s0x3397b8261d0f20b5:0x45e3362dac0fc52a!8m2!3d14.6260118!4d121.0837907!16s%2Fm%2F043ln0g?entry=ttu&g_ep=EgoyMDI1MDUxMy4xIKXMDSoASAFQAw%3D%3D"

    url = "https://api.brightdata.com/datasets/v3/trigger"
    headers = {
        "Authorization": f"Bearer {CONFIG['brightdata_key']}",
        "Content-Type": "application/json",
    }
    params = {
        "dataset_id": "gd_luzfs1dn2oa0teb81",
        "include_errors": "true",
    }
    data = [
        {"url":f"{mapurl}","days_limit":18}
    ]

    response = requests.post(url, headers=headers, params=params, json=data)
    print(response.json())

    SNAPSHOT_ID = response.json().get('snapshot_id')
    print('Snapshot ID:', SNAPSHOT_ID)

    headers = {
        'Authorization': f'Bearer {CONFIG["brightdata_key"]}',
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


if __name__ == "__main__":
    main(sys.argv[1:])  