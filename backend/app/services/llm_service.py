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
   - Use the provided retrieved knowledge base contexts whenever relevant to answer questions about coping strategies, CBT, DBT, ACT, mindfulness, sleep hygiene, grounding, panic de-escalation, imposter syndrome, ADHD coping, and mental wellness.
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

        # 3. Empathetic Grounded Fallback Engine
        return self._generate_grounded_fallback(user_message, retrieved_sources)

    def _generate_grounded_fallback(
        self,
        user_message: str,
        retrieved_sources: List[SourceReference]
    ) -> str:
        """
        Empathetic, evidence-grounded response synthesis when external LLM API keys
        are not configured or when third-party servers are temporarily unreachable.
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

        # Topic 1: Panic Attacks & Severe Acute Physical Anxiety
        if any(w in user_lower for w in ["panic attack", "heart racing", "can't breathe", "hyperventilat", "dizzy and shaking"]):
            return (
                f"I hear how intense and frightening these sensations feel right now. Please take comfort in knowing: "
                f"**Panic attacks are biologically self-limiting.** Your autonomic nervous system cannot sustain an adrenaline peak indefinitely; "
                f"it will naturally begin to downregulate within 10 to 15 minutes.\n\n"
                f"{evidence_summary}"
                f"**Immediate Somatic Reset:**\n"
                f"1. **Drop your shoulders and loosen your jaw.**\n"
                f"2. **Paced Breathing:** Inhale gently through your nose for 4 counts, hold for 2, and breathe out very slowly through pursed lips for 6 to 8 counts.\n"
                f"3. Splash cold water on your face to trigger the mammalian dive reflex.\n\n"
                f"You are safe in this moment. What is one object you can touch around you right now?\n\n{sources_note}"
            ).strip()

        # Topic 2: Overthinking, Rumination & Racing Thoughts
        elif any(w in user_lower for w in ["overthink", "rumination", "racing thought", "can't stop thinking", "in my head"]):
            return (
                f"Overthinking can feel like an exhausting mental loop that runs endlessly. It is very common, "
                f"especially when our minds are trying to protect us from uncertainty.\n\n"
                f"{evidence_summary}"
                f"A powerful technique is the **Scheduled Worry Window**: instead of battling the intrusive thoughts all day, "
                f"write them down and designate 15 minutes in the late afternoon to review them. Tell your mind: 'I hear this, but its time is 4:30 PM.'\n\n"
                f"Which thought is feeling loudest for you right now?\n\n{sources_note}"
            ).strip()

        # Topic 3: Procrastination & Task Initiation Paralysis
        elif any(w in user_lower for w in ["procrastinat", "can't start", "putting off", "avoiding work", "paralyzed to start"]):
            return (
                f"Thank you for sharing that. Procrastination is almost never laziness; it is an emotional regulation challenge "
                f"where the brain protects itself from feelings of dread, perfectionism, or fear of failure.\n\n"
                f"{evidence_summary}"
                f"Try using the **2-Minute Implementation Rule**: commit to opening the document or doing the first physical step "
                f"for only 120 seconds. Give yourself full permission to stop after 2 minutes. Usually, crossing that initial threshold "
                f"breaks the mental freeze.\n\n"
                f"What is the single smallest, lowest-friction step you could take today?\n\n{sources_note}"
            ).strip()

        # Topic 4: Imposter Syndrome & Workplace Insecurity
        elif any(w in user_lower for w in ["imposter", "fraud", "not smart enough", "faking it", "don't belong"]):
            return (
                f"Feeling like an imposter is an intensely common experience among conscientious, high-achieving individuals. "
                f"It is important to remember: **feelings of doubt are not facts about your competence.**\n\n"
                f"{evidence_summary}"
                f"Remind yourself that your human worth is not tied to flawless execution. Try creating an 'Evidence Portfolio' "
                f"of real problems you've solved and praise you've received to ground yourself in verifiable data rather than emotional appraisals.\n\n"
                f"What is one accomplishment or challenge you overcame that you are genuinely proud of?\n\n{sources_note}"
            ).strip()

        # Topic 5: Social Anxiety & Fear of Evaluation
        elif any(w in user_lower for w in ["social anxiety", "awkward", "everyone is judging", "parties", "talking to people"]):
            return (
                f"Navigating social situations with anxiety can feel like being under a blinding spotlight. "
                f"Psychologists call this the **Spotlight Effect**—we dramatically overestimate how much others notice our nervousness.\n\n"
                f"{evidence_summary}"
                f"Try **Attention Externalization**: instead of tracking your heart rate or vocal tone, consciously focus on the other "
                f"person's words, the ambient music, or the colors in the room. This takes the cognitive load off your internal alarm system.\n\n"
                f"What social setting is feeling most daunting for you right now?\n\n{sources_note}"
            ).strip()

        # Topic 6: Breakup, Heartbreak & Relationship Loss
        elif any(w in user_lower for w in ["breakup", "heartbreak", "heartbroken", "my ex", "dumped", "ended things"]):
            return (
                f"I am so sorry you are going through this. The end of a relationship triggers genuine neurobiological withdrawal—"
                f"your brain's attachment and reward centers are processing a profound loss of shared routines and safety.\n\n"
                f"{evidence_summary}"
                f"Be gentle with yourself. Mourning both the person and the future you envisioned is completely normal. "
                f"Prioritize simple grounding routines: staying hydrated, sleeping consistently, and leaning on trusted friends.\n\n"
                f"How are you holding up physically today?\n\n{sources_note}"
            ).strip()

        # Topic 7: Loneliness & Disconnection
        elif any(w in user_lower for w in ["lonely", "alone", "isolated", "no friends", "nobody cares"]):
            return (
                f"Loneliness can feel profoundly heavy, and I want to honor how honest it is of you to express it. "
                f"Loneliness is simply a biological signal indicating that your natural human need for belonging is asking for nourishment.\n\n"
                f"{evidence_summary}"
                f"Even small daily bids for connection—a friendly exchange with a barista, a short message to an acquaintance, "
                f"or sitting in a shared park or library—can begin signaling safety to your social nervous system.\n\n"
                f"Is there one person in your life you feel comfortable sending a quick 'thinking of you' message to today?\n\n{sources_note}"
            ).strip()

        # Topic 8: Anger & Irritability
        elif any(w in user_lower for w in ["angry", "irritat", "mad", "losing my temper", "rage", "frustrated"]):
            return (
                f"It is completely valid to feel anger. Anger is often the visible top of the **Anger Iceberg**, "
                f"acting as a protective armor for deeper vulnerable feelings like hurt, exhaustion, or feeling unappreciated.\n\n"
                f"{evidence_summary}"
                f"When you feel the wave rising, practice the **STOP protocol**: Stop physical action, Take a slow belly breath, "
                f"Observe what is happening inside without judgment, and Proceed with assertive intention rather than an explosive reaction.\n\n"
                f"What feeling might be hiding beneath the frustration right now?\n\n{sources_note}"
            ).strip()

        # Topic 9: Executive Dysfunction, ADHD & Cognitive Overload
        elif any(w in user_lower for w in ["adhd", "executive function", "brain fog", "can't focus", "scattered"]):
            return (
                f"Struggling with executive function is exhausting because your brain's management system is experiencing cognitive overload. "
                f"This is not a character flaw or laziness.\n\n"
                f"{evidence_summary}"
                f"Consider using **Body Doubling** (working in the presence of someone else or a virtual study stream) and externalizing "
                f"your memory onto visual sticky notes or whiteboards so your prefrontal cortex doesn't have to juggle tasks internally.\n\n"
                f"What is the main task competing for your focus right now?\n\n{sources_note}"
            ).strip()

        # Topic 10: General Anxiety & Stress
        elif any(w in user_lower for w in ["anxious", "anxiety", "worry", "fear", "nervous"]):
            return (
                f"Thank you for sharing that with me. Experiencing anxiety can feel exhausting, "
                f"and it is completely understandable to feel unsettled right now.\n\n"
                f"{evidence_summary}"
                f"A gentle exercise you might try right now is taking three slow, deliberate diaphragmatic breaths—letting "
                f"your exhalation last slightly longer than your inhalation to signal safety to your nervous system.\n\n"
                f"What part of this is feeling most challenging for you right now?\n\n{sources_note}"
            ).strip()

        # Topic 11: Sleep & Insomnia
        elif any(w in user_lower for w in ["sleep", "insomnia", "awake", "tired", "bed", "night"]):
            return (
                f"Struggling with sleep deeply affects your resilience, mood, and cognitive clarity. "
                f"It is so frustrating when you want to rest but your mind or body won't cooperate.\n\n"
                f"{evidence_summary}"
                f"Remember the **20-minute rule**: if you cannot fall asleep after roughly 20 minutes, get out of bed into dim lighting "
                f"and do a quiet, non-screen activity until drowsiness returns. This protects your conditioned bed-sleep association.\n\n"
                f"How has your wind-down routine felt over the past few days?\n\n{sources_note}"
            ).strip()

        # Topic 12: Burnout & Workplace Exhaustion
        elif any(w in user_lower for w in ["burnout", "stress", "work", "overwhelmed", "exhausted", "deadline"]):
            return (
                f"Feeling stretched past your limit is a real biological indicator that your system needs restoration and clearer boundaries.\n\n"
                f"{evidence_summary}"
                f"Give yourself permission to pause for even five minutes today to disengage from screens and release tension "
                f"in your shoulders and jaw.\n\n"
                f"What is one commitment or task you could step away from or delegate today?\n\n{sources_note}"
            ).strip()

        # Topic 13: Low Mood & Sadness
        elif any(w in user_lower for w in ["sad", "depressed", "down", "low", "hopeless", "crying"]):
            return (
                f"I hear how heavy things feel for you right now, and I want to acknowledge how much courage it takes "
                f"to put these feelings into words.\n\n"
                f"{evidence_summary}"
                f"When energy is low, treat yourself with unconditional gentleness. Even small micro-steps—like sipping warm tea "
                f"or sitting in natural light—are meaningful acts of care.\n\n"
                f"Would you like to talk more about what has been weighing on your heart?\n\n{sources_note}"
            ).strip()

        # Greetings
        elif any(w in user_lower for w in ["hello", "hi", "hey", "greetings"]):
            return (
                "Hello! I'm MindCare AI. I'm here to listen, offer supportive coping strategies, and help you reflect in a safe, "
                "non-judgmental space grounded in wellness research.\n\n"
                "How are you feeling today, and what's on your mind?"
            )

        # Default Grounded Reflection
        else:
            return (
                f"Thank you for opening up and sharing that with me. It is completely valid to reflect on what you are experiencing.\n\n"
                f"{evidence_summary}"
                f"I'm here to support you in exploring your thoughts and feelings. Please remember that while I can offer guidance "
                f"grounded in wellness research, reaching out to a therapist or trusted friend is always a wonderful option for personalized care.\n\n"
                f"How does that resonate with you, and where would you like to explore next?\n\n{sources_note}"
            ).strip()

llm_service = LLMService()
