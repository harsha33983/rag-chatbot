import logging
import os
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.schemas.chat import SourceReference

logger = logging.getLogger(__name__)

MINDCARE_SYSTEM_PROMPT = """You are MindCare AI, an empathetic, supportive, and grounded mental wellness conversational companion.

Your Core Directives:
1. Tone: Warm, empathetic, validating, non-judgmental, and calm.
2. Boundaries:
   - You are an AI assistant for mental well-being support, NOT a doctor, psychiatrist, or licensed psychotherapist.
   - NEVER diagnose mental health disorders (e.g., do not say 'You have Major Depressive Disorder' or 'This is Generalized Anxiety').
   - NEVER prescribe or recommend specific medications.
   - NEVER claim to provide clinical medical advice.
   - Always encourage consulting a qualified mental health professional or physician for clinical evaluation.
3. RAG Grounding & Source Citation:
   - Use the provided retrieved knowledge base contexts whenever relevant to answer questions about coping strategies, CBT, DBT, mindfulness, sleep hygiene, grounding, and mental wellness.
   - Mention the concepts or techniques referenced from the sources naturally.
   - If the user asks a question about something not in your knowledge base and you are uncertain, honestly acknowledge the limitation instead of fabricating an answer.
4. Style:
   - Break responses into clear, readable paragraphs or brief bullet points when explaining exercises.
   - Conclude with an open, gentle reflection or question to support the user's journey.
"""

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.model_name = settings.LLM_MODEL
        self._gemini_client = None

    def _init_gemini(self):
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            return genai.GenerativeModel(
                model_name=self.model_name if "gemini" in self.model_name else "gemini-1.5-flash",
                system_instruction=MINDCARE_SYSTEM_PROMPT
            )
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return None

    def generate_response(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        retrieved_sources: List[SourceReference]
    ) -> str:
        """
        Synthesizes empathetic, evidence-grounded response using LLM or robust fallback.
        """
        # Format knowledge context
        context_text = ""
        if retrieved_sources:
            context_blocks = []
            for i, src in enumerate(retrieved_sources, 1):
                context_blocks.append(
                    f"[Source {i}: '{src.title}' ({src.category})]\n{src.snippet}"
                )
            context_text = "\n\nRelevant Knowledge Base Evidence:\n" + "\n\n".join(context_blocks)
        else:
            context_text = "\n(No high-confidence knowledge base articles found for this specific query.)"

        prompt_with_context = f"""{context_text}

User Query:
{user_message}

Please provide an empathetic, grounded response following your core directives."""

        # 1. Try Gemini if configured
        if self.provider == "gemini" or (settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")):
            try:
                model = self._init_gemini()
                if model:
                    # Build history for Gemini
                    gemini_history = []
                    for msg in conversation_history:
                        role = "user" if msg["role"] == "user" else "model"
                        gemini_history.append({"role": role, "parts": [msg["content"]]})

                    chat = model.start_chat(history=gemini_history)
                    resp = chat.send_message(prompt_with_context)
                    if resp and resp.text:
                        return resp.text.strip()
            except Exception as e:
                logger.warning(f"Gemini API call failed: {e}. Attempting fallback.")

        # 2. Try OpenAI if configured
        api_key = settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if (self.provider == "openai" or api_key) and api_key:
            try:
                import httpx
                messages = [{"role": "system", "content": MINDCARE_SYSTEM_PROMPT}]
                for msg in conversation_history:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                messages.append({"role": "user", "content": prompt_with_context})

                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": self.model_name if "gpt" in self.model_name else "gpt-4o-mini",
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 800
                }
                with httpx.Client(timeout=30.0) as client:
                    res = client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
                    if res.status_code == 200:
                        data = res.json()
                        return data["choices"][0]["message"]["content"].strip()
                    else:
                        logger.warning(f"OpenAI error {res.status_code}: {res.text}")
            except Exception as e:
                logger.warning(f"OpenAI API call failed: {e}. Using intelligent fallback.")

        # 3. Empathetic Fallback Engine (Reliable, evidence-grounded, zero-crash)
        return self._generate_grounded_fallback(user_message, retrieved_sources)

    def _generate_grounded_fallback(
        self,
        user_message: str,
        retrieved_sources: List[SourceReference]
    ) -> str:
        """
        High quality, empathetic, grounded response synthesis when API keys are not supplied
        or third-party providers are temporarily unreachable.
        """
        user_lower = user_message.lower()

        # Build evidence section if sources are available
        if retrieved_sources:
            primary_source = retrieved_sources[0]
            evidence_summary = (
                f"Based on **{primary_source.title}** ({primary_source.category}):\n\n"
                f"{primary_source.snippet.strip()}\n\n"
            )
            sources_note = f"📖 *Referenced from: {primary_source.title}*"
        else:
            evidence_summary = (
                "While I don't have a specific clinical article in my library that directly addresses this nuance, "
                "I am here to listen and help you unpack your thoughts.\n\n"
            )
            sources_note = ""

        # Empathetic framing based on topic cues
        if any(w in user_lower for w in ["anxious", "anxiety", "panic", "worry", "fear"]):
            return (
                f"Thank you for sharing that with me. Experiencing anxiety or worry can feel truly exhausting, "
                f"and it is completely understandable to feel unsettled right now.\n\n"
                f"{evidence_summary}"
                f"A gentle exercise you might try right now is taking three slow, deliberate diaphragmatic breaths—letting "
                f"your exhalation last slightly longer than your inhalation to signal safety to your nervous system.\n\n"
                f"What part of this is feeling most challenging for you right now?\n\n{sources_note}"
            ).strip()

        elif any(w in user_lower for w in ["sad", "depressed", "down", "low", "hopeless", "tired", "empty"]):
            return (
                f"I hear how heavy things feel for you right now, and I want to acknowledge how much courage it takes "
                f"to put these feelings into words.\n\n"
                f"{evidence_summary}"
                f"When your energy is low, remember to treat yourself with gentle kindness. Even small steps, like stepping "
                f"outside for a few moments or sipping some water, can be meaningful acts of self-care.\n\n"
                f"Would you like to talk more about what's been weighing on you today?\n\n{sources_note}"
            ).strip()

        elif any(w in user_lower for w in ["sleep", "insomnia", "awake", "tired", "bed", "night"]):
            return (
                f"Struggling with sleep can deeply affect your mood, energy, and overall resilience during the day. "
                f"It is so frustrating when you want to rest but your mind or body won't cooperate.\n\n"
                f"{evidence_summary}"
                f"If you've been lying in bed unable to sleep for more than 20 minutes, try sitting in a comfortable chair "
                f"with soft lighting and doing a quiet, screen-free activity until you begin to feel drowsy.\n\n"
                f"How has your sleep routine felt over the past few days?\n\n{sources_note}"
            ).strip()

        elif any(w in user_lower for w in ["burnout", "stress", "work", "overwhelmed", "exhausted", "deadline"]):
            return (
                f"Feeling overwhelmed or stretched to your limit is a very real biological signal that your system needs "
                f"restoration and clearer boundaries.\n\n"
                f"{evidence_summary}"
                f"Give yourself permission to pause for even five minutes today to disengage from screens and release tension "
                f"in your shoulders and jaw.\n\n"
                f"What is one commitment or task you could step away from or delegate today?\n\n{sources_note}"
            ).strip()

        elif any(w in user_lower for w in ["hello", "hi", "hey", "greetings"]):
            return (
                "Hello! I'm MindCare AI. I'm here to listen, offer supportive coping strategies, and help you reflect in a safe, "
                "non-judgmental space.\n\n"
                "How are you feeling today, and what's on your mind?"
            )

        else:
            return (
                f"Thank you for opening up and sharing that with me. It is completely valid to reflect on what you are experiencing.\n\n"
                f"{evidence_summary}"
                f"I'm here to support you in exploring your thoughts and feelings. Please remember that while I can offer guidance "
                f"grounded in wellness research, reaching out to a therapist or trusted friend is always a powerful way to get personalized support.\n\n"
                f"How does that resonate with you, and where would you like to explore next?\n\n{sources_note}"
            ).strip()

llm_service = LLMService()

