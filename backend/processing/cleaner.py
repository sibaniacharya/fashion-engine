import re
import string
from langdetect import detect, LangDetectException

class DataCleaner:
    def __init__(self):
        # Basic regex for PII
        self.email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        self.phone_pattern = re.compile(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\b')
        
        # Punctuation and emoji checking
        # Match anything that is an alphabet or number
        self.meaningful_char_pattern = re.compile(r'[a-zA-Z0-9]')

    def normalize_whitespace(self, text: str) -> str:
        if not text:
            return ""
        # Replace multiple spaces/newlines with a single space
        return re.sub(r'\s+', ' ', text).strip()

    def mask_pii(self, text: str) -> str:
        text = self.email_pattern.sub('[EMAIL]', text)
        # Note: phone regex can be overly aggressive, but sufficient for this scope
        text = self.phone_pattern.sub('[PHONE]', text)
        return text

    def is_meaningful(self, text: str) -> bool:
        # Check if there's at least one alphanumeric character
        if not self.meaningful_char_pattern.search(text):
            return False
        return True

    def detect_language(self, text: str) -> str:
        try:
            return detect(text)
        except LangDetectException:
            return "unknown"

    def clean_record(self, raw_text: str) -> dict:
        """
        Processes the text and returns a dictionary with the results.
        """
        result = {
            "is_valid": True,
            "rejection_reason": None,
            "normalized_text": "",
            "language": "unknown"
        }

        if not raw_text or not raw_text.strip():
            result["is_valid"] = False
            result["rejection_reason"] = "Empty record"
            return result

        # 1. Whitespace normalization
        norm_text = self.normalize_whitespace(raw_text)

        # 2. Meaningful content check (drops emoji-only or punctuation-only)
        if not self.is_meaningful(norm_text):
            result["is_valid"] = False
            result["rejection_reason"] = "Meaningless content"
            return result
            
        # 3. PII Masking
        norm_text = self.mask_pii(norm_text)
        
        result["normalized_text"] = norm_text
        
        # 4. Language Detection
        result["language"] = self.detect_language(norm_text)
        
        return result
