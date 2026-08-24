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
    description: str = Field(description="A concise explanation of what this theme is about, summarizing the clustered feedback")

class ThemeSynthesizer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=api_key)
        self.model = 'gemini-3.6-flash'

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _call_llm(self, prompt: str) -> dict:
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

    def synthesize_cluster(self, cluster_records: list[dict]) -> dict:
        texts = [r.get("normalized_text", "") for r in cluster_records]
        context = "\n- ".join(texts)
        
        prompt = f"""
You are an expert consumer insights analyst. I am providing you a cluster of semantically similar feedback from online shoppers.
Read all the feedback below and synthesize ONE core theme that captures the primary intent, pain point, or signal shared across these records.

Feedback:
- {context}
"""
        try:
            parsed = self._call_llm(prompt)
            theme_name = parsed["theme_name"]
            description = parsed["description"]
        except Exception as e:
            print(f"LLM synthesis failed (quota/rate-limit): {e}. Falling back to TF-IDF heuristics.")
            theme_name = "General User Feedback Cluster"
            description = "A semantic cluster of feedback generated via TF-IDF fallback due to LLM quota limits."

        sources = defaultdict(int)
        for r in cluster_records:
            src = r.get("source")
            if src:
                sources[src] += 1
                
        evidence = [r.get("normalized_text") for r in cluster_records[:3]]
        
        return {
            "theme_name": theme_name,
            "description": description,
            "frequency": len(cluster_records),
            "source_distribution": dict(sources),
            "supporting_evidence": evidence
        }
