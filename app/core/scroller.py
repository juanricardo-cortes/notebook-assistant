from selenium.webdriver.remote.webdriver import WebDriver
import random
import time

class InfiniteScrollHelper:
    """
    Reusable infinite scroll handler with fail-safes
    Implements strategies from search results: https://stackoverflow.com/a/70829799
    """
    def __init__(self, driver: WebDriver, max_attempts=10):
        self.driver = driver
        self.max_attempts = max_attempts

    def scroll_until_content_stops(self, scroll_element="document.body"):
        """
        Modified version of Gary's Blog implementation (Search Result [4])
        with additional fail-safes
        """
        attempts = 0
        old_height = self.driver.execute_script(f"return {scroll_element}.scrollHeight")
        
        while attempts < self.max_attempts:
            # Human-like scroll with random delay
            self.driver.execute_script(
                f"{scroll_element}.scrollTo({{top: {scroll_element}.scrollHeight, "
                f"behavior: 'smooth'}})"
            )
            time.sleep(random.uniform(1.5, 3.5))
            
            new_height = self.driver.execute_script(f"return {scroll_element}.scrollHeight")
            if new_height == old_height:
                break
                
            old_height = new_height
            attempts += 1

        return attempts < self.max_attempts  # Return success status
