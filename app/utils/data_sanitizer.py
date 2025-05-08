import re

class DataSanitizer:
    """
    Utility for removing personally identifiable information (PII) and sensitive data from text.
    """

    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

    @staticmethod
    def remove_pii(text: str) -> str:
        """
        Removes emails, phone numbers, and SSNs from the input text.
        """
        text = DataSanitizer.EMAIL_PATTERN.sub('[REDACTED_EMAIL]', text)
        text = DataSanitizer.PHONE_PATTERN.sub('[REDACTED_PHONE]', text)
        text = DataSanitizer.SSN_PATTERN.sub('[REDACTED_SSN]', text)
        return text
