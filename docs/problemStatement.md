# Graduation Project — AI-Powered Wishlist Discovery Engine

## Product
**Chosen product:** Myntra  
**Role:** Product Manager on the Growth Team at Myntra.

## Business Context
Millions of users browse fashion products, save products they like, and add products to their wishlists. A wishlist represents an important user signal because the user has explicitly expressed interest in a product but has not yet purchased it. Over time, users can accumulate dozens or hundreds of wishlisted products, while only a small proportion may eventually result in purchases.

**Strategic Goal:** Increase the percentage of users who purchase at least one item from their wishlist within 30 days of adding it.

Improving wishlist-to-purchase conversion could:
- Increase purchase frequency
- Improve monetization from existing users
- Increase the value generated from existing high-intent demand

**Important Constraint:** The final product solution cannot offer monetary incentives to users.
*Note: The underlying user problem is NOT provided. The objective is to discover the underlying problem through research and evidence.*

---

## Part 1 — AI-Powered Discovery Engine

Before proposing any product solution, build an AI-powered Discovery Engine that analyzes user feedback at scale. The Discovery Engine should analyze publicly available conversations and feedback related to online fashion shopping.

### Potential Sources
- App Store reviews
- Google Play reviews
- Reddit discussions
- Fashion and shopping communities
- Social media conversations
- YouTube comments
- Product reviews
- Product Q&A
- Other publicly available conversations about online fashion shopping

*Note: The system does NOT need to use every possible source. The architecture should support multiple sources, but the initial implementation should prioritize sources that are legally and technically accessible and provide useful evidence.*

**Constraints:**
- Do not fabricate data.
- Do not scrape behind authentication.
- Do not bypass CAPTCHA, WAF, login restrictions, or Terms of Service.
- Use legitimate public APIs, exports, datasets, or permitted public access methods.

### Discovery Questions
The Discovery Engine should help answer:
1. Why do users add fashion products to their wishlist?
2. What prevents wishlisted products from eventually being purchased?
3. What uncertainties remain after users have identified a product they like?
4. What causes users to postpone a purchase?
5. How do users compare multiple shortlisted products?
6. What information do users seek outside Myntra before purchasing?
7. What role do the following factors play: fit, size, styling, price, reviews, quality, occasion, social validation?
8. When is the wishlist used as: genuine purchase intent, active evaluation, future purchase intent, bookmarking, inspiration?
9. How do these behaviors differ across user segments?
10. What unmet needs appear consistently across user conversations?
11. What purchase barriers appear repeatedly?
12. What information is missing at the point where users decide whether to purchase?
13. What workarounds do users currently use?
14. What happens outside the Myntra app before users make their final purchase decision?

### Discovery Engine Objective
The system must go beyond simple review summarization, sentiment analysis, star-rating analysis, and keyword frequency.
It should identify, quantify where possible, compare, and prioritize potential opportunity areas that could influence wishlist-to-purchase conversion.

### Expected Discovery Pipeline
Public Feedback Sources → Data Ingestion → Raw Feedback Storage → Cleaning & Normalization → PII Removal → Language Detection → AI Signal Extraction → Theme Discovery → Wishlist Behavior Analysis → Purchase Barrier Analysis → External Information-Seeking Analysis → User Segment Comparison → Opportunity Identification → Opportunity Scoring → Opportunity Ranking → Discovery Dashboard

---

## Technical Specifications & Architecture

### Data Ingestion
Modular ingestion architecture allowing independent adapters for different sources (Google Play reviews, Reddit, YouTube comments, Public fashion/product reviews and Q&A).
Normalize records into a common schema: `internal_id`, `source`, `source_id`, `date`, `title`, `text`, `rating`, `URL`, `category`, `metadata`.

### Data Cleaning
- Remove exact duplicates and detect near duplicates where practical.
- Remove empty records, identify spam, and identify irrelevant content.
- Detect language, normalize whitespace and metadata.
- Remove or mask PII.
- Preserve original text and source provenance.

**Important Data Cleaning Constraints:**
- Do NOT automatically remove all reviews with fewer than 8 words (meaningful short feedback must be retained).
- Do NOT remove meaningful text merely because it contains emojis.
- Do not silently discard non-English feedback (detect and record language).

### AI Signal Extraction
Identify signals where supported by actual text:
- `user_segment`, `shopping_intent`, `wishlist_intent`, `purchase_stage`, `pain_point`, `uncertainty`, `purchase_barrier`, `information_sought`, `comparison_behavior`
- Specific signals: `fit_size_signal`, `styling_signal`, `price_signal`, `quality_signal`, `review_social_validation_signal`, `occasion_signal`
- `external_research_behavior`, `theme_candidate`, `evidence_strength`
*The AI must not invent unsupported information.*

### Theme Discovery
Themes should be discovered from the data (approx. 8–12 themes generated before prioritization) rather than hard-coded. Identify patterns, cluster similar feedback, generate candidate themes, and compare across sources/segments.

### Analysis Modules
- **Wishlist Behavior Analysis:** Distinguish between genuine purchase intent, active evaluation, future purchase intent, bookmarking, inspiration, comparison, postponement, and abandonment.
- **Purchase Barrier Analysis:** Identify barriers preventing the move from wishlist to purchase (e.g., fit/size/quality uncertainty, lack of reviews/validation, product comparison).
- **External Information Seeking:** Identify what users do outside the platform before purchasing (e.g., searching Google, checking Instagram/YouTube, comparing products). Evidence-based classification only.
- **User Segmentation:** Identify segments (students, professionals, budget-conscious, trend-driven, etc.) and compare behaviors across them.

### Opportunity Identification
Identify opportunity areas related to **Wishlist → Purchase within 30 days**.
Formula: `Opportunity = USER PROBLEM + BEHAVIORAL BARRIER + POTENTIAL PRODUCT OUTCOME` (Do NOT directly turn an opportunity into a product solution).

Evaluate opportunities via programmatic scoring on: frequency, wishlist relevance, potential purchase impact, user pain, cross-source consistency, evidence confidence.

Include for each opportunity: `opportunity_name`, `problem_statement`, `affected_segments`, `journey_stage`, `frequency`, `wishlist_relevance`, `purchase_impact`, `user_pain`, `cross_source_consistency`, `evidence_confidence`, `opportunity_score`, `supporting_evidence`, `key_uncertainty`.

### Evidence Requirements
- Must be evidence-based.
- Do not fabricate reviews, quotes, statistics, themes, user behaviors, or segments.
- All quotes must be actual user-generated text with PII removed.

---

## Technical Stack & Output

### Tech Stack
- **Backend:** Python, FastAPI, Pydantic, Modular architecture. Deployed on **Railway**.
- **Frontend:** React / Next.js. Deployed on **Vercel**.
- **Storage:** PostgreSQL-ready architecture.
- **AI Integration:** LLM provider abstraction, structured output, JSON validation, retry/rate-limit handling, checkpointing, resume capability.

### Expected Output
A Discovery Dashboard that allows a Product Manager to understand:
1. What users care about.
2. Why users wishlist products.
3. Which wishlist behaviors indicate genuine purchase intent.
4. Why users postpone or abandon purchases.
5. What uncertainties users have.
6. What information users seek.
7. How behavior differs across segments.
8. What themes appear repeatedly.
9. Which purchase barriers are strongest.
10. Which opportunity areas appear most promising.
11. What evidence supports each opportunity.

### Part 1 Boundary
**Output of Part 1:** "Evidence-backed opportunity areas that could influence wishlist-to-purchase conversion."
*Note: Do NOT implement business metric decomposition, user interviews, final product solution, MVP, etc., during this stage.*
