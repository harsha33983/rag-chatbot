import re
from typing import NamedTuple, Optional, List, Dict

class CrisisCheckResult(NamedTuple):
    is_crisis: bool
    crisis_type: Optional[str]  # "self_harm", "suicide", "harm_to_others", "immediate_danger"
    matched_patterns: List[str]
    crisis_response: Optional[str]
    helplines: List[Dict[str, str]]

# Emergency resources with specific support for India (112, 14416, 9999666555), US/Canada (988), UK (999, 116 123)
CRISIS_HELPLINES = [
    {
        "region": "India",
        "name": "National Emergency Services",
        "contact": "112",
        "description": "Immediate police, medical, and emergency dispatch (24/7, Toll-free)"
    },
    {
        "region": "India",
        "name": "Tele-MANAS (Govt. of India)",
        "contact": "14416 / 1800-891-4416",
        "description": "24/7 Comprehensive mental health support in multiple Indian languages"
    },
    {
        "region": "India",
        "name": "Vandrevala Foundation",
        "contact": "+91 9999 666 555",
        "description": "24/7 Free crisis intervention and mental health counseling"
    },
    {
        "region": "United States & Canada",
        "name": "Suicide & Crisis Lifeline",
        "contact": "988",
        "description": "24/7 Free & confidential call or text"
    },
    {
        "region": "United States & Canada",
        "name": "Crisis Text Line",
        "contact": "Text HOME to 741741",
        "description": "Free, 24/7 crisis support via text message"
    },
    {
        "region": "United Kingdom",
        "name": "Samaritans / Emergency",
        "contact": "116 123 / 999",
        "description": "24/7 Free emotional support and emergency response"
    },
    {
        "region": "International",
        "name": "Befrienders Worldwide",
        "contact": "https://www.befrienders.org",
        "description": "Global directory of emotional support hotlines"
    }
]

# High precision regex patterns for explicit self-harm, suicide, immediate danger, harm to others
EXPLICIT_SUICIDE_PATTERNS = [
    r"\b(want\s+to\s+die|wanna\s+die)\b",
    r"\b(kill\s+myself|killing\s+myself)\b",
    r"\b(commit\s+suicide|committing\s+suicide)\b",
    r"\b(end\s+my\s+life|ending\s+my\s+life)\b",
    r"\b(take\s+my\s+own\s+life)\b",
    r"\b(better\s+off\s+dead)\b",
    r"\b(no\s+reason\s+to\s+live)\b",
    r"\b(suicide\s+(plan|note|method|attempt))\b",
    r"\b(slit\s+my\s+wrists?)\b",
    r"\b(hang\s+myself)\b",
    r"\b(shoot\s+myself)\b",
    r"\b(jump\s+off\s+(a\s+bridge|a\s+roof|a\s+building|the\s+balcony))\b",
    r"\b(overdose\s+on\s+(pills|meds|drugs|medication))\b",
    r"\b(goodbye\s+(cruel\s+world|forever\s+everyone))\b",
    r"\b(i\s+can['']?t\s+go\s+on\s+living)\b"
]

SELF_HARM_PATTERNS = [
    r"\b(harm\s+myself|harming\s+myself)\b",
    r"\b(cut\s+myself|cutting\s+myself)\b",
    r"\b(burn\s+myself|burning\s+myself)\b",
    r"\b(hurt\s+myself\s+physically)\b",
    r"\b(self[\s\-]harm)\b",
    r"\b(urge\s+to\s+cut)\b"
]

IMMEDIATE_DANGER_PATTERNS = [
    r"\b(i\s+(swallowed|drank|took)\s+(all\s+the|a\s+bottle\s+of)\s+pills)\b",
    r"\b(i\s+have\s+a\s+(gun|weapon|knife)\s+to\s+my\s+(head|chest|wrist))\b",
    r"\b(i['']?m\s+bleeding\s+(out|heavily))\b",
    r"\b(standing\s+on\s+the\s+edge\s+of\s+(a\s+bridge|the\s+roof))\b"
]

HARM_TO_OTHERS_PATTERNS = [
    r"\b(kill\s+(someone|somebody|people|everyone|them|him|her))\b",
    r"\b(murder\s+(someone|somebody|people|them|him|her))\b",
    r"\b(shoot\s+up\s+a\s+(school|workplace|mall|place))\b",
    r"\b(stab\s+(someone|somebody|him|her|them))\b",
    r"\b(physically\s+attack\s+(someone|people))\b"
]

