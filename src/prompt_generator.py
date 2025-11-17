"""Prompt generation engine - creates optimized prompts from templates."""
import json
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass

from .intent_detector import IntentDetector, IntentResult


@dataclass
class GeneratedPrompt:
    """Result of prompt generation."""
    prompt: str
    template_used: str
    intent: str
    confidence: float
    variables: Dict[str, str]
    metadata: Dict


class PromptGenerator:
    """Main prompt generation engine."""

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize prompt generator.

        Args:
            templates_dir: Directory containing template JSON files
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"

        self.templates_dir = Path(templates_dir)
        self.templates = self._load_templates()
        self.intent_detector = IntentDetector()

    def _load_templates(self) -> Dict[str, Dict]:
        """Load all template files from templates directory."""
        templates = {}

        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")

        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    intent = template_data.get("intent")
                    if intent:
                        templates[intent] = template_data
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")

        return templates

    def generate(self, hebrew_text: str, override_intent: Optional[str] = None) -> GeneratedPrompt:
        """
        Generate an optimized prompt from Hebrew text.

        Args:
            hebrew_text: Input text in Hebrew
            override_intent: Optional intent override (if user wants specific type)

        Returns:
            GeneratedPrompt object with the generated prompt and metadata
        """
        # Detect intent and style
        intent_result = self.intent_detector.detect_intent(hebrew_text)

        # Use override if provided
        final_intent = override_intent if override_intent else intent_result.intent

        # Ensure intent is supported
        if final_intent not in self.templates:
            final_intent = "general"

        # Get template
        template_data = self.templates[final_intent]

        # Extract variables from input text
        variables = self._extract_variables(hebrew_text, intent_result, template_data)

        # Generate prompt from template
        prompt = self._fill_template(template_data["template"], variables)

        # Add best practices and enhancements
        enhanced_prompt = self._enhance_prompt(prompt, intent_result)

        return GeneratedPrompt(
            prompt=enhanced_prompt,
            template_used=template_data["name"],
            intent=final_intent,
            confidence=intent_result.confidence,
            variables=variables,
            metadata={
                "style": intent_result.style,
                "matched_keywords": intent_result.metadata.get("matched_keywords", []),
                "original_text": hebrew_text
            }
        )

    def _extract_variables(
        self,
        text: str,
        intent_result: IntentResult,
        template_data: Dict
    ) -> Dict[str, str]:
        """
        Extract variables from text to fill template.

        This is a simplified extraction. In production, you'd use NER or LLM for better extraction.
        """
        variables = {}

        # Common variables based on detected style
        style = intent_result.style

        # Formality level
        if style["formality"] == "formal":
            variables["formality_level"] = "highly formal and professional"
        elif style["formality"] == "casual":
            variables["formality_level"] = "casual and friendly"
        else:
            variables["formality_level"] = "polite and respectful"

        # Tone
        variables["tone"] = style.get("tone", "neutral")

        # Length
        length_map = {
            "short": "concise (1-2 paragraphs)",
            "medium": "moderate length (3-5 paragraphs)",
            "long": "detailed and comprehensive (5+ paragraphs)"
        }
        variables["target_length"] = length_map.get(style.get("length", "medium"), "moderate length")

        # Intent-specific variables
        if intent_result.intent == "formal_letter":
            variables["topic"] = self._extract_topic(text)
            variables["recipient"] = self._extract_recipient(text)
            variables["context"] = text
            variables["additional_instructions"] = ""

        elif intent_result.intent == "creative_writing":
            variables["content_type"] = self._detect_content_type(text)
            variables["topic"] = self._extract_topic(text)
            variables["creativity_level"] = "high" if "יצירתי" in text else "moderate"
            variables["audience"] = "general"
            variables["theme_elements"] = ""
            variables["additional_instructions"] = text

        elif intent_result.intent == "email":
            variables["purpose"] = self._extract_purpose(text)
            variables["recipient"] = self._extract_recipient(text)
            variables["key_points"] = text
            variables["context"] = ""
            variables["additional_instructions"] = ""

        elif intent_result.intent == "summary":
            variables["summary_type"] = "summary"
            variables["content"] = text
            variables["focus_areas"] = "main points"
            variables["style"] = "clear and concise"
            variables["must_include"] = "key information"
            variables["additional_instructions"] = ""

        elif intent_result.intent == "translation":
            variables["source_language"] = "Hebrew"
            variables["target_language"] = self._detect_target_language(text)
            variables["text"] = text
            variables["cultural_context"] = "maintain original intent"
            variables["style"] = style["formality"]
            variables["additional_instructions"] = ""

        elif intent_result.intent == "question_answer":
            variables["question"] = text
            variables["context"] = ""
            variables["style"] = "clear and informative"
            variables["detail_level"] = style["length"]
            variables["must_include"] = "examples if relevant"
            variables["additional_instructions"] = ""

        else:  # general
            variables["task_description"] = text
            variables["style"] = style["formality"]
            variables["format"] = "clear and well-structured"
            variables["context"] = ""
            variables["additional_instructions"] = ""

        return variables

    def _fill_template(self, template: str, variables: Dict[str, str]) -> str:
        """Fill template with variables."""
        filled = template

        for key, value in variables.items():
            placeholder = "{" + key + "}"
            filled = filled.replace(placeholder, value)

        # Remove any unfilled placeholders
        import re
        filled = re.sub(r'\{[^}]+\}', '[to be specified]', filled)

        return filled

    def _enhance_prompt(self, prompt: str, intent_result: IntentResult) -> str:
        """Add best practices and enhancements to the prompt."""
        enhancements = []

        # Add thinking process for complex tasks
        if intent_result.confidence < 0.7:
            enhancements.append(
                "Note: Please think through this request carefully and ask for clarification if needed."
            )

        # Add output format specification
        enhancements.append("\nOutput Format: Provide a clear, well-structured response.")

        # Combine
        enhanced = prompt
        if enhancements:
            enhanced += "\n\n" + "\n".join(enhancements)

        return enhanced

    # Helper methods for extraction (simplified - would be more sophisticated in production)

    def _extract_topic(self, text: str) -> str:
        """Extract main topic from text."""
        # Simplified: return text or generic
        words = text.split()
        if len(words) > 5:
            return " ".join(words[:10]) + "..."
        return text if text else "[topic to be specified]"

    def _extract_recipient(self, text: str) -> str:
        """Extract recipient from text."""
        recipients = {
            "מורה": "teacher",
            "מנהל": "manager",
            "להנהלה": "management",
            "עמית": "colleague",
            "לקוח": "client"
        }

        for heb, eng in recipients.items():
            if heb in text:
                return eng

        return "[recipient]"

    def _extract_purpose(self, text: str) -> str:
        """Extract email purpose."""
        return text if text else "[purpose to be specified]"

    def _detect_content_type(self, text: str) -> str:
        """Detect type of creative content."""
        if "סיפור" in text:
            return "a story"
        elif "שיר" in text:
            return "a poem"
        elif "תיאור" in text:
            return "a description"
        else:
            return "creative content"

    def _detect_target_language(self, text: str) -> str:
        """Detect target translation language."""
        if "אנגלית" in text or "english" in text.lower():
            return "English"
        elif "עברית" in text or "hebrew" in text.lower():
            return "Hebrew"
        else:
            return "English"

    def get_available_templates(self) -> List[Dict]:
        """Get list of all available templates."""
        return [
            {
                "intent": data["intent"],
                "name": data["name"],
                "description": data["description"]
            }
            for data in self.templates.values()
        ]

    def get_template_by_intent(self, intent: str) -> Optional[Dict]:
        """Get specific template by intent."""
        return self.templates.get(intent)
