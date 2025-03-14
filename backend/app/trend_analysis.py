from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from pygooglenews import GoogleNews
import logging
import nltk
import spacy
import yake
import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64

nltk.download("stopwords")
nltk.download("punkt")

nlp = spacy.load("en_core_web_sm")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Google News Trends API with Visuals")

class Article(BaseModel):
    title: str
    link: str
    published: str
    source: str
    summary: str

class NewsResponse(BaseModel):
    feed_title: str
    articles: List[Article]
    trending_keywords: List[str]
    wordcloud: Optional[str] 

LANGUAGES = ["en", "hi", "es", "fr", "uk", "ja"]
COUNTRIES = ["WORLD", "US", "IN", "GB", "MX", "UA", "JP"]

def extract_keywords(text: str, num_keywords=10) -> List[str]:
    """Extracts keywords using YAKE"""
    kw_extractor = yake.KeywordExtractor(n=1, top=num_keywords)
    keywords = kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

def generate_summary(text: str) -> str:
    """Generate a clean one-liner summary from the article"""
    if not text:
        return "No summary available."

    text = re.sub(r'<.*?>', '', text)
    sentences = re.split(r'(?<=[.!?]) +', text)  # Splits by ". ", "! ", or "? "
    return sentences[0] if sentences else "No summary available."

def generate_wordcloud(keywords: List[str]) -> str:
    """Generate a word cloud and return base64 string"""
    wordcloud = WordCloud(width=400, height=200, background_color="white").generate(" ".join(keywords))
    
    img_io = io.BytesIO()
    plt.figure(figsize=(5, 2))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(img_io, format="png", bbox_inches="tight")
    plt.close()
    
    img_base64 = base64.b64encode(img_io.getvalue()).decode()
    return f"data:image/png;base64,{img_base64}"



@app.get("/")
def read_root():
    return {"Hello": "Trend_Analysis"}

@app.get("/fetch_trends", response_model=NewsResponse)
def fetch_trends(
    lang: Optional[str] = Query(default="en", description="Language code (e.g., 'en', 'hi')"),
    country: Optional[str] = Query(default="WORLD", description="Country code (e.g., 'US', 'IN', 'WORLD')"),
    limit: int = Query(10, ge=1, le=50, description="Number of articles to return")
):
    """Fetches trending news with keyword analysis and visualization"""
    try:
        effective_country = country if country and country.upper() == "WORLD" else country
        default_lang = lang if lang else "en"
        
        logger.info(f"Fetching trends with lang={default_lang}, country={effective_country}, limit={limit}")
        
        gn = GoogleNews(lang=default_lang, country=effective_country)
        news_feed = gn.topic_headlines("WORLD") if country and country.upper() == "WORLD" else gn.top_news()
        
        articles_data = news_feed["entries"][:limit]
        
        all_text = " ".join(entry["title"] + " " + entry.get("summary", "") for entry in articles_data)
        keywords = extract_keywords(all_text, num_keywords=10)
        wordcloud_img = generate_wordcloud(keywords)

        articles = [
            Article(
                title=entry["title"],
                link=entry["link"],
                published=entry["published"],
                source=entry["source"]["title"],
                summary=generate_summary(entry.get("summary", entry["title"]))  # Clean one-liner summary
            ) for entry in articles_data
        ]
        
        return NewsResponse(
            feed_title=news_feed["feed"].title,
            articles=articles,
            trending_keywords=keywords,
            wordcloud=wordcloud_img
        )
    except Exception as e:
        logger.error(f"Error fetching trends: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.get("/trend_analysis")
def trend_analysis():
    """Endpoint to visualize current trending topics"""
    try:
        gn = GoogleNews(lang="en", country="US")
        news_feed = gn.top_news()

        all_text = " ".join(entry["title"] for entry in news_feed["entries"])
        keywords = extract_keywords(all_text, num_keywords=15)
        wordcloud_img = generate_wordcloud(keywords)

        return {
            "message": "Current trending topics analysis",
            "trending_keywords": keywords,
            "wordcloud": wordcloud_img
        }
    except Exception as e:
        logger.error(f"Error fetching trend analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating trend analysis: {str(e)}")

from fastapi.responses import Response
from collections import Counter

@app.get("/trending_chart")
def run_trending_chart():
    """Generates a bar chart of trending keywords"""
    try:
        gn = GoogleNews(lang="en", country="US")
        news_feed = gn.top_news()

        all_text = " ".join(entry["title"] for entry in news_feed["entries"])
        keywords = extract_keywords(all_text, num_keywords=10)

        keyword_counts = Counter(keywords)

        labels, values = zip(*keyword_counts.items())

        plt.figure(figsize=(10, 5))
        plt.barh(labels, values, color="skyblue")
        plt.xlabel("Frequency")
        plt.ylabel("Trending Keywords")
        plt.title("Trending News Keywords")
        plt.gca().invert_yaxis()  

        img_io = io.BytesIO()
        plt.savefig(img_io, format="png", bbox_inches="tight")
        plt.close()

        img_io.seek(0)
        return Response(content=img_io.getvalue(), media_type="image/png")

    except Exception as e:
        logger.error(f"Error generating trending chart: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating trending chart")
