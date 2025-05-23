from abstractions.base_scraper import SocialScraper
from utils.openai_manager import OpenAIService
from core.rate_limiter import RateLimiter

class GeminiService(SocialScraper):
    def __init__(self, output_folder='output/gemini', config=None):
        super().__init__(output_folder)
        self.config = config
        print("Starting GeminiService")

    def scrape_profile(self, prompt: str) -> list:
        RateLimiter.random_delay()
        openai_service = OpenAIService(self.config)
        instructions = "You are an expert in everything AI."
        prompt = f"{prompt}"
        response = openai_service.generate_gemini_response(prompt, instructions)
        return [response]