from abc import ABC, abstractmethod
import datetime
import os
import re
import json
from utils.openai_manager import OpenAIService

class SocialScraper(ABC):
    def __init__(self, output_folder):
        date_str = datetime.date.today().strftime("%Y%m%d")
        self.output_folder = f"{output_folder}/{date_str}"
        os.makedirs(self.output_folder, exist_ok=True)

    @abstractmethod
    def scrape_profile(self, profile_url: str) -> list:
        """Scrape content from a profile URL. Must return list of content items."""
        pass

    def save_content(self, profile_handle: str, content: list, platform: str):
        """Save scraped content to JSON file using YouTube-style naming convention"""
        safe_handle = re.sub(r'[^\w\-_. ]', '_', profile_handle)
        date_str = datetime.date.today().strftime("%Y%m%d")
        filename = f"{self.output_folder}/{platform}_{safe_handle}_{date_str}.txt"
        print(f"Saving content to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)

        return filename

    def check_content(self, content: list, config) -> bool:
        """Check if the content is empty or not."""
        openai_service = OpenAIService(config["openai_api_key"])
        instructions = "Check if the content talks about AI and does it have enough likes, comments, shares, etc. If yes, return True, else return False."
        prompt = f"Content: {content}"
        response = openai_service.generate_response(prompt, instructions)
        print(f"Response from OpenAI: {response}")
        if response.lower() == "true":
            return True
        return False    