class SafetyService:
    @staticmethod
    def evaluate_message(text: str) -> CrisisCheckResult:
        """
        Screen the user's message for crisis, self-harm, suicide, or immediate danger.
        Returns a CrisisCheckResult. If is_crisis is True, normal generation MUST be bypassed.
        """
        if not text:
            return CrisisCheckResult(False, None, [], None, [])

        clean_text = text.lower().strip()

        # Check immediate danger
        for pattern in IMMEDIATE_DANGER_PATTERNS:
            if re.search(pattern, clean_text, re.IGNORECASE):
                return CrisisCheckResult(
                    is_crisis=True,
                    crisis_type="immediate_danger",
                    matched_patterns=[pattern],
                    crisis_response=SafetyService._build_emergency_response(immediate=True),
                    helplines=CRISIS_HELPLINES
                )

        # Check explicit suicide
        matched_suicide = []
        for pattern in EXPLICIT_SUICIDE_PATTERNS:
            if re.search(pattern, clean_text, re.IGNORECASE):
                matched_suicide.append(pattern)
        if matched_suicide:
            return CrisisCheckResult(
                is_crisis=True,
                crisis_type="suicide",
                matched_patterns=matched_suicide,
                crisis_response=SafetyService._build_emergency_response(immediate=False),
                helplines=CRISIS_HELPLINES
            )

        # Check self-harm
        matched_self_harm = []
        for pattern in SELF_HARM_PATTERNS:
            if re.search(pattern, clean_text, re.IGNORECASE):
                matched_self_harm.append(pattern)
        if matched_self_harm:
            return CrisisCheckResult(
                is_crisis=True,
                crisis_type="self_harm",
                matched_patterns=matched_self_harm,
                crisis_response=SafetyService._build_self_harm_response(),
                helplines=CRISIS_HELPLINES
            )

        # Check harm to others
        matched_harm_others = []
        for pattern in HARM_TO_OTHERS_PATTERNS:
            if re.search(pattern, clean_text, re.IGNORECASE):
                matched_harm_others.append(pattern)
        if matched_harm_others:
            return CrisisCheckResult(
                is_crisis=True,
                crisis_type="harm_to_others",
                matched_patterns=matched_harm_others,
                crisis_response=SafetyService._build_harm_others_response(),
                helplines=CRISIS_HELPLINES
            )

        return CrisisCheckResult(
            is_crisis=False,
            crisis_type=None,
            matched_patterns=[],
            crisis_response=None,
            helplines=[]
        )

    @staticmethod
    def _build_emergency_response(immediate: bool = False) -> str:
        urgency = "⚠️ **Please reach out for immediate support right now. Your safety and your life matter deeply.**"
        
        response = f"""{urgency}

I can hear how overwhelmed and in pain you are feeling right now. Please know that **you do not have to walk through this alone**, and there is immediate help available.

I am an AI assistant and cannot provide clinical crisis intervention or replace human emergency support. Please contact trusted emergency services or a dedicated crisis counselor right away:

### 🚨 Emergency Contacts & Helplines (Available 24/7):
- **India Emergency:** Dial **112** (Police, Medical, Fire, Immediate Rescue)
- **India Tele-MANAS (Govt. of India):** Dial **14416** or **1800-891-4416** (Free, confidential 24/7 mental health counseling in multiple languages)
- **India Vandrevala Foundation:** Dial **+91 9999 666 555** (24/7 free crisis counseling)
- **United States & Canada:** Call or Text **988** (Suicide & Crisis Lifeline)
- **Crisis Text Line:** Text **HOME to 741741**
- **United Kingdom:** Call **116 123** (Samaritans) or **999** for emergency dispatch
- **International:** Find local support worldwide at [Befrienders Worldwide](https://www.befrienders.org)

If you are in immediate physical danger, please call your local emergency services (like **112** or **911**), go to the nearest emergency room, or reach out to a trusted family member, neighbor, or friend who can be with you right now. People care about you and want to help you stay safe."""
        return response

    @staticmethod
    def _build_self_harm_response() -> str:
        return """⚠️ **You deserve gentle care and safety. Please reach out for support.**

I hear that you are going through an intensely painful moment right now and feeling the urge to harm yourself. These feelings can be overwhelming, but you do not have to navigate them alone.

Please consider these grounding actions right now:
1. **Safety First:** Put any dangerous objects out of reach or step into a room where someone else is present.
2. **Cold Temperature Reset (TIPP Skill):** Hold an ice cube in your hand, or splash cold water on your face. This activates the mammalian dive reflex and slows down your autonomic stress response.
3. **Connect with Support:** Speak with a compassionate crisis counselor or a trusted person.

### 📞 Immediate Crisis Helplines:
- **India:** Dial **112** (Emergency) or **14416** (Tele-MANAS, 24/7)
- **Vandrevala Foundation (India):** **+91 9999 666 555**
- **USA & Canada:** Call/Text **988**
- **Crisis Text Line:** Text **HOME to 741741**
- **UK:** Call **116 123** (Samaritans)

*MindCare AI is an automated support companion and cannot substitute professional mental healthcare or emergency assistance.*"""

    @staticmethod
    def _build_harm_others_response() -> str:
        return """⚠️ **Safety Notice**

I cannot assist with statements or intentions that involve violence or harming others. If you or someone else is in immediate danger or experiencing overwhelming thoughts of harm, please contact emergency services immediately:

- **India Emergency:** Dial **112**
- **USA/Canada Emergency:** Dial **911**
- **UK Emergency:** Dial **999**
- **Mental Health Crisis Support:** In India call **14416** (Tele-MANAS) or in the US/Canada call **988**."""

safety_service = SafetyService()

