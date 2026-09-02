# Fashion Engine: AI-Powered Wishlist Discovery

A production-ready data pipeline and dashboard built to understand e-commerce wishlist behavior.

## 1. Problem
In fashion e-commerce, millions of items are wishlisted daily, yet a significant portion never converts to a purchase within a 30-day window. Traditional quantitative analytics show *what* users are doing (drop-off rates, click-through rates), but fail to answer *why* users add items to a wishlist and ultimately abandon them.

## 2. Why the Discovery Engine was built
The Discovery Engine was built to bridge this gap by transforming massive volumes of unstructured, qualitative user feedback into actionable, structured product opportunities. Rather than relying on gut feelings, this engine uses AI to programmatically identify if a wishlist action is genuine purchase intent or merely bookmarking, and uncovers the precise friction points preventing conversion.

## 3. Data Sources
The engine extracts and processes organic user feedback from public channels:
- **Google Play Store Reviews:** Analyzed for UI friction, app performance, and immediate post-purchase/post-wishlist feedback.
- **Reddit (Coming Soon):** Deep-dive community discussions regarding product quality and brand perception.
- **YouTube (Coming Soon):** External research behaviors and influencer-driven comparison metrics.

## 4. Architecture
The architecture is divided into three core micro-environments:
- **Data Pipeline (Python):** Ingests, normalizes, and extracts AI signals using Google Gemini.
- **Backend API (FastAPI):** Serves the aggregated data via heavily validated, paginated REST endpoints.
- **Frontend Dashboard (Next.js):** A premium, interactive UI designed to visualize the analytical findings for product managers and stakeholders.

## 5. AI Analysis Pipeline
Raw data undergoes a rigorous multi-phase pipeline:
1. **Ingestion:** Data is securely fetched and stored in a local SQLite database (`raw_reviews.db`).
2. **Cleaning & Normalization:** Spam is removed, and all Personally Identifiable Information (PII) is cryptographically masked via RegEx to ensure privacy compliance.
3. **LLM Extraction:** Google Gemini is bound by strict Pydantic `enum` schemas to extract 10+ specific signals per review (e.g., `shopping_intent`, `pain_point`, `comparison_behavior`) while rejecting hallucinations.

## 6. Theme Discovery
Using a mathematical approach (TF-IDF Vectorization paired with Agglomerative Clustering), the engine groups semantically similar feedback into recurring themes (e.g., "Service Quality", "UI Navigation"). This ensures themes are driven by statistical frequency, not manual bias.

## 7. Wishlist Behavior Analysis
The engine programmatically separates "Wishlist as a Bookmark" from "Wishlist as Purchase Intent" by analyzing intent keywords within the feedback, allowing product teams to target these segments differently.

## 8. Purchase Barrier Analysis
The system aggregates the exact pain points (e.g., "Expensive pricing", "Poor app performance") that users explicitly cite as reasons for postponing or abandoning a purchase, mapping them to specific user demographic segments.

## 9. Opportunity Scoring
Potential product enhancements are ranked using a transparent 1-5 scoring matrix based on:
- **Purchase Impact:** How directly solving the problem leads to a sale.
- **Wishlist Relevance:** How closely the issue is tied to the wishlist funnel.
- **User Pain:** The severity of the friction.

## 10. Technology Stack
- **AI/LLM:** Google Gemini API
- **Data Processing:** Python, Scikit-learn, SQLite/PostgreSQL
- **Backend Server:** FastAPI, SQLAlchemy, Uvicorn
- **Frontend:** Next.js (React), Vanilla CSS (Glassmorphism design)
- **Deployment:** Railway

## 11. Local Setup
1. Clone the repository: `git clone https://github.com/sibaniacharya/fashion-engine.git`
2. Install Backend dependencies: `cd backend && pip install -r requirements.txt`
3. Install Frontend dependencies: `cd frontend && npm install`

## 12. Environment Variables
Create a `.env` file in the `backend/` directory:
```env
GEMINI_API_KEY="your_api_key_here"
# Optional (falls back to local SQLite if omitted)
DATABASE_URL="postgresql://user:password@localhost:5432/db"
FRONTEND_URL="http://localhost:3000"
```

## 13. Running the Pipeline
Navigate to `backend/` and execute the phases sequentially:
```bash
python scripts/run_phase3.py # AI Extraction
python scripts/run_phase4.py # Theme Discovery
python scripts/run_phase5.py # Behavior Analysis
python scripts/run_phase6.py # Opportunity Scoring
```

## 14. Running the Backend
From the `backend/` directory, start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```
API Documentation available at: `http://localhost:8000/docs`

## 15. Running the Frontend
From the `frontend/` directory, start the Next.js dev server:
```bash
npm run dev
```
Navigate to `http://localhost:3000` to view the Discovery Dashboard.

## 16. Deployment
The repository is production-ready for Railway deployment.
1. Connect your GitHub repository to a new Railway project.
2. Railway will automatically detect the `railway.toml` and build the backend.
3. Deploy the Next.js frontend as a separate Vercel or Railway service.
4. Set the necessary environment variables in the cloud dashboards.

## 17. Limitations
- **API Limits:** Free-tier LLM limits severely throttle ingestion speeds. The pipeline implements SQLite checkpointing and Tenacity exponential backoff to gracefully handle HTTP 429 Rate Limits, but bulk processing requires a paid tier.
- **Source Expansion:** Currently, only the Google Play ingestion adapter is fully active. Reddit and YouTube require external API credentials and heavier quota allowances to function at scale.

## 18. Production URLs
- **Live Dashboard:** *(To be added post-deployment)*
- **Live API:** *(To be added post-deployment)*
- **Repository:** https://github.com/sibaniacharya/fashion-engine

## 19. Documentation & Reports
- **Part 1 Final Report:** [docs/part1-final-report-for-part2.md](docs/part1-final-report-for-part2.md) - Synthesizes the final canonical outputs from the Part 1 Discovery Engine.
- **Part 2 Metric Decomposition:** [docs/part2-metric-decomposition.md](docs/part2-metric-decomposition.md) - Defines the Wishlist → Purchase conversion funnel and prioritizes opportunities for validation.
