import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from abstractions.base_scraper import SocialScraper
from linkedin_scraper import actions
import time
import re

class LinkedInScraper(SocialScraper):
    def __init__(self, driver, output_folder='output/linkedin'):
        super().__init__(output_folder)
        self.driver = driver  # Initialize Selenium WebDriver
        self.wait = WebDriverWait(driver, 20)
        try: 
            # self.create_new_linkedin_account()
            actions.login(self.driver, "petecastiglione3@chefalicious.com", "thepunisher")  # Log in to LinkedIn
        except Exception as e:
            # Handle login errors (e.g., incorrect credentials, network issues)
            # Dynamically create new credentials if needed
            print(f"Error logging in to LinkedIn: {e}")
            return

    def scrape_profile(self, profile_url: str) -> list:
        try:
            self.driver.get(f"{profile_url}/recent-activity/all/")  # Navigate to the profile URL

            time.sleep(10)  # Wait for the page to load
            text = self.driver.find_element("tag name", "body").text
            posts = self.extract_posts_from_text(text)
            # self.driver.quit()
        except Exception as e:
            print(f"Error navigating to profile: {e}")
            return []
        return posts

    def extract_posts_from_text(self, text):
        posts = []
        post_pattern = re.compile(r"Feed post number \d+.*?Like\nComment\nRepost", re.DOTALL)
        matches = post_pattern.findall(text)

        for match in matches:
            try:
                # Extract author
                author_match = re.search(r"^Feed post number \d+\n(.*?)\n", match, re.MULTILINE)
                author = author_match.group(1).strip() if author_match else "Unknown"

                # Extract time posted
                time_match = re.search(r"(\d+\s\w+\sago)", match)
                time_posted = time_match.group(1).strip() if time_match else "Unknown"

                # Extract content
                content_match = re.search(r"Follow\n(.*?)\n…more", match, re.DOTALL)
                content = content_match.group(1).strip() if content_match else "[Content not found]"

                # Extract likes, comments, and reposts
                comments_match = re.search(r"(\d+)\s+comment", match)
                comments = int(comments_match.group(1)) if comments_match else 0

                reposts_match = re.search(r"(\d+)\s+repost", match)
                reposts = int(reposts_match.group(1)) if reposts_match else 0

                likes_match = re.search(r"(\d+)\n(?:\d+\s+comment|\d+\s+repost|Like)\n(?:Comment|Repost)?", match)
                likes = int(likes_match.group(1)) if likes_match else 0

                posts.append({
                    "author": author,
                    "time_posted": time_posted,
                    "content": content,
                    "likes": likes,
                    "comments": comments,
                    "reposts": reposts
                })
            except Exception as e:
                print(f"Error processing post: {e}")
                continue

        return posts

    def create_new_linkedin_account(self):
        from utils.email_provider import EmailProvider
        mail_api = EmailProvider()
        newemail, newpassword = mail_api.create_email_with_credentials()
        print("Email:", newemail)
        print("Password:", newpassword)

        self.driver.get("https://www.linkedin.com/signup")
        time.sleep(5)

        # Fill out the registration form
        email = self.driver.find_element(By.NAME, "email-or-phone")
        password = self.driver.find_element(By.NAME, "password")
        join_now = self.driver.find_element(By.ID, "join-form-submit")

        # Fill in the form fields with the provided data
        email.send_keys(newemail)

        time.sleep(random.randint(2, 4))
        password.send_keys(newpassword)

        time.sleep(random.randint(2, 4))
        join_now.click()

        time.sleep(random.randint(2, 4))
        firstname = self.driver.find_element(By.NAME, "first-name")
        lastname = self.driver.find_element(By.NAME, "last-name")

        time.sleep(random.randint(2, 4))
        firstname.send_keys("Pete")
        time.sleep(random.randint(2, 4))
        lastname.send_keys("Castiglione")
        time.sleep(random.randint(2, 4))

        join_now = self.driver.find_element(By.ID, "join-form-submit")
        join_now.click()
        time.sleep(1000)
