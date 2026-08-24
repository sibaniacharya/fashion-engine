# Phase-Wise Implementation Plan: AI-Powered Discovery Engine

This document outlines the detailed implementation plan for Part 1 of the AI-Powered Discovery Engine, divided into clear, independently testable phases.

## Phase 0: Project Foundation
**Objective:** Set up the core project infrastructure, repository structure, and development environment.
**Inputs:** Architecture Document, Problem Statement
**Implementation Tasks:**
- Initialize GitHub repository and set up version control.
- Set up Python backend project (FastAPI) and manage dependencies using `poetry` or `pip`.
- Set up frontend project (React/Next.js) with basic boilerplate.
- Configure PostgreSQL database locally or via Docker.
- Setup code quality tools (linting, formatting, pre-commit hooks).
**Outputs:** Working repository with base backend, frontend, and database configurations.
**Validation:** Both backend server and frontend dev server start successfully; database connection is established.
**Acceptance Criteria:** A developer can clone the repo, run setup commands, and start the local environment without errors.
**Dependencies:** None.

## Phase 1: Data Ingestion
**Objective:** Build modular data ingestion adapters to collect raw feedback from public sources.
**Inputs:** Public feedback sources (Google Play, Reddit, YouTube, etc.)
**Implementation Tasks:**
- Design and implement the base `IngestionAdapter` interface.
- Implement `GooglePlayAdapter` using public scraper libraries.
- Implement `RedditAdapter` utilizing public APIs.
- Implement `YouTubeAdapter` for comments on specific videos.
- Implement the `RawFeedback` database schema.
- Create ingestion scripts/endpoints to trigger data fetching and store results.
**Outputs:** Ingested raw feedback data stored in the database.
**Validation:** Run ingestion scripts and verify raw data appears in the database with correct schemas.
**Acceptance Criteria:** Data from at least two sources is successfully fetched and saved in the raw table without auth bypass.
**Dependencies:** Phase 0 (Database setup).

## Phase 2: Data Cleaning and Normalization
**Objective:** Process raw data to remove noise, deduplicate, detect language, and mask PII while preserving valuable context.
**Inputs:** Raw feedback records.
**Implementation Tasks:**
- Implement exact and near-duplicate detection.
- Implement filtering logic (empty records, spam detection, non-meaningful content). Ensure short (<8 words) but meaningful reviews are preserved.
- Integrate a language detection library (e.g., `langdetect` or `fasttext`).
- Implement PII masking using regex or NLP libraries (e.g., Presidio).
- Define and implement the `NormalizedFeedback` database schema.
**Outputs:** Cleaned, deduplicated, and PII-masked records in the `NormalizedFeedback` table.
**Validation:** Run the cleaning pipeline on a sample of raw data and manually inspect the output for PII leakage and retained short reviews.
**Acceptance Criteria:** Pipeline successfully transforms raw data into normalized data; PII is masked; meaningful short reviews and emojis are preserved.
**Dependencies:** Phase 1 (Raw data).

## Phase 3: AI Signal Extraction
**Objective:** Extract structured intent, signals, and pain points from normalized text using LLMs.
**Inputs:** Normalized feedback records.
**Implementation Tasks:**
- Abstract the LLM provider interface.
- Design Pydantic schemas for structured output (user segments, shopping intent, pain points, specific signals).
- Implement the extraction pipeline with JSON validation, retry logic, and rate-limit handling.
- Process normalized records and store results in `ExtractedSignals` table.
**Outputs:** Structured signals for each processed feedback item.
**Validation:** Review a random sample of extracted signals against the original text to ensure no fabricated information.
**Acceptance Criteria:** LLM consistently returns structured JSON matching the Pydantic schema; extracted signals are strictly supported by the text.
**Dependencies:** Phase 2 (Normalized data).

## Phase 4: Theme Discovery
**Objective:** Dynamically identify and cluster recurring themes from the extracted signals and text.
**Inputs:** Extracted signals, Normalized text.
**Implementation Tasks:**
- Implement semantic clustering (e.g., embeddings + K-Means/HDBSCAN or LLM-driven topic modeling).
- Generate human-readable labels for candidate themes.
- Merge highly similar themes.
- Calculate theme frequency and map themes back to the supporting evidence (feedback IDs).
- Store themes in the `Themes` table.
**Outputs:** A list of 8-12 meaningful themes mapped to source feedback.
**Validation:** Verify that identified themes have high internal consistency and represent actual user pain points.
**Acceptance Criteria:** System dynamically generates 8-12 distinct themes with accurate links to source evidence.
**Dependencies:** Phase 3.

