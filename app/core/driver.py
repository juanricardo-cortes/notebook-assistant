from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class AntiDetectDriver:
    """
    Configures and returns a Selenium Chrome WebDriver instance with anti-detection features.
    Optionally supports proxy rotation.
    """
    def __init__(self, proxy=None):
        self.proxy = proxy

    def get_driver(self):
        print("Initializing AntiDetectDriver...")
        options = Options()
        options.add_argument("--disable-webrtc")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        if self.proxy:
            options.add_argument(f"--proxy-server={self.proxy}")
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
