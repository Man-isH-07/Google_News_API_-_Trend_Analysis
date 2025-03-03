from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from pygooglenews import GoogleNews
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Google News Trends API with World Option")

class Article(BaseModel):
    title: str
    link: str
    published: str
    source: str

class NewsResponse(BaseModel):
    feed_title: str
    articles: List[Article]

LANGUAGES = ["en", "hi", "es", "fr", "uk", "ja"]
COUNTRIES = ["WORLD", "US", "IN", "GB", "MX", "UA", "JP"]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/fetch_trends", response_model=NewsResponse)
def fetch_trends(
    lang: Optional[str] = Query(None, description="Language code (e.g., 'en', 'hi')", regex="^(en|hi|es|fr|uk|ja)$"),
    country: Optional[str] = Query(None, description="Country code (e.g., 'US', 'IN', 'WORLD')", regex="^(WORLD|US|IN|GB|MX|UA|JP)$"),
    limit: int = Query(10, ge=1, le=50, description="Number of articles to return")
):
    """Fetches the latest trends, using 'WORLD' for global news or specific region otherwise."""
    try:
        effective_country = country if country and country.upper() == "WORLD" else country
        default_lang = lang if lang else "en"
        
        logger.info(f"Fetching trends with lang={default_lang}, country={effective_country}, limit={limit}")
        
        gn = GoogleNews(lang=default_lang, country=effective_country)
        if country and country.upper() == "WORLD":
            news_feed = gn.topic_headlines("WORLD")
        else:
            news_feed = gn.top_news()
        
        articles = [
            Article(
                title=entry["title"],
                link=entry["link"],
                published=entry["published"],
                source=entry["source"]["title"]
            ) for entry in news_feed["entries"][:limit]
        ]
        return NewsResponse(
            feed_title=news_feed["feed"].title,
            articles=articles
        )
    except Exception as e:
        logger.error(f"Error fetching trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.get("/fetch_trends/{topic_name}", response_model=NewsResponse)
def fetch_trends_by_topic(
    topic_name: str,
    lang: Optional[str] = Query(None, description="Language code (e.g., 'en', 'hi')", regex="^(en|hi|es|fr|uk|ja)$"),
    country: Optional[str] = Query(None, description="Country code (e.g., 'US', 'IN', 'WORLD')", regex="^(WORLD|US|IN|GB|MX|UA|JP)$"),
    limit: int = Query(10, ge=1, le=50, description="Number of articles to return")
):
    """Fetches trends for a topic, using 'WORLD' for global context or specific region otherwise."""
    try:
        effective_country = country if country and country.upper() == "WORLD" else country
        default_lang = lang if lang else "en"
        
        logger.info(f"Fetching trends for topic '{topic_name}' with lang={default_lang}, country={effective_country}, limit={limit}")
        
        gn = GoogleNews(lang=default_lang, country=effective_country)
        search_results = gn.search(query=topic_name)
        articles = [
            Article(
                title=entry["title"],
                link=entry["link"],
                published=entry["published"],
                source=entry["source"]["title"]
            ) for entry in search_results["entries"][:limit]
        ]
        return NewsResponse(
            feed_title=search_results["feed"].title,
            articles=articles
        )
    except Exception as e:
        logger.error(f"Error fetching topic trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.get("/update_trends")
def update_trends(
    lang: Optional[str] = Query(None, description="Language code (e.g., 'en', 'hi')", regex="^(en|hi|es|fr|uk|ja)$"),
    country: Optional[str] = Query(None, description="Country code (e.g., 'US', 'IN', 'WORLD')", regex="^(WORLD|US|IN|GB|MX|UA|JP)$")
):
    """Simulates updating trends, using 'WORLD' for global news or specific region otherwise."""
    try:
        effective_country = country if country and country.upper() == "WORLD" else country
        default_lang = lang if lang else "en"
        
        logger.info(f"Updating trends with lang={default_lang}, country={effective_country}")
        
        gn = GoogleNews(lang=default_lang, country=effective_country)
        if country and country.upper() == "WORLD":
            news_feed = gn.topic_headlines("WORLD")
        else:
            news_feed = gn.top_news()
        return {"message": "Trends updated", "feed_title": news_feed["feed"].title}
    except Exception as e:
        logger.error(f"Error updating trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating trends: {str(e)}")