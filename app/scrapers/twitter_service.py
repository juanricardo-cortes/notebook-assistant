from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abstractions.base_scraper import SocialScraper
from core.scroller import InfiniteScrollHelper
from core.rate_limiter import RateLimiter
import datetime
import re
import time

class TwitterScraper(SocialScraper):
    def __init__(self, driver, output_folder='output/twitter'):
        super().__init__(output_folder)
        self.driver = driver
        self.scroller = InfiniteScrollHelper(driver)
        self.wait = WebDriverWait(driver, 20)

    def scrape_profile(self, profile_url: str) -> list:
        self.driver.get(profile_url)
        RateLimiter.random_delay(30, 60)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        tweets = []

        # Scroll with infinite scroll helper
        self.scroller.scroll_until_content_stops()

        try:
            tweet_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article[data-testid='tweet']"))
            )
        except Exception as e:
            print(f"Error locating tweet elements: {e}")
            return tweets

        for tweet in tweet_elements:
            try:
                # Extract the time element
                time_element = tweet.find_element(By.TAG_NAME, "time")
                tweet_date = datetime.datetime.strptime(
                    time_element.get_attribute("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ"
                ).date()

                # Check if the tweet is from yesterday
                if tweet_date >= yesterday:
                    try:
                        content = tweet.find_element(By.CSS_SELECTOR, "div[lang]").text
                    except Exception:
                        content = "[Content not found]"

                    try:
                        comments = tweet.find_element(By.CSS_SELECTOR, "button[data-testid='reply']").text
                    except Exception:
                        print("Error finding comments button")
                        comments = "0"

                    try:
                        retweets = tweet.find_element(By.CSS_SELECTOR, "button[data-testid='retweet']").text
                    except Exception:
                        retweets = "0"

                    try:
                        likes = tweet.find_element(By.CSS_SELECTOR, "button[data-testid='like']").text
                    except Exception:
                        likes = "0"

                    tweets.append({
                        "date": str(tweet_date),
                        "content": content,
                        "comments": comments,
                        "retweets": retweets,
                        "likes": likes,
                        "url": self.driver.current_url
                    })
                elif tweet_date < yesterday:
                    break
            except Exception as e:
                print(f"Error processing tweet: {e}")
                continue

        print(f"Scraped {len(tweets)} tweets from {profile_url}.")
        return tweets
