# AI Discovery Engine: Edge Cases & Failure Scenarios

This document outlines the edge cases and failure scenarios for the AI Discovery Engine and details their handling and validation strategies.

## 1. Data Ingestion & API Constraints

### Data Ingestion Source API Failures
**Scenario:** A target source API (e.g., Reddit API or Google Play scraper) goes down, times out, or changes its response format.
**Expected Behavior:** The ingestion job fails gracefully for the affected source but does not crash the entire ingestion pipeline.
**Handling Strategy:** Implement try-catch blocks around source-specific adapters. Use exponential backoff for retries. If the API format changes, alert the developer and mark the ingestion job as failed for that source, while other sources continue to run.
**Validation Approach:** Mock API failures in unit tests to ensure the ingestion manager continues with other sources.

### Rate Limits from Sources
**Scenario:** The system hits API rate limits while scraping or fetching data.
**Expected Behavior:** The system pauses fetching for the required duration instead of getting banned.
**Handling Strategy:** Implement rate-limit detection (e.g., handling 429 HTTP status codes) and respect `Retry-After` headers. Use throttling in the ingestion workers.
**Validation Approach:** Simulate 429 responses in tests and verify that the worker sleeps for the correct duration.

## 2. Data Cleaning & Normalization

### Duplicate Reviews
**Scenario:** The same review is fetched multiple times across different ingestion runs or duplicated within a single run.
**Expected Behavior:** Only one instance of the review is retained in the `NormalizedFeedback` table.
**Handling Strategy:** Use a composite unique key (e.g., `source` + `source_id`) at the database level for exact matches. Use hashing or fasttext similarity for near-duplicate detection.
**Validation Approach:** Insert duplicate records during tests and verify the database rejects or deduplicates them correctly.

### Spam and Irrelevant Content
**Scenario:** A user posts a review that is either spam (e.g., "click here for free money") or completely irrelevant to fashion/shopping (e.g., "The weather is nice today").
**Expected Behavior:** The review is flagged and excluded from AI signal extraction.
**Handling Strategy:** Implement heuristic filters (regex for URLs/spam keywords) and an initial LLM/classifier pass to flag `is_relevant` boolean.
**Validation Approach:** Provide a known dataset of spam/irrelevant reviews and ensure the pipeline correctly drops them.

### Short but Meaningful Reviews
**Scenario:** A review contains fewer than 8 words but contains strong purchase signals (e.g., "Should I size up?", "Is this transparent?").
**Expected Behavior:** The review is retained and passed to the AI engine.
**Handling Strategy:** Do not apply blind word-count filters. Route short reviews to the relevance classifier or LLM to determine if they contain actionable fashion/shopping signals.
**Validation Approach:** Feed specific short-but-meaningful test strings to the pipeline and verify they reach the normalized table.

### Multilingual Content
**Scenario:** Feedback is submitted in a language other than English (e.g., Spanish or Hindi).
**Expected Behavior:** The review is not silently discarded; its language is detected and recorded.
**Handling Strategy:** Use a library like `langdetect` or `fasttext`. Tag the record with the detected language code. Optionally, filter out non-English records for initial AI processing but keep them stored for future iterations.
**Validation Approach:** Pass non-English text to the cleaner and verify it is tagged with the correct language code and not deleted.

### Emoji-containing Reviews
**Scenario:** A review relies heavily on emojis for context (e.g., "Love the dress 😍 but it doesn't fit 😭").
**Expected Behavior:** Meaningful text is preserved; the review is not dropped just because it has emojis.
**Handling Strategy:** Strip emojis if they break downstream systems, or keep them if the LLM can interpret them. Do not filter out rows solely based on emoji presence. Empty reviews with *only* emojis may be dropped.
**Validation Approach:** Test with emoji-only text (should be dropped) and text-plus-emoji (should be retained).

### Missing Fields and Malformed Data
**Scenario:** A source returns a review missing a title, rating, or timestamp, or returns malformed JSON.
**Expected Behavior:** The system handles missing optional fields gracefully and rejects wholly malformed records without crashing.
**Handling Strategy:** Use Pydantic models with explicit `Optional` fields and default values (e.g., `rating=None`). Catch validation errors for mandatory fields and skip the record.
**Validation Approach:** Feed partial or malformed JSON into the adapter and assert it logs a warning and skips the record without raising an unhandled exception.

### Personally Identifiable Information (PII)
**Scenario:** A user includes their phone number, email address, or full name in a review.
**Expected Behavior:** The PII is masked (e.g., `[EMAIL]`, `[PHONE]`) before reaching the LLM or being displayed on the dashboard.
**Handling Strategy:** Use regex patterns and NLP tools (like Microsoft Presidio) during the cleaning phase to replace sensitive tokens.
**Validation Approach:** Send a string containing fake phone numbers and emails; assert the output contains masked placeholders.

