from abc import ABC, abstractmethod
import datetime
import os
import re
import json
import time
from utils.openai_manager import OpenAIService
from core.rate_limiter import RateLimiter
class SocialScraper(ABC):
    def __init__(self, output_folder):
        date_str = datetime.date.today().strftime("%Y%m%d")
        self.output_folder = f"{output_folder}/{date_str}"
        os.makedirs(self.output_folder, exist_ok=True)

    @abstractmethod
    def scrape_profile(self, profile_url: str) -> list:
        """Scrape content from a profile URL. Must return list of content items."""
        pass

    def save_content(self, profile_handle: str, content: list, platform: str, count: str):
        """Save scraped content to JSON file using YouTube-style naming convention"""
        safe_handle = re.sub(r'[^\w\-_. ]', '_', profile_handle)
        date_str = datetime.date.today().strftime("%Y%m%d")
        random_str = ''.join([chr(i) for i in os.urandom(6)]).encode('utf-8').hex()[:6]
        filename = f"{self.output_folder}/{platform}_{safe_handle}_{date_str}_{random_str}_{count}.txt"
        print(f"Saving content to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)

        return filename

    def check_content(self, content: list, config, valuation) -> list:
        """Check if the content is empty or not."""
        print("CHECK CONTENT")
        print(f"OUTPUT FOLDER: {self.output_folder}")
        
        if "perplexity" in self.output_folder:
            openai_service = OpenAIService(config=config)    
            instructions = valuation
            new_content = []
            for content_item in content:
                RateLimiter.random_delay(10,15)
                prompt = f"{valuation}: Content: {content_item['answer_text']}"
                response = openai_service.generate_gemini_response(prompt, instructions)
                print(f"Response from OpenAI: {response}")
                if "not applicable" not in response.lower():
                    new_content.append(response)
                else:
                    print("removed")
            return new_content
        else:
            openai_service = OpenAIService(config=config)    
            instructions = valuation
            new_content = []
            for content_item in content:
                RateLimiter.random_delay(10,15)
                prompt = f"{valuation}: Content: {content_item}"
                response = openai_service.generate_gemini_response(prompt, instructions)
                print(f"Response from OpenAI: {response}")
                if "not applicable" not in response.lower():
                    new_content.append(response)
                else:
                    print("removed")
            return new_content
        
    def extract_important_links(self, content: list, config) -> str:
        """Extract important links from the content."""
        RateLimiter.random_delay(10,15)
        openai_service = OpenAIService(config=config)
        instructions = config["extract_links_prompt"]
        prompt = f"{instructions}: Content: {content}"
        response = openai_service.generate_response(prompt, instructions)
        print(f"Response from OpenAI: {response}")
        return response
    
    def generate_title(self, data, config) -> str:
        """Get summary of the content."""
        RateLimiter.random_delay(10,15)
        openai_service = OpenAIService(config=config)
        instructions = config["title_prompt"]
        prompt = f"{instructions}: Content: {data}"
        response = openai_service.generate_response(prompt, instructions)
        print(f"Response from OpenAI: {response}")
        return response
    
    def generate_summary(self, data: list, config) -> str:
        """Get summary of the content"""
        if "perplexity" in self.output_folder:
            for data_element in data:
                RateLimiter.random_delay(10,15)
                openai_service = OpenAIService(config=config)
                instructions = config["summarize_prompt"]
                prompt = f"{instructions}: Content: {data_element}"
                response = openai_service.generate_gemini_response(prompt, instructions)
                break
            return response
        else: 
            RateLimiter.random_delay(10,15)
            openai_service = OpenAIService(config=config)
            instructions = config["summarize_prompt"]
            prompt = f"{instructions}: Content: {data}"
            response = openai_service.generate_gemini_response(prompt, instructions)
            print(f"Response from OpenAI: {response}")
            return response
    