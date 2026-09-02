import os
import json
from collections import defaultdict
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()


class ThemeSchema(BaseModel):
    theme_name: str = Field(description="A 2-4 word name for this theme")
    description: str = Field(
        description="A concise explanation of what this theme is about, summarizing the clustered feedback"
    )


class ThemeSynthesizer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.6-flash"

    @retry(
        stop=stop_after_attempt(1), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _call_llm(self, prompt: str) -> dict:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ThemeSchema,
                    temperature=0.2,
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"LLM call failed: {e}")
            return {
                "theme_name": "INSUFFICIENT_EVIDENCE",
                "description": "Fallback due to analysis failure",
            }

    def synthesize_cluster(self, cluster_records: list[dict]) -> dict:
        texts = [r.get("text", r.get("normalized_text", "")) for r in cluster_records]
        context = "\n- ".join(texts)

        prompt = f"""
You are an expert consumer insights analyst. I am providing you a cluster of semantically similar feedback from online shoppers.
Read all the feedback below and synthesize ONE core theme that captures the primary intent, pain point, barrier, or behavioral signal shared across these records.
RULES:
1. Do NOT use generic sentiment labels (e.g., 'Positive Experience', 'App Satisfaction', 'General Feedback'). Sentiment is secondary.
2. Themes MUST represent specific recurring user needs, behaviors, uncertainties, or purchase barriers.
3. If the feedback supports it, prefer structural themes like: 'Fit / Size Uncertainty', 'Product Quality Uncertainty', 'Price / Value Uncertainty', 'Comparison Difficulty', 'Returns / Exchange Confidence', 'Availability', 'Styling / Occasion', 'Social Validation', 'Product Information Gap', 'App Performance / UX Issues', 'Delivery / Shipping Friction'.
4. If the feedback is too scattered, or is MERELY GENERIC PRAISE (e.g. "nice", "good", "great app", "awesome", "best app") with no specific actionable need/barrier, you MUST set theme_name to 'INSUFFICIENT_EVIDENCE' and explain why in description.
5. NO THEMES based on generic sentiment. PERIOD.

Feedback:
- {context}
"""
        parsed = self._call_llm(prompt)
        theme_name = parsed["theme_name"]

        # Avoid generic fabricated clusters
        generic_terms = [
            "general",
            "feedback",
            "positive",
            "satisfaction",
            "experience",
            "praise",
            "appreciation",
            "great",
            "good",
            "awesome",
            "nice",
            "best",
        ]
        if (
            any(term in theme_name.lower() for term in generic_terms)
            or theme_name.upper() == "UNKNOWN"
        ):
            theme_name = "INSUFFICIENT_EVIDENCE"

        description = parsed["description"]
        is_fallback = theme_name == "INSUFFICIENT_EVIDENCE"

        sources = defaultdict(int)
        for r in cluster_records:
            src = r.get("source")
            if src:
                sources[src] += 1

        unique_records = len(cluster_records)
        source_coverage = len(sources)

        if unique_records > 10:
            evidence_confidence = "strong"
        elif unique_records > 5:
            evidence_confidence = "moderate"
        elif unique_records > 2:
            evidence_confidence = "weak"
        else:
            evidence_confidence = "unknown"

        evidence = []
        for r in cluster_records[:3]:
            evidence.append(
                {
                    "quote": r.get("text", r.get("normalized_text", "")),
                    "source": r.get("source", "Unknown"),
                    "trace_id": r.get("signal_id", r.get("raw_id", "unknown")),
                    "date": r.get("date", "Unknown date"),
                    "explanation": f"Supports the theme '{theme_name}'",
                }
            )

        return {
            "theme_name": theme_name,
            "description": description,
            "frequency": len(cluster_records),
            "unique_records": unique_records,
            "source_coverage": source_coverage,
            "evidence_confidence": evidence_confidence,
            "source_distribution": dict(sources),
            "supporting_evidence": evidence,
            "is_fallback": is_fallback,
        }
