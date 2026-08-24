# Backend Deployment Plan (Railway)

This document outlines the strategy for deploying the FastAPI backend to a production Railway environment while adhering strictly to security best practices and project constraints.

## 1. Infrastructure Configuration
- **Railway Config:** We will implement a `railway.toml` specifying the startup command and builder for the web service.
- **Startup Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Dependencies:** We will generate a strict `requirements.txt` listing `fastapi`, `uvicorn`, `sqlalchemy`, `google-genai`, `scikit-learn`, `psycopg2-binary`, etc.

## 2. Environment Variables & Secrets Management
All sensitive credentials will be injected via Railway's dashboard (no `.env` files will be committed to the repo). Required variables:
- `GEMINI_API_KEY`: Required for LLM extraction pipelines.
- `DATABASE_URL`: PostgreSQL connection string provided by Railway.
- `FRONTEND_URL`: For secure CORS mapping.

## 3. Database & Persistence Strategy
Currently, the app relies on a local `discovery_engine.db` SQLite file. 
- **Change:** We will modify `backend/database.py` to read `DATABASE_URL` from the environment. If present (production), it will connect to a Railway PostgreSQL database. If missing (local), it will safely fallback to the existing `sqlite:///./discovery_engine.db`.
- **Note on JSON Artifacts:** Currently, analytical data is saved as flat JSON files in `/data/analyzed`. Railway's ephemeral file system resets on deployment unless a persistent volume is mounted. The easiest approach is to mount a volume to `/app/data` in Railway settings to persist the JSON reports.

## 4. API Security & Logging
- **CORS:** Update `backend/main.py` to read `FRONTEND_URL` and restrict cross-origin requests to the production Next.js domain (falling back to `*` only if running locally).
- **Health Checks:** The existing `/api/health` endpoint will serve as the ping target for Railway's deployment health checks.
- **Production Logging:** Replace basic `print()` statements in `main.py` with standard Python `logging` to ensure logs are cleanly forwarded to the Railway observability dashboard.

## 5. Failure Handling
The existing `tenacity` retry loops and checkpointing logic natively protect against API rate-limiting and temporary database disconnects during deployment cycles.
