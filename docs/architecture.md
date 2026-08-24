# AI-Powered Discovery Engine Architecture

## 1. Overall System Architecture
The AI-Powered Discovery Engine is designed to ingest, process, and analyze public feedback related to online fashion shopping. The system aims to surface evidence-backed opportunity areas to improve wishlist-to-purchase conversions.

**Core Components:**
- **Data Ingestion Layer**: Modular adapters fetching data from public sources.
- **Data Processing Pipeline**: Cleaning, normalization, and PII masking.
- **AI Engine**: Signal extraction, theme discovery, and analysis modules leveraging LLMs.
- **Storage Layer**: PostgreSQL-ready architecture for raw data, normalized data, and analysis results.
- **Backend API**: Python FastAPI backend serving insights and handling orchestration.
- **Frontend Dashboard**: React/Next.js dashboard for visualizing insights.

## 2. Data Sources
The system will draw from publicly available conversations and feedback, strictly adhering to terms of service, avoiding authentication bypass, and prioritizing legally/technically accessible data.

**Primary Sources:**
- Google Play reviews
- Reddit discussions
- YouTube comments
- Public fashion/product reviews and Q&A

**Future Extensions:**
- App Store reviews (where permitted)
- Social media conversations
- Fashion and shopping communities

## 3. Data Ingestion
The ingestion architecture must be modular, allowing for independent adapters per source.

**Ingestion Adapters:**
- **Google Play Adapter**: Fetches app reviews.
- **Reddit Adapter**: Uses public APIs to fetch subreddit discussions and comments.
- **YouTube Adapter**: Fetches comments from specific fashion review videos.
- **General Scraper/API Adapter**: For public Q&A and reviews.

**Normalized Schema:**
All incoming records are mapped to a common schema:
- `internal_id` (UUID)
- `source` (Enum)
- `source_id` (String)
- `date` (Timestamp)
- `title` (String)
- `text` (Text)
- `rating` (Integer/Float)
- `URL` (String)
- `category` (String)
- `metadata` (JSONB)

## 4. Data Storage
A relational database architecture, designed to be PostgreSQL-ready, will support the pipeline.

**Core Tables:**
- **Raw Feedback**: Stores unaltered ingested data.
- **Normalized Feedback**: Stores cleaned, PII-masked, and language-detected data.
- **Extracted Signals**: Stores AI-generated signals linked to feedback.
- **Themes & Clusters**: Stores discovered themes and evidence links.
- **Opportunities**: Stores scored opportunities and metadata.

## 5. Data Cleaning and Normalization
A critical pipeline to ensure data quality without losing valuable short-form context.

**Pipeline Steps:**
1. **Deduplication**: Remove exact duplicates and detect near-duplicates.
2. **Filtering**: Remove empty records, spam, and irrelevant content.
3. **Formatting**: Normalize whitespace and metadata.
4. **Language Detection**: Identify and tag the language of the feedback. (Non-English is not discarded silently but recorded).
5. **PII Removal**: Mask Personally Identifiable Information while preserving original text meaning.

*Note: Reviews with fewer than 8 words or those containing meaningful emojis are NOT automatically removed, as short queries (e.g., "Should I size up?") carry strong purchase signals.*

## 6. AI Signal Extraction
This module uses LLMs (with provider abstraction) to extract structured insights from normalized text. The AI must not invent unsupported information and must preserve evidence traceability.

**Extracted Signals include:**
- User segment, Shopping intent, Wishlist intent, Purchase stage
- Pain points, Uncertainties, Purchase barriers
- Information sought, Comparison behaviors
- Specific signals: Fit/size, styling, price, quality, occasion, social validation
- External research behavior and evidence strength

## 7. Theme Discovery
Instead of hardcoding categories, the AI engine will dynamically discover 8–12 recurring themes.

**Process:**
- Identify recurring patterns in extracted signals and raw text.
- Cluster semantically similar feedback.
- Generate candidate themes and merge similar ones.
- Calculate frequency and percentage representation.
- Compare themes across different sources and user segments.
- Retain exact evidence supporting each theme.

## 8. Wishlist Behavior Analysis
Analyzes the shopping journey from discovery to purchase or abandonment.

**Categorization of Wishlist Usage:**
- Genuine purchase intent
- Active evaluation
- Future purchase intent
- Bookmarking
- Inspiration
- Wishlist followed by comparison, postponement, or abandonment

## 9. Purchase Barrier Analysis
Identifies explicit uncertainties preventing the transition from wishlist to purchase.

**Potential Barriers Identified:**
- Fit, size, styling, quality, or price uncertainty
- Lack of reviews or social validation
- Product comparison struggles
- Return/replacement policy uncertainties
- Wait for external validation or information

## 10. External Information-Seeking Analysis
Identifies out-of-platform actions taken by users before purchasing.

**Analyzed Behaviors:**
- Searching Google, checking Instagram, watching YouTube
- Reading Reddit, asking friends, seeking influencer content
*Classification strictly relies on evidence present in the text.*

## 11. Opportunity Identification and Scoring
Opportunities represent the intersection of a user problem, a behavioral barrier, and a potential product outcome.

**Opportunity Definition:**
`Opportunity = USER PROBLEM + BEHAVIORAL BARRIER + POTENTIAL PRODUCT OUTCOME`

**Programmatic Scoring Criteria:**
- Frequency
- Wishlist Relevance
- Potential Purchase Impact
- User Pain
- Cross-source Consistency
- Evidence Confidence

**Opportunity Output Format:**
Includes opportunity name, problem statement, affected segments, frequency, score, supporting evidence (quotes), and key uncertainties.

## 12. Backend APIs
Built using **Python, FastAPI**, and **Pydantic** to handle requests and orchestrate the AI pipeline.

**Core Responsibilities:**
- Trigger ingestion and cleaning pipelines.
- Manage LLM integrations (structured output, JSON validation, retries, rate limits).
- Manage pipeline state (checkpointing and resume capability).
- Serve aggregated insights and evidence to the frontend dashboard.

## 13. Frontend Dashboard
A **React / Next.js** application serving as the interface for the Product Manager.

**Dashboard Features:**
- Visualizations of what users care about and why they wishlist products.
- Purchase barrier breakdown and segment comparisons.
- Theme prevalence and external information-seeking trends.
- **Opportunity Hub:** A ranked list of promising opportunity areas with direct links to supporting evidence.

## 14. Deployment Architecture
The deployment strategy leverages modern PaaS providers for simplicity and scalability.

- **Backend / API / Processing Workers:** Deployed on **Railway**.
- **Frontend Dashboard:** Deployed on **Vercel**.
- **Database:** Managed PostgreSQL instance (hosted on Railway or a dedicated provider).
