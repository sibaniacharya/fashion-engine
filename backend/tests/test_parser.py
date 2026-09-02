import pytest
import json
from pydantic import ValidationError
from ai.extractor import robust_parse, LLMParseError, BatchExtractionResponse


def test_clean_json():
    text = '{"results": [{"record_id": "1", "analysis": {"user_segment": "UNKNOWN", "shopping_intent": "UNKNOWN", "wishlist_intent": "UNKNOWN", "purchase_stage": "UNKNOWN", "pain_point": "UNKNOWN", "uncertainty": "UNKNOWN", "purchase_barrier": "UNKNOWN", "information_sought": "UNKNOWN", "comparison_behavior": "UNKNOWN", "fit_size_signal": "UNKNOWN", "styling_signal": "UNKNOWN", "price_signal": "UNKNOWN", "quality_signal": "UNKNOWN", "social_validation_signal": "UNKNOWN", "occasion_signal": "UNKNOWN", "external_research_behavior": "UNKNOWN", "theme_candidate": "UNKNOWN", "evidence_strength": "UNKNOWN"}}]}'
    data = robust_parse(text)
    assert "results" in data
    validated = BatchExtractionResponse(**data)
    assert validated.results[0].record_id == "1"


def test_markdown_json():
    text = '```json\n{"results": [{"record_id": "2", "analysis": {"user_segment": "UNKNOWN", "shopping_intent": "UNKNOWN", "wishlist_intent": "UNKNOWN", "purchase_stage": "UNKNOWN", "pain_point": "UNKNOWN", "uncertainty": "UNKNOWN", "purchase_barrier": "UNKNOWN", "information_sought": "UNKNOWN", "comparison_behavior": "UNKNOWN", "fit_size_signal": "UNKNOWN", "styling_signal": "UNKNOWN", "price_signal": "UNKNOWN", "quality_signal": "UNKNOWN", "social_validation_signal": "UNKNOWN", "occasion_signal": "UNKNOWN", "external_research_behavior": "UNKNOWN", "theme_candidate": "UNKNOWN", "evidence_strength": "UNKNOWN"}}]}\n```'
    data = robust_parse(text)
    assert "results" in data
    validated = BatchExtractionResponse(**data)
    assert validated.results[0].record_id == "2"


def test_surrounding_text():
    text = 'Here is the extracted data:\n{"results": [{"record_id": "3", "analysis": {"user_segment": "UNKNOWN", "shopping_intent": "UNKNOWN", "wishlist_intent": "UNKNOWN", "purchase_stage": "UNKNOWN", "pain_point": "UNKNOWN", "uncertainty": "UNKNOWN", "purchase_barrier": "UNKNOWN", "information_sought": "UNKNOWN", "comparison_behavior": "UNKNOWN", "fit_size_signal": "UNKNOWN", "styling_signal": "UNKNOWN", "price_signal": "UNKNOWN", "quality_signal": "UNKNOWN", "social_validation_signal": "UNKNOWN", "occasion_signal": "UNKNOWN", "external_research_behavior": "UNKNOWN", "theme_candidate": "UNKNOWN", "evidence_strength": "UNKNOWN"}}]}\nHope this helps!'
    data = robust_parse(text)
    assert "results" in data
    validated = BatchExtractionResponse(**data)
    assert validated.results[0].record_id == "3"


def test_array_fallback():
    text = 'Here is the extracted data:\n[{"record_id": "4", "analysis": {"user_segment": "UNKNOWN", "shopping_intent": "UNKNOWN", "wishlist_intent": "UNKNOWN", "purchase_stage": "UNKNOWN", "pain_point": "UNKNOWN", "uncertainty": "UNKNOWN", "purchase_barrier": "UNKNOWN", "information_sought": "UNKNOWN", "comparison_behavior": "UNKNOWN", "fit_size_signal": "UNKNOWN", "styling_signal": "UNKNOWN", "price_signal": "UNKNOWN", "quality_signal": "UNKNOWN", "social_validation_signal": "UNKNOWN", "occasion_signal": "UNKNOWN", "external_research_behavior": "UNKNOWN", "theme_candidate": "UNKNOWN", "evidence_strength": "UNKNOWN"}}]\nHope this helps!'
    data = robust_parse(text)
    assert "results" in data
    validated = BatchExtractionResponse(**data)
    assert validated.results[0].record_id == "4"


def test_malformed_json():
    text = '{"results": [{"record_id": "5", "analysis": {"user_segment": '  # Truncated
    with pytest.raises(LLMParseError):
        robust_parse(text)


def test_empty_response():
    text = "\nI am unable to analyze this record."
    with pytest.raises(LLMParseError):
        robust_parse(text)


def test_missing_fields_validation():
    # Missing required field `purchase_stage`
    text = '{"results": [{"record_id": "6", "analysis": {"user_segment": "UNKNOWN", "shopping_intent": "UNKNOWN", "wishlist_intent": "UNKNOWN", "pain_point": "UNKNOWN", "uncertainty": "UNKNOWN", "purchase_barrier": "UNKNOWN", "information_sought": "UNKNOWN", "comparison_behavior": "UNKNOWN", "fit_size_signal": "UNKNOWN", "styling_signal": "UNKNOWN", "price_signal": "UNKNOWN", "quality_signal": "UNKNOWN", "social_validation_signal": "UNKNOWN", "occasion_signal": "UNKNOWN", "external_research_behavior": "UNKNOWN", "theme_candidate": "UNKNOWN", "evidence_strength": "UNKNOWN"}}]}'
    data = robust_parse(text)
    with pytest.raises(ValidationError):
        BatchExtractionResponse(**data)


def test_wrong_enum_validation():
    text = '{"results": [{"record_id": "7", "analysis": {"user_segment": "Segment unknown", "shopping_intent": "UNKNOWN", "wishlist_intent": "UNKNOWN", "purchase_stage": "UNKNOWN", "pain_point": "UNKNOWN", "uncertainty": "UNKNOWN", "purchase_barrier": "UNKNOWN", "information_sought": "UNKNOWN", "comparison_behavior": "UNKNOWN", "fit_size_signal": "UNKNOWN", "styling_signal": "UNKNOWN", "price_signal": "UNKNOWN", "quality_signal": "UNKNOWN", "social_validation_signal": "UNKNOWN", "occasion_signal": "UNKNOWN", "external_research_behavior": "UNKNOWN", "theme_candidate": "UNKNOWN", "evidence_strength": "UNKNOWN"}}]}'
    data = robust_parse(text)
    with pytest.raises(ValidationError):
        BatchExtractionResponse(**data)


if __name__ == "__main__":
    pytest.main([__file__])
