from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abstractions.base_scraper import SocialScraper
from core.scroller import InfiniteScrollHelper
import datetime
import time

class InstagramScraper(SocialScraper):
    def __init__(self, driver, output_folder='output/instagram'):
        super().__init__(output_folder)
        self.driver = driver
        self.scroller = InfiniteScrollHelper(driver)
        self.wait = WebDriverWait(driver, 25)
    
    def close_popup(self):
        try:
            # Perform a click outside the popup to close it
            body_element = self.driver.find_element(By.TAG_NAME, "body")
            body_element.click()
            print("Clicked outside the popup to close it.")
        except Exception as e:
            print(f"Failed to close popup by clicking outside: {e}")

    def scrape_profile(self, profile_url: str) -> list:
        from playwright.sync_api import sync_playwright # type: ignore

        posts = []
        
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Navigate to the profile URL
            page.goto(profile_url)

            page.wait_for_timeout(10000)  # Wait for the page to load

            # Close any popups by clicking outside
            try:
                page.locator("body").click()
                print("Clicked outside to close any popups.")
            except Exception as e:
                print(f"No popup to close or failed to close popup: {e}")

            # Scroll and collect posts
            while True:
                try:
                    # Wait for posts to load
                    page.wait_for_selector("article.x1iyjqo2", timeout=10000)  # Updated selector and increased timeout

                    # Extract posts
                    post_elements = page.locator("article.x1iyjqo2 div._ac7v").element_handles()  # Updated selector
                    print(f"Found {len(post_elements)} posts.")
                    for post in post_elements:
                        try:
                            post_date = post.query_selector("time").get_attribute("datetime")
                            post_date = datetime.datetime.strptime(post_date, "%Y-%m-%dT%H:%M:%S.%fZ").date()

                            if post_date == yesterday:
                                content = post.query_selector("div.x1lliihq").inner_text() if post.query_selector("div.x1lliihq") else "[Content not found]"  # Updated selector
                                likes = post.query_selector("xpath=//span[contains(text(), 'likes')]").inner_text() if post.query_selector("xpath=//span[contains(text(), 'likes')]") else "0"
                                comments = post.query_selector("xpath=//ul/li/div/span").inner_text() if post.query_selector("xpath=//ul/li/div/span") else "0"

                                posts.append({
                                    "date": str(post_date),
                                    "content": content,
                                    "likes": likes,
                                    "comments": comments,
                                    "url": profile_url
                                })
                            elif post_date < yesterday:
                                browser.close()
                                return posts
                        except Exception as e:
                            print(f"Error processing post: {e}")
                            continue

                    # Scroll down
                    page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                except Exception as e:
                    print(f"Error during scrolling or extracting posts: {e}")
                    break

            browser.close()
        return posts

