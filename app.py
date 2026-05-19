from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

happy_words = {
    "love", "great", "awesome", "good", "happy", "excellent",
    "amazing", "wonderful", "fantastic", "best", "like", "nice"
}

sad_words = {
    "sad", "terrible", "bad", "hate", "awful", "worst",
    "angry", "upset", "horrible", "disappointed", "poor"
}

def detect_sentiment(text: str) -> str:
    t = text.lower()

    happy_score = sum(word in t for word in happy_words)
    sad_score = sum(word in t for word in sad_words)

    if happy_score > sad_score:
        return "happy"
    elif sad_score > happy_score:
        return "sad"
    else:
        return "neutral"

@app.get("/")
async def root():
    return {"message": "Sentiment API running"}

@app.post("/sentiment")
async def sentiment(req: SentimentRequest):
    results = []

    for sentence in req.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": detect_sentiment(sentence)
        })

    return {"results": results}