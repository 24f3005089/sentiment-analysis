from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    sentences: List[str]

@app.get("/")
async def root():
    return {"message": "Sentiment API running"}

@app.post("/sentiment")
async def sentiment(data: InputData):

    results = []

    for sentence in data.sentences:

        text = sentence.lower()

        if any(word in text for word in [
            "love", "great", "excellent", "happy",
            "awesome", "good", "amazing"
        ]):
            label = "happy"

        elif any(word in text for word in [
            "hate", "bad", "terrible", "sad",
            "awful", "worst", "angry"
        ]):
            label = "sad"

        else:
            label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}