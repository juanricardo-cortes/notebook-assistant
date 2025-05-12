import sys
import json
import os
import time
from core.driver import AntiDetectDriver
from services.youtube_service import YouTubeService
from services.twitter_service import TwitterScraper
from services.instagram_service import InstagramScraper
from services.linkedin_service import LinkedInScraper
from services.facebook_service import FacebookService
from monitors.social_monitor import SocialMonitor
from core.proxy_manager import FreeProxyManager

from utils.drive_manager import GoogleDriveUploader
from utils.gmail_manager import GmailService
from utils.credentials_provider import CredentialsProvider
from utils.email_provider import EmailProvider
from features.notebook_default import NotebookDefault
from utils.openai_manager import OpenAIService

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

        start_monitoring()

def start_monitoring():
    print("Starting monitoring...")
    # youtube_data, youtube_links = monitor_youtube_channels()
    twitter_data, twitter_links = monitor_twitter_profiles()
    # instagram_data, instagram_links = monitor_instagram_profiles()
    # linkedin_data, linkedin_links = monitor_linkedin_profiles()
    # facebook_data, facebook_links = monitor_facebook_groups()
    
    all_files = [] 
    all_links = []

    # all_files.extend(youtube_data)
    all_files.extend(twitter_data)
    # all_files.extend(instagram_data)
    # all_files.extend(linkedin_data)
    # all_files.extend(facebook_data)

    # all_links.extend(youtube_links)
    all_links.extend(twitter_links)
    # all_links.extend(instagram_links)
    # all_links.extend(linkedin_links)
    # all_links.extend(facebook_links)

    if not all_files:
        print("No data to process. Stopping execution.")
        return
    else:
        start_notebook_assistant(all_files)
        print("Monitoring completed.")
        start_google_drive(all_links)
        print("Google Drive upload completed.")

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
    driver = AntiDetectDriver().get_driver()
    instagram_scraper = InstagramScraper(driver)
    instagram_profiles = CONFIG["instagram_profiles"]
    monitor = SocialMonitor(instagram_scraper, instagram_profiles, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_linkedin_profiles():
    driver = AntiDetectDriver().get_driver()
    linkedin_scraper = LinkedInScraper(driver)
    linkedin_profiles = CONFIG["linkedin_profiles"]
    monitor = SocialMonitor(linkedin_scraper, linkedin_profiles, CONFIG)
    processed_data = monitor.execute_monitoring()
    return processed_data

def monitor_facebook_groups():
    driver = AntiDetectDriver().get_driver()
    facebook_scraper = FacebookService(driver)
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
        time.sleep(2)

def start_notebook_assistant(processed_data):
    driver = AntiDetectDriver().get_driver()
    notebook_assistant = NotebookDefault(driver=driver)
    notebook_assistant.generate_audio_podcast_from_profiles(processed_data)

def start_google_drive(all_links):
    time.sleep(10)  # Wait for the file to be ready
    credentials_provider = CredentialsProvider(CONFIG)
    credentials = credentials_provider.get_credentials()
    uploader = GoogleDriveUploader(credentials=credentials)
    uploader.authenticate()
    file_metadata = uploader.upload_file(emails_to_share=CONFIG["emails_to_share"])

    links_text = "\n".join(all_links)
    openai_service = OpenAIService(CONFIG["openai_api_key"])
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

if __name__ == "__main__":
    main(sys.argv[1:])