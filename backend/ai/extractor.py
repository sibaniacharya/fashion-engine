import os
import json
import logging
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from ai.schemas import AISignalSchema
from pydantic import ValidationError, BaseModel
from typing import List
from dotenv import load_dotenv
import re

load_dotenv()


class LLMParseError(Exception):
    pass


def robust_parse(text: str) -> dict:
    import json

    # Strip markdown fences
    t = re.sub(r"^```json\s*", "", text, flags=re.MULTILINE | re.IGNORECASE)
    t = re.sub(r"^```\s*", "", t, flags=re.MULTILINE)
    t = t.strip()

    # Direct parse
    try:
        parsed = json.loads(t)
        if isinstance(parsed, list):
            return {"results": parsed}
        return parsed
    except json.JSONDecodeError:
        pass

    # Regex fallback for array (prioritize over dict so we don't just grab the first element)
    match_arr = re.search(r"\[.*\]", t, re.DOTALL)
    if match_arr:
        try:
            arr = json.loads(match_arr.group(0))
            if isinstance(arr, list) and len(arr) > 0 and isinstance(arr[0], dict):
                return {"results": arr}
        except json.JSONDecodeError:
            pass

    # Regex fallback for dict
    match = re.search(r"\{.*\}", t, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise LLMParseError(f"Failed to extract JSON from LLM response")


logger = logging.getLogger("extractor")
logger.setLevel(logging.INFO)


class BatchRecordResult(BaseModel):
    record_id: str
    analysis: AISignalSchema


class BatchExtractionResponse(BaseModel):
    results: List[BatchRecordResult]


class SignalExtractor:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in .env.")
        self.client = Groq(api_key=api_key)
        self.model = "qwen/qwen3.8-27b"
        self.retry_count = 0
        self.rate_limit_events = 0

    def record_retry(self, retry_state):
        self.retry_count += 1
        exception = retry_state.outcome.exception()
        if exception and "429" in str(exception):
            self.rate_limit_events += 1

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=5, min=10, max=120),
        reraise=True,
    )
    def extract_signals_batch(self, batch: list[dict]) -> dict:
        """
        Batch format expected: [{"record_id": "...", "source": "...", "text": "..."}, ...]
        Returns a dict mapping record_id -> analysis dict
        """
        if not batch:
            return {}

        batch_prompt = ""
        for i, record in enumerate(batch):
            batch_prompt += f"RECORD {i+1}\n"
            batch_prompt += f"ID: {record['record_id']}\n"
            batch_prompt += f"Source: {record['source']}\n"
            batch_prompt += f"Text: {record['text']}\n\n"

        prompt = f"""
You are a consumer insights analyst for Myntra. Extract semantic signals from the records into strictly valid JSON.
RULES:
1. NEVER invent information. Use 'UNKNOWN' if missing evidence.
2. Enum constraints:
- wishlist_intent: EXPLICIT_WISHLIST, EXPLICIT_PURCHASE_INTENT, GENERAL_PRODUCT_INTEREST, PURCHASE_EVALUATION, COMPARISON, POSTPONEMENT, ABANDONMENT, BOOKMARKING, UNKNOWN
- external_research_behavior: EXPLICIT_RESEARCH, IMPLIED_RESEARCH, NO_EVIDENCE, UNKNOWN
- user_segment: COMPARISON_SHOPPER, FIT_CONSCIOUS, QUALITY_CONSCIOUS, VALUE_CONSCIOUS, FREQUENT_SHOPPER, UNKNOWN
- evidence_strength: STRONG, MODERATE, WEAK, UNKNOWN
- purchase_stage: DISCOVERY, EVALUATION, POSTPONEMENT, POST_PURCHASE, UNKNOWN
- Flags (shopping_intent, comparison_behavior, fit_size_signal, styling_signal, price_signal, quality_signal, social_validation_signal, occasion_signal): YES, NO, UNKNOWN

Records:
{batch_prompt}

Output strictly valid JSON matching this structure:
{{"results": [{{"record_id": "string", "analysis": {{"user_segment": "UNKNOWN", "shopping_intent": "UNKNOWN", "wishlist_intent": "UNKNOWN", "purchase_stage": "UNKNOWN", "pain_point": "UNKNOWN", "uncertainty": "UNKNOWN", "purchase_barrier": "UNKNOWN", "information_sought": "UNKNOWN", "comparison_behavior": "UNKNOWN", "fit_size_signal": "UNKNOWN", "styling_signal": "UNKNOWN", "price_signal": "UNKNOWN", "quality_signal": "UNKNOWN", "social_validation_signal": "UNKNOWN", "occasion_signal": "UNKNOWN", "external_research_behavior": "UNKNOWN", "theme_candidate": "UNKNOWN", "evidence_strength": "UNKNOWN"}}}}]}}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data extraction AI. Output strictly valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=1400,
                response_format={"type": "json_object"},
            )

            raw_text = response.choices[0].message.content

            data = robust_parse(raw_text)
            validated_data = BatchExtractionResponse(**data)

            # Map back to dict
            result_map = {}
            for res in validated_data.results:
                result_map[res.record_id] = res.analysis.model_dump()

            return result_map

        except (LLMParseError, ValidationError) as ve:
            logger.error(f"Parse/Validation Error: {ve}")
            raise
        except Exception as e:
            if "429" in str(e):
                self.rate_limit_events += 1
            print(f"Error calling Groq or parsing response: {e}")
            raise
