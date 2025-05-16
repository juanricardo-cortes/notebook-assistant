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

        test()
        # start_monitoring()
        # start_bigquery()
    
    return

def start_monitoring():
    print("Starting monitoring...")
    all_files = [] 
    all_links = []
    all_titles = []

    
    # youtube_data, youtube_links, youtube_titles = monitor_youtube_channels()
    # all_files.extend(youtube_data)
    # all_links.extend(youtube_links)
    # all_titles.extend(youtube_titles)

    # twitter_data, twitter_links, twitter_titles = monitor_twitter_profiles()
    # all_files.extend(twitter_data)
    # all_links.extend(twitter_links)
    # all_titles.extend(twitter_titles)

    newsletter_data, newsletter_links, newsletter_titles = monitor_newsletters()
    all_files.extend(newsletter_data)
    all_links.extend(newsletter_links)
    all_titles.extend(newsletter_titles)

    # instagram_data, instagram_links, instagram_titles = monitor_instagram_profiles()
    # all_files.extend(instagram_data)
    # all_links.extend(instagram_links)
    # all_titles.extend(instagram_titles)

    # linkedin_data, linkedin_links, linkedin_titles = monitor_linkedin_profiles()
    # all_files.extend(linkedin_data)
    # all_links.extend(linkedin_links)
    # all_titles.extend(linkedin_titles)

    # facebook_data, facebook_links, facebook_titles = monitor_facebook_groups()
    # all_files.extend(facebook_data)
    # all_links.extend(facebook_links)
    # all_titles.extend(facebook_titles)
    
    if not all_files:
        print("No data to process. Stopping execution.")
        return
    else:
        # start_notebook_assistant(all_files)
        # print("Monitoring completed.")
        # start_google_drive(all_links, all_titles)
        print("Google Drive upload completed.")

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

def start_google_drive(all_links, all_titles):
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

    body_with_links = f"Daily podcast update has been uploaded to Google Drive. Link: {file_metadata['webViewLink']}\n\nAdditional Links:\n{response}"
    for email in CONFIG["emails_to_share"]:
        gmail_service = GmailService(credentials=credentials)
        gmail_service.send_email(
            to=email,
            subject='Daily Ai Podcast Updates',
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

if __name__ == "__main__":
    main(sys.argv[1:])  