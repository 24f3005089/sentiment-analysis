from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

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
async def root():
    return {"message": "API is working"}

@app.post("/sentiment")
async def analyze_sentiment(data: SentimentRequest):

    happy_words = [
        "love", "great", "excellent", "happy",
        "awesome", "good", "amazing", "fantastic"
    ]

    sad_words = [
        "hate", "bad", "terrible", "sad",
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