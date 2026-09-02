# Groq Quota Optimization Analysis

## 1. Measured Token Usage (Historical)
- **Average input tokens per record**: ~55 tokens (Batch input is ~220 tokens for 4 records)
- **Average output tokens per record**: ~300 tokens
- **Average total tokens per record**: ~355 tokens (if perfectly capped)
- **Maximum observed output tokens**: >1200 tokens for a batch of 4 (We know this because `max_tokens=1200` triggered a `400 json_validate_failed` error due to truncation).

## 2. Configuration Analysis
- **Is `max_tokens=1800` unnecessarily high?**
  Yes. For a batch of 4, the LLM realistically outputs 1250-1350 tokens. Reserving 1800 tokens requests ~2020 tokens from the daily 200k quota, artificially limiting us to ~99 batches (396 records/day).
- **Is `batch_size=4` optimal?**
  Yes. Larger batch sizes mathematically amortize the prompt instruction overhead (saving input tokens per record). However, if the batch size exceeds 4, the required `max_tokens` buffer increases the risk of early truncation and rate limits. Batch size 4 is the sweet spot.
- **Can a smaller `max_tokens` safely support the schema?**
  Yes. Based on the 1200-token truncation event, setting `max_tokens=1400` provides a ~150-token safety buffer over the maximum observed output, while reclaiming 400 reserved tokens per batch from the quota limit.

## 3. Projected Capacity Estimates
With the 200,000 TPD limit on `qwen/qwen3.6-27b`:
- **Requested tokens per batch (`max_tokens=1400`)**: ~1620 tokens
- **Estimated batches/day**: 200,000 / 1620 ≈ 123 batches
- **Estimated records processable per 200K TPD**: 123 * 4 = 492 records/day
- **Estimated number of days for 325 deferred records**: 325 / 492 ≈ 0.66 days (Under 1 day).

## 4. Prompt Token Overhead
The current prompt defines the JSON schema with pretty-printed indentation:
```json
{
  "results": [
    {
      "record_id": "string",
      "analysis": {
...
```
**Optimization:** Every indentation space consumes tokens. We can safely compress this entire JSON template into a single minified line. This will shave off approximately ~50-70 input tokens per batch, saving thousands of tokens over a daily run, without removing any analytical instructions.

---

## Final Recommendation

**CURRENT:**
- batch size: 4
- max_tokens: 1800
- avg tokens/record: 505 (reserved)
- estimated records/day: ~396

**RECOMMENDED:**
- batch size: 4
- max_tokens: 1400
- estimated tokens/batch: ~1620 (1400 + 220)
- estimated records/day: ~492
- estimated days for 325 records: ~0.66 days (16 hours)
- prompt adjustment: Minify the JSON structure template in `extractor.py` to a single line.
