from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class SentimentRequest(BaseModel):
    sentences: List[str]

@app.get("/")
def home():
    return {"message": "Sentiment API running"}

@app.post("/sentiment")
def analyze_sentiment(data: SentimentRequest):
    happy_words = [
        "love", "great", "happy", "excellent", "good",
        "awesome", "amazing", "fantastic", "wonderful"
    ]

    sad_words = [
        "sad", "terrible", "bad", "hate", "awful",
        "worst", "angry", "upset", "horrible"
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