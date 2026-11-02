from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.app.services.sentiment_service import sentiment_service

router = APIRouter(prefix="/sentiment", tags=["Sentiment & Emotion Analysis"])

class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="User input text to classify")

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    label: str
    confidence: float
    tone_strategy: str
    tone_instruction: str
    disclaimer: str = "Sentiment analysis is an NLP feature for conversational tone adaptation and is not a clinical mental health diagnosis."

@router.post("/predict", response_model=SentimentResponse)
def predict_sentiment(req: SentimentRequest):
    result = sentiment_service.predict(req.text)
    return SentimentResponse(
        text=req.text,
        sentiment=result.label,
        label=result.label,
        confidence=result.confidence,
        tone_strategy=result.tone_strategy,
        tone_instruction=result.tone_instruction
    )

