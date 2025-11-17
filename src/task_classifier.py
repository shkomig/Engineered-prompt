"""Task classification module - classifies user tasks into visual/textual/technical."""
import re
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class TaskResult:
    """Result of task classification."""
    task_type: str  # visual, textual, or technical
    confidence: float
    style: Dict[str, str]
    metadata: Dict[str, any]


class TaskClassifier:
    """Rule-based task classifier for Hebrew text - classifies into 3 main categories."""

    # Task classification patterns - Hebrew keywords that indicate task type
    TASK_PATTERNS = {
        "visual": {
            "keywords": [
                # Image/Video creation keywords
                "תמונה", "תמונות", "צור תמונה", "ציור", "אילוסטרציה",
                "גרפיקה", "וידאו", "סרטון", "אנימציה", "דיאגרמה",
                "לוגו", "עיצוב גרפי", "פוסטר", "באנר", "אייקון",
                "render", "3d", "art", "image", "picture", "visual",
                "דמיון חזותי", "ויזואליזציה", "מפה", "אינפוגרפיקה"
            ],
            "confidence_boost": 0.4
        },
        "technical": {
            "keywords": [
                # Code/Programming keywords
                "קוד", "פונקציה", "תכנת", "פייתון", "python", "javascript",
                "תוכנית", "סקריפט", "אלגוריתם", "api", "database",
                "sql", "react", "django", "code", "function", "class",
                "debug", "באג", "שגיאה בקוד", "optimization", "רפקטור",
                "לולאה", "תנאי", "משתנה", "מחלקה", "אובייקט", "json",
                "html", "css", "nodejs", "git", "regex", "formula",
                "נוסחה", "חישוב מתמטי", "latex", "equation", "מתמטיקה"
            ],
            "confidence_boost": 0.4
        },
        "textual": {
            "keywords": [
                # Text creation keywords
                "כתוב", "מכתב", "אימייל", "מייל", "סיכום", "מאמר",
                "דוח", "הצעה", "תיאור", "סיפור", "תוכן", "טקסט",
                "הודעה", "פוסט", "בלוג", "רשימה", "מסמך", "נייר עמדה",
                "email", "letter", "document", "write", "compose",
                "תרגם", "הסבר", "סכם", "נסח", "ערוך", "תענה",
                "שאלה", "תשובה", "מדריך", "הוראות", "FAQ", "תיעוד",
                "פרזנטציה", "מצגת", "נאום", "דברי פתיחה"
            ],
            "confidence_boost": 0.3
        }
    }

    # Style indicators for textual tasks
    FORMALITY_INDICATORS = {
        "formal": ["רשמי", "פורמלי", "מכובד", "נימוס", "רציני", "מקצועי"],
        "casual": ["חופשי", "קליל", "לא רשמי", "חברי", "נינוח", "משעשע"],
    }

    TONE_INDICATORS = {
        "professional": ["מקצועי", "עסקי", "פורמלי"],
        "friendly": ["ידידותי", "חברי", "חם"],
        "urgent": ["דחוף", "מיידי", "חשוב"],
        "persuasive": ["משכנע", "שכנוע", "להניע"],
        "informative": ["אינפורמטיבי", "מידע", "להסביר"]
    }

    LENGTH_INDICATORS = {
        "concise": ["קצר", "תמציתי", "קצרצר", "במשפט", "1-2"],
        "moderate": ["בינוני", "סביר", "רגיל", "3-5"],
        "extensive": ["ארוך", "מפורט", "מקיף", "מעמיק", "1000"],
    }

    def classify_task(self, text: str) -> TaskResult:
        """
        Classify user task from Hebrew text into visual/textual/technical.

        Args:
            text: Hebrew input text

        Returns:
            TaskResult with detected task type, confidence, style, and metadata
        """
        text_lower = text.lower()

        # Calculate confidence scores for each task type
        task_scores = {}
        for task_type, config in self.TASK_PATTERNS.items():
            score = 0.0
            matched_keywords = []

            for keyword in config["keywords"]:
                if keyword.lower() in text_lower:
                    score += config["confidence_boost"]
                    matched_keywords.append(keyword)

            if matched_keywords:
                task_scores[task_type] = {
                    "score": min(score, 1.0),  # Cap at 1.0
                    "keywords": matched_keywords
                }

        # Determine task type
        if not task_scores:
            # Default to textual if no specific keywords found
            detected_task = "textual"
            confidence = 0.5
            matched_keywords = []
        else:
            # Get task type with highest score
            detected_task = max(task_scores.items(), key=lambda x: x[1]["score"])[0]
            confidence = task_scores[detected_task]["score"]
            matched_keywords = task_scores[detected_task]["keywords"]

        # Detect style (primarily for textual tasks)
        style = self._detect_style(text_lower, detected_task)

        return TaskResult(
            task_type=detected_task,
            confidence=confidence,
            style=style,
            metadata={
                "matched_keywords": matched_keywords,
                "all_scores": {k: v["score"] for k, v in task_scores.items()}
            }
        )

    def _detect_style(self, text: str, task_type: str) -> Dict[str, str]:
        """Detect style attributes from text."""
        style = {
            "formality": "neutral",
            "tone": "neutral",
            "length": "moderate"
        }

        # Only detect style for textual tasks
        if task_type != "textual":
            return style

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

    def get_supported_tasks(self) -> list:
        """Get list of all supported task types."""
        return ["visual", "textual", "technical"]