## Phase 5: Wishlist Behavior and Purchase Barrier Analysis
**Objective:** Analyze specific shopping journeys, wishlist intents, and purchase barriers.
**Inputs:** Extracted signals.
**Implementation Tasks:**
- Group data to differentiate wishlist intents (e.g., inspiration vs. active evaluation).
- Identify and quantify purchase barriers (e.g., fit uncertainty, price).
- Analyze external information-seeking behaviors (e.g., searching Google, checking YouTube).
- Compare these behaviors across different user segments.
**Outputs:** Aggregated metrics and insights on wishlist behaviors, barriers, and segments.
**Validation:** Ensure aggregated metrics correctly roll up from the underlying evidence without hallucinated behaviors.
**Acceptance Criteria:** Aggregated tables/views provide clear metrics on wishlist intents and purchase barriers with supporting evidence counts.
**Dependencies:** Phase 3.

## Phase 6: Opportunity Identification and Prioritization
**Objective:** Identify, score, and rank potential opportunity areas based on analyzed data.
**Inputs:** Themes, Wishlist Behaviors, Purchase Barriers.
**Implementation Tasks:**
- Define the programmatic scoring algorithm based on frequency, wishlist relevance, user pain, cross-source consistency, and evidence confidence.
- Generate Opportunity records combining `USER PROBLEM + BEHAVIORAL BARRIER + POTENTIAL PRODUCT OUTCOME`.
- Calculate scores and rank the opportunities.
- Store results in the `Opportunities` table.
**Outputs:** Ranked list of evidence-backed opportunities.
**Validation:** Verify the scoring logic programmatically matches the defined formula.
**Acceptance Criteria:** Opportunities are ranked systematically, and top opportunities have robust evidence links.
**Dependencies:** Phase 4, Phase 5.

## Phase 7: Backend APIs
**Objective:** Build RESTful APIs to expose the aggregated data and insights to the frontend.
**Inputs:** Processed data in database (Themes, Opportunities, Aggregated Analysis).
**Implementation Tasks:**
- Create endpoints for high-level metrics and segment comparisons.
- Create endpoints to fetch top themes and related evidence.
- Create endpoints for the Opportunity Hub (listing, ranking, and details).
- Include evidence traceability endpoints to fetch original quotes for any finding.
**Outputs:** Fully functional OpenAPI/Swagger documented FastAPI backend.
**Validation:** Call API endpoints using Swagger UI or Postman to verify JSON responses.
**Acceptance Criteria:** APIs return accurate, structured JSON data corresponding to the database records with sub-second latency for aggregated queries.
**Dependencies:** Phase 6.

## Phase 8: Frontend Dashboard
**Objective:** Develop the user interface for the Product Manager to explore the discovery insights.
**Inputs:** Backend APIs.
**Implementation Tasks:**
- Design and build dashboard layouts and navigation.
- Implement data visualization components (charts for themes, segments, and behaviors).
- Build the Opportunity Hub interface showing ranked opportunities and scores.
- Build the Evidence Viewer component to display masked quotes supporting the insights.
**Outputs:** Functional React/Next.js dashboard.
**Validation:** Navigate through the dashboard and verify visualizations match the API data.
**Acceptance Criteria:** Dashboard accurately visualizes insights, ranks opportunities, and allows clicking through to see supporting raw evidence.
**Dependencies:** Phase 7.

## Phase 9: End-to-End Validation
**Objective:** Ensure the entire pipeline works harmoniously from ingestion to visualization.
**Inputs:** Complete system.
**Implementation Tasks:**
- Trigger a fresh ingestion run from end-to-end.
- Monitor logs, data flow, API responses, and frontend updates.
- Verify traceability (finding an opportunity on the frontend and tracing it back to the raw source data).
**Outputs:** Validated, stable system.
**Validation:** Manual QA of the pipeline and UI.
**Acceptance Criteria:** Data flows seamlessly from ingestion to the dashboard without manual intervention; all evidence is traceable.
**Dependencies:** Phase 1-8.

## Phase 10: Deployment
**Objective:** Deploy the system to cloud infrastructure.
**Inputs:** Validated codebase, Environment variables.
**Implementation Tasks:**
- Set up PostgreSQL database on a managed provider.
- Deploy the FastAPI backend to Railway.
- Deploy the Next.js frontend to Vercel.
- Configure CORS, environment variables, and production database URLs.
**Outputs:** Live URLs for the dashboard and API.
**Validation:** Access the live dashboard URL and verify functionality.
**Acceptance Criteria:** Dashboard is accessible on the web, API responds correctly, and data pipelines run successfully in the cloud environment.
**Dependencies:** Phase 9.
