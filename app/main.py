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
        start_monitoring()
        # start_email_provider()

def start_monitoring():
    print("Starting monitoring...")
    all_files = [
        # "C:/pinokio/api/notebook-assistant/app/output/youtube/20250509/youtube__AllAboutAI_20250509.txt",
        # "C:/pinokio/api/notebook-assistant/app/output/youtube/20250509/youtube__DavidOndrej_20250509.txt"
    ]
    # all_files.extend(monitor_youtube_channels())
    # all_files.extend(monitor_twitter_profiles())
    # all_files.extend(monitor_linkedin_profiles())
    # all_files.extend(monitor_instagram_profiles())
    # all_files.extend(monitor_facebook_groups())
    start_notebook_assistant(all_files)
    print("Monitoring completed.")

def monitor_youtube_channels():
    api_key = CONFIG["youtube_api_key"]
    channel_urls = CONFIG["youtube_channels"]
    youtube_service = YouTubeService(api_key)
    monitor = SocialMonitor(youtube_service, channel_urls)
    return monitor.execute_monitoring()

def monitor_twitter_profiles():
    driver = AntiDetectDriver().get_driver()
    twitter_scraper = TwitterScraper(driver)
    twitter_profiles = CONFIG["twitter_profiles"]
    monitor = SocialMonitor(twitter_scraper, twitter_profiles)
    return monitor.execute_monitoring()

def monitor_instagram_profiles():
    driver = AntiDetectDriver().get_driver()
    instagram_scraper = InstagramScraper(driver)
    instagram_profiles = CONFIG["instagram_profiles"]
    monitor = SocialMonitor(instagram_scraper, instagram_profiles)
    return monitor.execute_monitoring()

def monitor_linkedin_profiles():
    driver = AntiDetectDriver().get_driver()
    linkedin_scraper = LinkedInScraper(driver)
    linkedin_profiles = CONFIG["linkedin_profiles"]
    monitor = SocialMonitor(linkedin_scraper, linkedin_profiles)
    return monitor.execute_monitoring()

def monitor_facebook_groups():
    driver = AntiDetectDriver().get_driver()
    facebook_scraper = FacebookService(driver)
    facebook_groups = CONFIG["facebook_groups"]
    monitor = SocialMonitor(facebook_scraper, facebook_groups)
    return monitor.execute_monitoring()

def start_proxy_rotation():
    proxy_manager = FreeProxyManager()
    all_proxies = proxy_manager.get_proxy_list()
    print(f"Found {len(all_proxies)} proxies")
    working_proxy = proxy_manager.get_random_proxy()
    print(f"Random working proxy: {working_proxy}")

def start_email_provider():
    from utils.email_provider import EmailProvider
    mail_api = EmailProvider()
    for _ in range(3):
        email, password = mail_api.create_email_with_credentials()
        print("Generated Email:", email)
        print("Generated Password:", password)
        time.sleep(2)

def start_notebook_assistant(processed_data):
    from features.notebook_default import NotebookDefault
    notebook_assistant = NotebookDefault()
    notebook_assistant.generate_audio_podcast_from_profiles(processed_data)

if __name__ == "__main__":
    main(sys.argv[1:])