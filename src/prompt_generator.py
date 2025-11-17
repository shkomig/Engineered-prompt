"""Prompt generation engine - creates optimized prompts from focused templates."""
import json
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

from .task_classifier import TaskClassifier, TaskResult


@dataclass
class GeneratedPrompt:
    """Result of prompt generation."""
    prompt: str
    template_used: str
    task_type: str
    confidence: float
    variables: Dict[str, str]
    metadata: Dict


class PromptGenerator:
    """Main prompt generation engine with focused templates."""

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
        self.classifier = TaskClassifier()

    def _load_templates(self) -> Dict[str, Dict]:
        """Load all template files from templates directory."""
        templates = {}

        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")

        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    task_type = template_data.get("task_type")
                    if task_type:
                        templates[task_type] = template_data
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")

        return templates

    def generate(
        self,
        hebrew_text: str,
        context: str = "",
        instructions: str = "",
        override_task: Optional[str] = None
    ) -> GeneratedPrompt:
        """
        Generate an optimized prompt from Hebrew text.

        Args:
            hebrew_text: Input text in Hebrew
            context: Additional context (optional)
            instructions: Special instructions (optional)
            override_task: Optional task type override (visual/textual/technical)

        Returns:
            GeneratedPrompt object with the generated prompt and metadata
        """
        # Classify task type
        task_result = self.classifier.classify_task(hebrew_text)

        # Use override if provided
        final_task = override_task if override_task else task_result.task_type

        # Ensure task type is supported
        if final_task not in self.templates:
            final_task = "textual"  # Default to textual

        # Get template
        template_data = self.templates[final_task]

        # Extract variables from input text
        variables = self._extract_variables(
            hebrew_text,
            task_result,
            template_data,
            context,
            instructions
        )

        # Generate prompt from template
        prompt = self._fill_template(template_data["template"], variables)

        return GeneratedPrompt(
            prompt=prompt,
            template_used=template_data["name"],
            task_type=final_task,
            confidence=task_result.confidence,
            variables=variables,
            metadata={
                "style": task_result.style,
                "matched_keywords": task_result.metadata.get("matched_keywords", []),
                "original_text": hebrew_text
            }
        )

    def _extract_variables(
        self,
        text: str,
        task_result: TaskResult,
        template_data: Dict,
        context: str,
        instructions: str
    ) -> Dict[str, str]:
        """
        Extract variables from text to fill template.
        """
        variables = {}
        task_type = task_result.task_type
        style = task_result.style

        # Always include context and instructions
        variables["context"] = context if context else "[to be specified]"
        variables["instructions"] = instructions if instructions else "[to be specified]"

        if task_type == "visual":
            # Visual template variables
            variables["subject"] = self._extract_subject(text)
            variables["visual_style"] = self._detect_visual_style(text)
            variables["lighting"] = "[to be specified]"
            variables["composition"] = "[to be specified]"
            variables["quality"] = self._detect_quality(text)

        elif task_type == "textual":
            # Textual template variables
            variables["purpose"] = self._extract_purpose(text)
            variables["recipient"] = self._extract_recipient(text)
            variables["tone"] = self._map_tone(style.get("tone", "neutral"), style.get("formality", "neutral"))
            variables["length"] = self._map_length(style.get("length", "moderate"))
            variables["key_points"] = self._extract_key_points(text)

        elif task_type == "technical":
            # Technical template variables
            variables["language"] = self._detect_language(text)
            variables["environment"] = self._detect_environment(text)
            variables["functionality"] = self._extract_functionality(text)
            variables["optimization"] = self._detect_optimization(text)

        return variables

    def _fill_template(self, template: str, variables: Dict[str, str]) -> str:
        """Fill template with variables using $$ $$ markers."""
        filled = template

        for key, value in variables.items():
            placeholder = "$$" + key + "$$"
            filled = filled.replace(placeholder, value)

        # Remove any unfilled placeholders (leave [to be specified] as is)
        import re
        filled = re.sub(r'\$\$[^$]+\$\$', '[to be specified]', filled)

        return filled

    # Helper methods for variable extraction

    def _extract_subject(self, text: str) -> str:
        """Extract main subject from text for visual prompts."""
        # Remove common instruction words
        clean_text = text.replace("צור", "").replace("תמונה", "").replace("של", "").strip()
        return clean_text if clean_text else "[to be specified]"

    def _detect_visual_style(self, text: str) -> str:
        """Detect visual style from text."""
        styles = {
            "ריאליסטי": "Photo-realistic",
            "אמנות דיגיטלית": "Digital Art",
            "סקיצה": "Concept Sketch",
            "3d": "3D Render",
            "צבעי מים": "Watercolor",
            "מינימליסטי": "Minimalist"
        }

        for heb, eng in styles.items():
            if heb in text.lower():
                return eng

        return "[to be specified]"

    def _detect_quality(self, text: str) -> str:
        """Detect quality requirements."""
        if "4k" in text.lower() or "גבוהה" in text:
            return "4K, Ultra Detailed"
        elif "קולנועי" in text or "cinematic" in text.lower():
            return "Cinematic, Professional Grade"
        return "[to be specified]"

    def _extract_purpose(self, text: str) -> str:
        """Extract purpose from textual request."""
        purposes = {
            "סכם": "Summarize",
            "הסבר": "Explain",
            "בקש": "Request",
            "דווח": "Report",
            "שכנע": "Persuade",
            "מידע": "Inform"
        }

        for heb, eng in purposes.items():
            if heb in text:
                return eng

        return "[to be specified]"

    def _extract_recipient(self, text: str) -> str:
        """Extract recipient from text."""
        recipients = {
            "מורה": "Teacher",
            "מנהל": "Boss/Manager",
            "עמית": "Colleague",
            "לקוח": "Customer",
            "קהל": "General Audience"
        }

        for heb, eng in recipients.items():
            if heb in text:
                return eng

        return "[to be specified]"

    def _map_tone(self, tone: str, formality: str) -> str:
        """Map detected tone and formality to English description."""
        tone_map = {
            "professional": "Professional",
            "friendly": "Friendly",
            "urgent": "Urgent",
            "persuasive": "Persuasive",
            "informative": "Informative"
        }

        formality_map = {
            "formal": "Formal",
            "casual": "Casual",
            "neutral": "Professional"
        }

        mapped_tone = tone_map.get(tone, formality_map.get(formality, "Professional"))
        return mapped_tone

    def _map_length(self, length: str) -> str:
        """Map length preference to English description."""
        length_map = {
            "concise": "Concise (1-2 paragraphs)",
            "moderate": "Moderate (3-5 paragraphs)",
            "extensive": "Extensive (1000+ words)"
        }

        return length_map.get(length, "Moderate (3-5 paragraphs)")

    def _extract_key_points(self, text: str) -> str:
        """Extract key points to cover."""
        # For now, return the original request
        # In production, this could use NLP to extract specific points
        return text if text else "[to be specified]"

    def _detect_language(self, text: str) -> str:
        """Detect programming language from text."""
        languages = {
            "פייתון": "Python",
            "python": "Python",
            "javascript": "JavaScript",
            "js": "JavaScript",
            "java": "Java",
            "sql": "SQL",
            "c++": "C++",
            "bash": "Bash",
            "latex": "LaTeX"
        }

        text_lower = text.lower()
        for key, lang in languages.items():
            if key in text_lower:
                return lang

        return "[to be specified]"

    def _detect_environment(self, text: str) -> str:
        """Detect framework/environment from text."""
        environments = {
            "react": "React",
            "django": "Django",
            "flask": "Flask",
            "node": "Node.js",
            "jupyter": "Jupyter Notebook",
            "console": "Console Only"
        }

        text_lower = text.lower()
        for key, env in environments.items():
            if key in text_lower:
                return env

        return "[to be specified]"

    def _extract_functionality(self, text: str) -> str:
        """Extract required functionality."""
        # Return the original request as functionality description
        return text if text else "[to be specified]"

    def _detect_optimization(self, text: str) -> str:
        """Detect optimization requirements."""
        optimizations = {
            "מהיר": "Optimize for speed",
            "קריא": "Optimize for readability",
            "זיכרון": "Optimize for low memory usage",
            "ביצועים": "Optimize for performance"
        }

        for heb, eng in optimizations.items():
            if heb in text:
                return eng

        return "Optimize for readability"

    def get_available_templates(self) -> list:
        """Get list of all available templates."""
        return [
            {
                "task_type": data["task_type"],
                "name": data["name"],
                "description": data["description"]
            }
            for data in self.templates.values()
        ]

    def get_template_by_task(self, task_type: str) -> Optional[Dict]:
        """Get specific template by task type."""
        return self.templates.get(task_type)
