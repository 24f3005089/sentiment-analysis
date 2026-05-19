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

def predict_sentiment(sentence: str):
    text = sentence.lower()

    happy_words = [
        "love", "great", "excellent", "happy",
        "awesome", "good", "amazing", "fantastic"
    ]

    sad_words = [
        "hate", "bad", "terrible", "sad",
        "awful", "worst", "angry", "horrible"
    ]

    if any(word in text for word in happy_words):
        return "happy"

    if any(word in text for word in sad_words):
        return "sad"

    return "neutral"

@app.get("/")
async def home():
    return {"message": "Sentiment API running"}

# IMPORTANT: accept POST on root URL also
@app.post("/")
async def root_sentiment(data: SentimentRequest):

    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": predict_sentiment(sentence)
        })

    return {"results": results}

@app.post("/sentiment")
async def sentiment(data: SentimentRequest):

    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": predict_sentiment(sentence)
        })

    return {"results": results}