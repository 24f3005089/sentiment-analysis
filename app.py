from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ENABLE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

@app.get("/")
def home():
    return {"message": "Sentiment API running"}

@app.post("/sentiment")
def analyze_sentiment(data: SentimentRequest):

    happy_words = [
        "love", "great", "happy", "excellent",
        "good", "awesome", "amazing", "fantastic"
    ]

    sad_words = [
        "sad", "terrible", "bad", "hate",
        "awful", "worst", "angry", "horrible"
    ]

    results = []

    for sentence in data.sentences:
        text = sentence.lower()

        if any(word in text for word in happy_words):
            sentiment = "happy"
        elif any(word in text for word in sad_words):
            sentiment = "sad"
        else:
            sentiment = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}