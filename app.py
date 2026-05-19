from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class SentimentRequest(BaseModel):
    sentences: List[str]

# Sentiment prediction function
def predict_sentiment(sentence: str):

    text = sentence.lower()

    happy_words = [
        "love", "great", "excellent", "happy", "awesome",
        "good", "amazing", "fantastic", "wonderful", "best",
        "nice", "cool", "liked", "like", "enjoy", "enjoyed",
        "brilliant", "positive", "smile", "fun", "beautiful",
        "perfect", "super", "excited", "delight", "delighted",
        "pleased", "outstanding", "fabulous", "favorite",
        "success", "successful", "win", "winning", "yay",
        "glad", "cheerful", "satisfied", "pleasant", "excellent",
        "incredible", "sweet", "lovely", "awesome", "enthusiastic"
    ]

    sad_words = [
        "hate", "bad", "terrible", "sad", "awful",
        "worst", "angry", "horrible", "boring", "poor",
        "disappointed", "disappointing", "upset", "annoying",
        "pain", "cry", "depressed", "negative", "problem",
        "useless", "dislike", "failure", "failed", "losing",
        "loss", "tragic", "unhappy", "miserable", "frustrated",
        "stress", "stressed", "disaster", "sucks", "ugly",
        "regret", "furious", "damaged", "hurt", "pathetic",
        "unfortunate", "dreadful", "hate", "crying", "depressing"
    ]

    neutral_words = [
        "meeting", "schedule", "weather", "report",
        "class", "office", "project", "today",
        "tomorrow", "document", "information",
        "data", "update", "announcement"
    ]

    happy_score = 0
    sad_score = 0

    for word in happy_words:
        if word in text:
            happy_score += 1

    for word in sad_words:
        if word in text:
            sad_score += 1

    if happy_score > sad_score:
        return "happy"

    if sad_score > happy_score:
        return "sad"

    if any(word in text for word in neutral_words):
        return "neutral"

    # fallback rules
    if "!" in text and happy_score == 0 and sad_score == 0:
        return "happy"

    if "?" in text:
        return "neutral"

    return "neutral"

# GET endpoint
@app.get("/")
async def home():
    return {"message": "Sentiment API running"}

# POST endpoint for evaluator
@app.post("/")
async def analyze_root(data: SentimentRequest):

    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": predict_sentiment(sentence)
        })

    return {"results": results}

# POST endpoint for manual testing
@app.post("/sentiment")
async def analyze_sentiment(data: SentimentRequest):

    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": predict_sentiment(sentence)
        })

    return {"results": results}