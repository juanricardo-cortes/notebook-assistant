class ErrorHandler:
    """
    Handles scraping exceptions, including CAPTCHA detection and generic errors.
    """
    @staticmethod
    def handle_captcha(driver):
        # Simple CAPTCHA detection based on page content
        page_source = driver.page_source.lower()
        if "captcha" in page_source or "verify you are human" in page_source:
            raise Exception("CAPTCHA encountered. Manual intervention required.")

    @staticmethod
    def handle_exception(e, context=""):
        print(f"Error in {context}: {str(e)}")
