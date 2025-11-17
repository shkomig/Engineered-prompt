"""Intent detection module - identifies user's goal from Hebrew text."""
import re
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class IntentResult:
    """Result of intent detection."""
    intent: str
    confidence: float
    style: Dict[str, str]
    metadata: Dict[str, any]


class IntentDetector:
    """Rule-based intent detector for Hebrew text."""

    # Intent patterns - Hebrew keywords that indicate specific intents
    INTENT_PATTERNS = {
        "formal_letter": {
            "keywords": [
                "מכתב", "מכתבים", "פנייה רשמית", "בקשה רשמית",
                "למורה", "למנהל", "להנהלה", "מכתב התפטרות",
                "תלונה רשמית", "בקשה להיעדרות"
            ],
            "confidence_boost": 0.3
        },
        "creative_writing": {
            "keywords": [
                "סיפור", "שיר", "כתיבה יצירתית", "תיאור",
                "סיפור קצר", "חיבור", "רעיון לסיפור", "עלילה"
            ],
            "confidence_boost": 0.3
        },
        "email": {
            "keywords": [
                "אימייל", "מייל", "הודעה", "שלח הודעה",
                "כתוב לי מייל", "email", "דוא\"ל"
            ],
            "confidence_boost": 0.25
        },
        "summary": {
            "keywords": [
                "סיכום", "תמצית", "לסכם", "תקציר",
                "עיקרי הנושא", "נקודות עיקריות"
            ],
            "confidence_boost": 0.25
        },
        "translation": {
            "keywords": [
                "תרגם", "תרגום", "לאנגלית", "לעברית",
                "translate", "תרגם לי"
            ],
            "confidence_boost": 0.4
        },
        "question_answer": {
            "keywords": [
                "מה זה", "איך", "למה", "מדוע", "תסביר",
                "הסבר", "שאלה", "?", "תענה"
            ],
            "confidence_boost": 0.2
        },
        "business_proposal": {
            "keywords": [
                "הצעה עסקית", "פרזנטציה", "עסקים",
                "מצגת", "הצעת מחיר", "proposal"
            ],
            "confidence_boost": 0.3
        }
    }

    # Style indicators
    FORMALITY_INDICATORS = {
        "formal": ["רשמי", "פורמלי", "מכובד", "נימוס", "רציני"],
        "casual": ["חופשי", "קליל", "לא רשמי", "חברי", "נינוח"],
    }

    TONE_INDICATORS = {
        "positive": ["חיובי", "אופטימי", "שמח", "מעודד"],
        "neutral": ["נייטרלי", "אובייקטיבי", "עניינל"],
        "critical": ["ביקורתי", "שלילי", "קריטי"],
    }

    LENGTH_INDICATORS = {
        "short": ["קצר", "תמציתי", "קצרצר", "במשפט"],
        "medium": ["בינוני", "סביר", "רגיל"],
        "long": ["ארוך", "מפורט", "מקיף", "מעמיק"],
    }

    def detect_intent(self, text: str) -> IntentResult:
        """
        Detect user intent from Hebrew text.

        Args:
            text: Hebrew input text

        Returns:
            IntentResult with detected intent, confidence, style, and metadata
        """
        text_lower = text.lower()

        # Calculate confidence scores for each intent
        intent_scores = {}
        for intent, config in self.INTENT_PATTERNS.items():
            score = 0.0
            matched_keywords = []

            for keyword in config["keywords"]:
                if keyword.lower() in text_lower:
                    score += config["confidence_boost"]
                    matched_keywords.append(keyword)

            if matched_keywords:
                intent_scores[intent] = {
                    "score": min(score, 1.0),  # Cap at 1.0
                    "keywords": matched_keywords
                }

        # If no intent detected, default to general
        if not intent_scores:
            detected_intent = "general"
            confidence = 0.5
            matched_keywords = []
        else:
            # Get intent with highest score
            detected_intent = max(intent_scores.items(), key=lambda x: x[1]["score"])[0]
            confidence = intent_scores[detected_intent]["score"]
            matched_keywords = intent_scores[detected_intent]["keywords"]

        # Detect style
        style = self._detect_style(text_lower)

        return IntentResult(
            intent=detected_intent,
            confidence=confidence,
            style=style,
            metadata={
                "matched_keywords": matched_keywords,
                "all_scores": {k: v["score"] for k, v in intent_scores.items()}
            }
        )

    def _detect_style(self, text: str) -> Dict[str, str]:
        """Detect writing style from text."""
        style = {
            "formality": "neutral",
            "tone": "neutral",
            "length": "medium"
        }

        # Detect formality
        formal_count = sum(1 for indicator in self.FORMALITY_INDICATORS["formal"] if indicator in text)
        casual_count = sum(1 for indicator in self.FORMALITY_INDICATORS["casual"] if indicator in text)

        if formal_count > casual_count:
            style["formality"] = "formal"
        elif casual_count > formal_count:
            style["formality"] = "casual"

        # Detect tone
        tone_scores = {}
        for tone, indicators in self.TONE_INDICATORS.items():
            tone_scores[tone] = sum(1 for indicator in indicators if indicator in text)

        if max(tone_scores.values()) > 0:
            style["tone"] = max(tone_scores.items(), key=lambda x: x[1])[0]

        # Detect length preference
        length_scores = {}
        for length, indicators in self.LENGTH_INDICATORS.items():
            length_scores[length] = sum(1 for indicator in indicators if indicator in text)

        if max(length_scores.values()) > 0:
            style["length"] = max(length_scores.items(), key=lambda x: x[1])[0]

        return style

    def get_supported_intents(self) -> list:
        """Get list of all supported intents."""
        return list(self.INTENT_PATTERNS.keys()) + ["general"]
