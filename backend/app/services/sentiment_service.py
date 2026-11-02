import os
import logging
from typing import Dict, Any, NamedTuple, Optional
from pathlib import Path
import joblib

logger = logging.getLogger(__name__)

class SentimentResult(NamedTuple):
    label: str               # "happy" | "sad" | "angry" | "fearful" | "anxious" | "neutral"
    confidence: float        # 0.0 - 1.0
    tone_strategy: str       # Short descriptor of the tone adaptation strategy
    tone_instruction: str    # System prompt guidance for the LLM

TONE_MAPPINGS: Dict[str, Dict[str, str]] = {
    "happy": {
        "strategy": "Supportive & Celebratory",
        "instruction": "The user is expressing positive, hopeful, or joyful emotions. Mirror their warmth with encouraging, celebratory reinforcement while remaining grounded and present."
    },
    "sad": {
        "strategy": "Empathetic & Gentle",
        "instruction": "The user is feeling sad, grieving, or emotionally heavy. Adopt an exceptionally gentle, soft, validating tone. Avoid toxic positivity or rushing to solutions. Acknowledge the weight of their feelings first."
    },
    "angry": {
        "strategy": "Calm & De-escalating",
        "instruction": "The user is feeling frustrated, angry, or resentful. Maintain a calm, respectful, non-defensive demeanor. Validate that frustration is a normal human response, avoid condescending language, and support them in untangling what is underneath the anger."
    },
    "fearful": {
        "strategy": "Reassuring & Grounding",
        "instruction": "The user is experiencing fear, acute dread, or feeling threatened. Offer a steady, reassuring presence. Emphasize physical and psychological safety in the present moment, keeping instructions simple and grounded."
    },
    "anxious": {
        "strategy": "Structured & Calming",
        "instruction": "The user is feeling anxious, restless, or overthinking. Use structured, clear, and steady language. Break recommendations into small, bite-sized steps (such as slow breathing or single sensory grounding cues) to avoid cognitive overwhelm."
    },
    "neutral": {
        "strategy": "Balanced & Informative",
        "instruction": "The user is asking an informational, reflective, or neutral question. Provide clear, objective, and well-organized insights with a compassionate, respectful tone."
    }
}

class SentimentService:
    def __init__(self):
        self._model = None
        self._model_path = Path(__file__).resolve().parent.parent / "ml" / "sentiment_pipeline.joblib"

    @property
    def model(self):
        if self._model is None:
            if self._model_path.exists():
                try:
                    self._model = joblib.load(self._model_path)
                    logger.info(f"Loaded 6-class sentiment model from {self._model_path}")
                except Exception as e:
                    logger.warning(f"Failed to load sentiment model ({e}). Using rule-based fallback.")
                    self._model = "fallback"
            else:
                logger.warning(f"Sentiment model not found at {self._model_path}. Using fallback.")
                self._model = "fallback"
        return self._model

    def predict(self, text: str) -> SentimentResult:
        """
        Predicts one of the 6 emotional classes (happy, sad, angry, fearful, anxious, neutral)
        along with prediction confidence and real-time tone adaptation instructions.
        Note: This is an NLP conversational aid and must NEVER be treated as clinical diagnosis.
        """
        if not text or not text.strip():
            return self._build_result("neutral", 1.0)

        clean_text = text.strip()

        # Try ML Model prediction
        m = self.model
        if m != "fallback" and hasattr(m, "predict") and hasattr(m, "predict_proba"):
            try:
                pred_label = m.predict([clean_text])[0]
                probs = m.predict_proba([clean_text])[0]
                classes = list(m.classes_)
                idx = classes.index(pred_label)
                confidence = float(probs[idx])
                return self._build_result(pred_label, round(confidence, 4))
            except Exception as e:
                logger.warning(f"Error during ML sentiment prediction: {e}. Using fallback.")

        # Robust heuristic fallback
        return self._fallback_predict(clean_text)

    def _fallback_predict(self, text: str) -> SentimentResult:
        t = text.lower()
        if any(w in t for w in ["panic", "anxious", "anxiety", "worried", "nervous", "dread", "racing thoughts"]):
            return self._build_result("anxious", 0.85)
        if any(w in t for w in ["terrified", "scared", "fear", "frightened", "nightmare", "horror"]):
            return self._build_result("fearful", 0.85)
        if any(w in t for w in ["angry", "mad", "furious", "hate", "irritated", "pissed", "rage"]):
            return self._build_result("angry", 0.85)
        if any(w in t for w in ["sad", "depressed", "crying", "unhappy", "grief", "hopeless", "lonely"]):
            return self._build_result("sad", 0.85)
        if any(w in t for w in ["happy", "glad", "proud", "joy", "excited", "grateful", "relieved", "great"]):
            return self._build_result("happy", 0.85)
        return self._build_result("neutral", 0.80)

    def _build_result(self, label: str, confidence: float) -> SentimentResult:
        mapping = TONE_MAPPINGS.get(label, TONE_MAPPINGS["neutral"])
        return SentimentResult(
            label=label,
            confidence=confidence,
            tone_strategy=mapping["strategy"],
            tone_instruction=mapping["instruction"]
        )

sentiment_service = SentimentService()

