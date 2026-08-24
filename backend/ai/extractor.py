import os
import json
import logging
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log
from ai.schemas import AISignalSchema
from pydantic import ValidationError
from dotenv import load_dotenv

load_dotenv()

# Setup basic logging to capture tenacity retries
logger = logging.getLogger("extractor")
logger.setLevel(logging.INFO)

class SignalExtractor:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-3.6-flash'
        self.retry_count = 0
        self.rate_limit_events = 0

    def record_retry(self, retry_state):
        self.retry_count += 1
        exception = retry_state.outcome.exception()
        if exception and '429' in str(exception):
            self.rate_limit_events += 1

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        reraise=True,
        before_sleep=lambda rs: rs.fn.__self__.record_retry(rs)
    )
    def extract_signals(self, text: str) -> dict:
        prompt = f"""
You are an expert consumer insights analyst for Myntra, a fashion e-commerce platform.
Analyze the following customer feedback and extract semantic signals.
Do not invent information. If a signal is not explicitly or implicitly supported by the text, return null.

Feedback:
"{text}"
"""
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AISignalSchema,
                temperature=0.0,
            ),
        )
        
        try:
            data = json.loads(response.text)
            validated_data = AISignalSchema(**data)
            return validated_data.model_dump()
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Error parsing LLM response: {e}")
            raise
