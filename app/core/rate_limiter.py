import time
import random

class RateLimiter:
    """
    Enforces delays between requests to avoid triggering anti-bot systems.
    """
    @staticmethod
    def random_delay(min_delay=1.5, max_delay=4.0):
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
