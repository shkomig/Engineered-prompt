"""Tests for intent detection module."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.intent_detector import IntentDetector


def test_formal_letter_detection():
    """Test detection of formal letter intent."""
    detector = IntentDetector()

    text = "כתוב לי מכתב רשמי למורה על איחור של תלמיד"
    result = detector.detect_intent(text)

    assert result.intent == "formal_letter"
    assert result.confidence > 0.2
    assert "מכתב" in result.metadata["matched_keywords"]
    print(f"✓ Formal letter test passed: {result.intent} ({result.confidence:.2f})")


def test_creative_writing_detection():
    """Test detection of creative writing intent."""
    detector = IntentDetector()

    text = "כתוב לי סיפור קצר על חתול בחלל"
    result = detector.detect_intent(text)

    assert result.intent == "creative_writing"
    assert result.confidence > 0.2
    print(f"✓ Creative writing test passed: {result.intent} ({result.confidence:.2f})")


def test_email_detection():
    """Test detection of email intent."""
    detector = IntentDetector()

    text = "שלח מייל לעמית בעבודה לבקש עזרה"
    result = detector.detect_intent(text)

    assert result.intent == "email"
    print(f"✓ Email test passed: {result.intent} ({result.confidence:.2f})")


def test_translation_detection():
    """Test detection of translation intent."""
    detector = IntentDetector()

    text = "תרגם לי לאנגלית את המשפט הבא"
    result = detector.detect_intent(text)

    assert result.intent == "translation"
    print(f"✓ Translation test passed: {result.intent} ({result.confidence:.2f})")


def test_style_detection():
    """Test style detection."""
    detector = IntentDetector()

    text = "כתוב לי מכתב רשמי וקצר"
    result = detector.detect_intent(text)

    assert result.style["formality"] == "formal"
    assert result.style["length"] == "short"
    print(f"✓ Style detection test passed: {result.style}")


def test_unknown_intent():
    """Test handling of unknown/general intent."""
    detector = IntentDetector()

    text = "עזור לי עם משהו"
    result = detector.detect_intent(text)

    assert result.intent == "general"
    print(f"✓ General intent test passed: {result.intent}")


if __name__ == "__main__":
    print("Running intent detector tests...\n")

    test_formal_letter_detection()
    test_creative_writing_detection()
    test_email_detection()
    test_translation_detection()
    test_style_detection()
    test_unknown_intent()

    print("\n✅ All tests passed!")
