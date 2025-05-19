from abstractions.base_scraper import SocialScraper
import requests
from bs4 import BeautifulSoup # type: ignore
from utils.openai_manager import OpenAIService
from core.rate_limiter import RateLimiter
from datetime import datetime, timedelta

class NewsletterService(SocialScraper):
    def __init__(self, output_folder='output/newsletter', config=None):
        super().__init__(output_folder)
        self.config = config
        self.openai_service = OpenAIService(config=config) if config else None

    def scrape_text_from_links(self, links):
        """
        Scrapes all text content from the given list of links.

        Args:
            links (list): A list of URLs to scrape.

        Returns:
            dict: A dictionary where keys are links and values are the scraped text content.
        """
        text_content = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        for link in links:
            try:
                response = requests.get(link, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text_content[link] = soup.get_text(strip=True)
                else:
                    print(f"Failed to fetch {link}: {response.status_code}")
            except Exception as e:
                print(f"Error scraping {link}: {e}")

        return text_content

    def scrape_profile(self, url):
        """
        Scrapes the given URL for links and their child headers.

        Args:
            url (str): The URL to scrape.

        Returns:
            list: A list of dictionaries containing headers, links, and text content.
        """
        # Set custom headers to avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        RateLimiter.random_delay(10,20)
        # Fetch the website content
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract links and their child headers
        headers_and_links = []
        new_url = url
        new_url = self.modify_url(url)

        if url == "https://openai.com/news" or url == "https://www.deeplearning.ai/the-batch":
            for link in soup.find_all('a', href=True):
                # Check if the <a> tag has a header as a child
                header = link.find(['div'])
                if header:
                    if "https" in link['href'] or "http" in link['href']:
                        headers_and_links.append({
                            'header': header.get_text(strip=True),
                            'link': f"{link['href']}"
                        })
                    else:
                        headers_and_links.append({
                            'header': header.get_text(strip=True),
                            'link': f"{new_url}{link['href']}"
                        })
        elif url == "https://research.google/blog" or url == "https://news.mit.edu/topic/artificial-intelligence2":
            for link in soup.find_all('a', href=True):
                # Check if the <a> tag has a header as a child
                header = link.find(['span'])
                if header:
                    if "https" in link['href'] or "http" in link['href']:
                        headers_and_links.append({
                            'header': header.get_text(strip=True),
                            'link': f"{link['href']}"
                        })
                    else:
                        headers_and_links.append({
                            'header': header.get_text(strip=True),
                            'link': f"{new_url}{link['href']}"
                        })
        elif url == "https://deepmind.google/discover/blog":
            for link in soup.find_all('a', href=True):
                # Check if the <a> tag has a header as a child
                header = link.find(['p'])
                if header:
                    if "https" in link['href'] or "http" in link['href']:
                        headers_and_links.append({
                            'header': header.get_text(strip=True),
                            'link': f"{link['href']}"
                        })
                    else:
                        headers_and_links.append({
                            'header': header.get_text(strip=True),
                            'link': f"{new_url}{link['href']}"
                        })
        elif url == "https://www.kdnuggets.com":
            for link in soup.find_all('a', href=True):
                # Check if the <a> tag has a header as a child
                header = link.find(['b'])
                if header:
                    if "https" in link['href'] or "http" in link['href']:
                        headers_and_links.append({
                            'header': header.get_text(strip=True),
                            'link': f"{link['href']}"
                        })
                    else:
                        headers_and_links.append({
                            'header': header.get_text(strip=True),
                            'link': f"{new_url}{link['href']}"
                        })
        else:
            for link in soup.find_all('a', href=True):
                # Check if the <a> tag has a header as a child
                header = link.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if header:
                    headers_and_links.append({
                        'header': header.get_text(strip=True),
                        'link': f"{new_url}{link['href']}"
                    })

        # Print the headers and links
        print(f"Found {len(headers_and_links)} headers and links:")
        for item in headers_and_links:
            print(f"Header: {item['header']}, Link: {item['link']}")

        # Scrape text from the links
        links = [item['link'] for item in headers_and_links]

        print(f"Scraping text from {len(links)} links...")

        text_content = self.scrape_text_from_links(links)

        # Add the scraped text to the headers_and_links
        for item in headers_and_links:
            item['text'] = text_content.get(item['link'], None)

        return self.validate_date(headers_and_links)
    
    def validate_date(self, headers_and_links): 
        """
        Validate the date of the scraped content.
        This is a placeholder function and should be implemented based on your requirements.
        """
        # Implement your date validation logic here
        yesterday = datetime.now() - timedelta(days=1)
        yesterday_str = yesterday.strftime("%b %d, %Y")
        print(f"Yesterday's date: {yesterday_str}")

        new_headers_and_links = []
        for info in headers_and_links:
            RateLimiter.random_delay(5,10)
            print("Check if info text has yesterday's date")
            if not info.get('text'):
                print(f"No text found for {info['header']}. Skipping...")
                continue
            print(f"Checking content for {info['header']}")
            # Check if the content has yesterday's date
            if yesterday_str in info['text']:
                print(f"Content is relevant for {info['header']}.")
                new_headers_and_links.append(info)
                continue
            else:
                print(f"Content is not relevant for {info['header']}.")
                continue 
        return new_headers_and_links
    
    def modify_url(self, url):
        """
        Modify the URL to point to the correct location.
        This is a placeholder function and should be implemented based on your requirements.
        """
        new_url = url
        print(f"Modifying URL: {url}")
        # Implement your URL modification logic here
        if url == "https://huggingface.co/blog":
            new_url = "https://huggingface.co"
        if url == "https://openai.com/news":
            new_url = "https://openai.com"
        if url == "https://research.google/blog":
            new_url = "https://research.google"
        if url == "https://deepmind.google/discover/blog":
            new_url = "https://deepmind.google"
        if url == "https://www.deeplearning.ai/the-batch":
            new_url = "https://www.deeplearning.ai"
        if url == "https://news.mit.edu/topic/artificial-intelligence2":
            new_url = "https://news.mit.edu"

        return new_url