## 3. AI Processing & LLM Integration

### Hallucinated AI Insights
**Scenario:** The LLM extracts a pain point or barrier that was never mentioned in the text (e.g., claims the user complained about "shipping" when the text only mentions "size").
**Expected Behavior:** The AI must not invent unsupported information.
**Handling Strategy:** Use strict prompt engineering instructing the LLM to return `null` if a signal is absent. Require the LLM to output the exact quote it used to derive the signal.
**Validation Approach:** Manually review a sample of extracted signals against the raw text. Implement automated tests evaluating LLM output against deterministic baseline cases.

### Invalid Structured LLM Responses
**Scenario:** The LLM returns malformed JSON, missing required keys, or outputs conversational text instead of a JSON object.
**Expected Behavior:** The system recovers, retries the prompt, and skips if it repeatedly fails.
**Handling Strategy:** Use tools like OpenAI's JSON mode or function calling. Wrap LLM calls in Pydantic validation. If a `ValidationError` occurs, retry up to 3 times with a prompt appending the error message.
**Validation Approach:** Mock the LLM to return invalid JSON and verify the retry logic and fallback behavior.

### AI Rate Limits and API Timeouts
**Scenario:** The LLM API provider (e.g., OpenAI, Anthropic) hits a rate limit or times out.
**Expected Behavior:** The pipeline pauses and retries without losing the batch of data.
**Handling Strategy:** Implement exponential backoff for 429s and 5xx errors. Implement checkpointing so that if a batch fails, the pipeline can resume from the last successful record.
**Validation Approach:** Mock the LLM provider to throw 429 exceptions and verify the backoff and checkpoint logic.

### Partial Processing Failures
**Scenario:** A batch of 100 reviews is sent to the AI engine; 99 succeed but 1 fails due to sequence length or weird encoding.
**Expected Behavior:** The 99 successful records are saved, and the 1 failure is logged and skipped.
**Handling Strategy:** Process records individually or handle batch failures by dividing and conquering. Wrap individual record extraction in try-catch blocks.
**Validation Approach:** Inject a known "poison pill" record into a batch and ensure the rest of the batch processes successfully.

## 4. Analysis & Aggregation

### Theme Clustering: Meaningless or Duplicate Themes
**Scenario:** The clustering algorithm creates themes that are either too generic (e.g., "Clothes") or duplicates (e.g., "Too small" and "Runs small").
**Expected Behavior:** Themes are distinct, meaningful, and limited to 8-12 major categories.
**Handling Strategy:** Implement a secondary LLM pass to review the candidate clusters, merge semantically identical themes, and filter out overly generic labels.
**Validation Approach:** Pass a synthetic dataset with obvious duplicates and assert the system successfully merges them.

### Source Bias
**Scenario:** One source (e.g., Google Play) contributes 90% of the data, skewing the theme discovery to app-related bugs rather than fashion pain points.
**Expected Behavior:** The system prevents one source from completely drowning out others in theme prioritization.
**Handling Strategy:** When scoring opportunities, include `cross_source_consistency` as a metric. Track and visualize the breakdown of sources per theme on the dashboard.
**Validation Approach:** Generate a heavily skewed dataset and verify that the scoring algorithm still ranks cross-source opportunities fairly.

### Opportunity Scoring
**Scenario:** An opportunity is identified but has very low frequency, resulting in a skewed or zero score.
**Expected Behavior:** The scoring algorithm gracefully handles low-frequency opportunities without division-by-zero errors and ranks them appropriately low.
**Handling Strategy:** Ensure the mathematical formula for scoring includes safe division and normalizes inputs.
**Validation Approach:** Write unit tests for the scoring function with edge-case inputs (e.g., 0 frequency, 0 user pain).

### Missing Evidence
**Scenario:** The frontend requests the supporting quotes for a specific opportunity, but the links to the original `NormalizedFeedback` are broken or empty.
**Expected Behavior:** The dashboard handles the empty state gracefully and indicates no direct quotes are available, rather than crashing.
**Handling Strategy:** Ensure the database relies on foreign key constraints for traceability. In the API, return an empty array `[]` instead of throwing a 500 error if evidence is missing.
**Validation Approach:** Query the evidence endpoint for a synthetic opportunity with no mapped feedback and verify the 200 OK `[]` response.

## 5. Deployment

### Deployment Failures
**Scenario:** The FastAPI backend fails to start on Railway, or Next.js fails to build on Vercel due to environment variable misconfigurations.
**Expected Behavior:** Deployments roll back to the last stable version, and clear logs are emitted.
**Handling Strategy:** Enforce CI/CD pipeline checks (build steps, unit tests, linting) before allowing deployments. Validate essential environment variables (e.g., DB URLs, LLM API keys) on application startup and fail fast with descriptive errors.
**Validation Approach:** Remove a required environment variable in a staging environment and verify the app fails fast with a clear error message.
