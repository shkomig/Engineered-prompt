"""Tests for prompt generation module."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.prompt_generator import PromptGenerator


def test_prompt_generation():
    """Test basic prompt generation."""
    generator = PromptGenerator()

    text = "כתוב לי מכתב רשמי למורה על איחור של תלמיד"
    result = generator.generate(text)

    assert result.prompt is not None
    assert len(result.prompt) > 50
    assert result.intent == "formal_letter"
    print(f"✓ Basic generation test passed")
    print(f"  Intent: {result.intent}")
    print(f"  Template: {result.template_used}")
    print(f"  Prompt length: {len(result.prompt)} chars")


def test_creative_prompt_generation():
    """Test creative writing prompt generation."""
    generator = PromptGenerator()

    text = "כתוב לי סיפור יצירתי על חתול בחלל"
    result = generator.generate(text)

    assert result.intent == "creative_writing"
    assert "story" in result.prompt.lower() or "creative" in result.prompt.lower()
    print(f"✓ Creative writing generation test passed")


def test_email_prompt_generation():
    """Test email prompt generation."""
    generator = PromptGenerator()

    text = "כתוב מייל לעמית לבקש עזרה בפרויקט"
    result = generator.generate(text)

    assert result.intent == "email"
    assert "email" in result.prompt.lower() or "message" in result.prompt.lower()
    print(f"✓ Email generation test passed")


def test_intent_override():
    """Test manual intent override."""
    generator = PromptGenerator()

    text = "עזור לי"
    result = generator.generate(text, override_intent="translation")

    assert result.intent == "translation"
    print(f"✓ Intent override test passed")


def test_template_loading():
    """Test that all templates are loaded."""
    generator = PromptGenerator()

    templates = generator.get_available_templates()
    assert len(templates) >= 5  # Should have at least 5 templates
    print(f"✓ Template loading test passed: {len(templates)} templates loaded")

    for template in templates:
        print(f"  - {template['name']} ({template['intent']})")


if __name__ == "__main__":
    print("Running prompt generator tests...\n")

    test_template_loading()
    test_prompt_generation()
    test_creative_prompt_generation()
    test_email_prompt_generation()
    test_intent_override()

    print("\n✅ All tests passed!")
