# Google News API - Trend Analysis

A simple Google News trend explorer built with:
- **FastAPI** backend for fetching Google News headlines and topic searches.
- **Streamlit** UI for interactive browsing.
- **pygooglenews** as the Google News feed client.

There is also an optional **trend analysis** module that can extract keywords and generate wordclouds/bar charts.

## Features
- Top news by region or **WORLD** (global)
- Topic-based news search
- One-click “update trends” endpoint
- Streamlit UI to browse results
- Optional keyword extraction + wordcloud generation

## Project Structure
- `backend/app/main.py` FastAPI app (core API)
- `backend/app/app.py` Streamlit UI
- `backend/app/trend_analysis.py` Extended API with NLP + visuals (optional)
- `googleapi.py` Simple CLI script for quick tests
- `backend/Dockerfile` Placeholder (currently empty)
- `backend/pyproject.toml` Placeholder (currently empty)

## Requirements
Core dependencies (from imports in the code):
- `fastapi`
- `uvicorn`
- `pygooglenews`
- `streamlit`
- `requests`

Optional for trend analysis (`backend/app/trend_analysis.py`):
- `nltk`
- `spacy`
- `yake`
- `sumy`
- `matplotlib`
- `wordcloud`

## Setup
Create and activate a virtual environment, then install dependencies:

```bash
pip install fastapi uvicorn[standard] pygooglenews streamlit requests
```

If you want the trend analysis module:

```bash
pip install nltk spacy yake sumy matplotlib wordcloud
python -m spacy download en_core_web_sm
```

## Run the API
From the project root:

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Run the Streamlit UI
In a second terminal:

```bash
streamlit run backend/app/app.py
```

The UI will open in your browser and talk to the FastAPI server.

## API Endpoints (FastAPI)
- `GET /` Health check
- `GET /fetch_trends?lang=en&country=US&limit=10`
- `GET /fetch_trends/{topic_name}?lang=en&country=US&limit=10`
- `GET /update_trends?lang=en&country=US`

Valid languages: `en, hi, es, fr, uk, ja`  
Valid countries: `WORLD, US, IN, GB, MX, UA, JP`

## Optional: Trend Analysis API
If you want the extended endpoints, run:

```bash
uvicorn backend.app.trend_analysis:app --reload
```

Extra endpoints:
- `GET /trend_analysis` Returns trending keywords + wordcloud (base64 image)
- `GET /trending_chart` Returns a PNG chart of keyword frequencies

## Notes
- The Dockerfile and `pyproject.toml` are currently empty placeholders.
- `backend/app/trend_analysis.py` downloads NLTK resources on startup.
