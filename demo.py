"""
Demo script for Engineered Prompt system
Demonstrates the full workflow from Hebrew input to generated prompt
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.prompt_generator import PromptGenerator
from src.database import PromptDatabase
from src.intent_detector import IntentDetector
import config


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*80 + "\n")


def demo():
    """Run the demo."""
    print("🎯 Engineered Prompt - Demo\n")
    print("מערכת המרת טקסט עברי לפרומפט מובנה\n")
    print_separator()

    # Initialize components
    print("🔧 מאתחל רכיבי מערכת...")
    generator = PromptGenerator(config.TEMPLATES_DIR)
    db = PromptDatabase(config.DATABASE_URL)
    detector = IntentDetector()

    print(f"✓ נטענו {len(generator.get_available_templates())} תבניות")
    print("✓ מסד נתונים מוכן")
    print("✓ מזהה כוונות מוכן")

    print_separator()

    # Demo examples
    examples = [
        {
            "title": "דוגמה 1: מכתב רשמי",
            "text": "כתוב לי מכתב רשמי למורה של בני על איחור חוזר של התלמיד לשיעורים בגלל בעיות תחבורה",
            "emoji": "📝"
        },
        {
            "title": "דוגמה 2: כתיבה יצירתית",
            "text": "כתוב לי סיפור קצר ויצירתי על רובוט שמגלה רגשות לראשונה",
            "emoji": "✨"
        },
        {
            "title": "דוגמה 3: אימייל עבודה",
            "text": "שלח מייל קצר לעמית בעבודה לבקש עזרה בפרויקט החדש",
            "emoji": "📧"
        },
        {
            "title": "דוגמה 4: תרגום",
            "text": "תרגם לאנגלית באופן רשמי: שלום, אני רוצה לקבוע פגישה",
            "emoji": "🌐"
        }
    ]

    for i, example in enumerate(examples, 1):
        print(f"{example['emoji']} {example['title']}")
        print(f"{'─'*80}")
        print(f"\n📥 קלט עברי:")
        print(f'   "{example["text"]}"')
        print()

        # Detect intent
        intent_result = detector.detect_intent(example["text"])
        print(f"🔍 זיהוי כוונה:")
        print(f"   • כוונה: {intent_result.intent}")
        print(f"   • ביטחון: {intent_result.confidence:.0%}")
        print(f"   • סגנון: רשמיות={intent_result.style['formality']}, טון={intent_result.style['tone']}, אורך={intent_result.style['length']}")
        if intent_result.metadata.get('matched_keywords'):
            print(f"   • מילות מפתח: {', '.join(intent_result.metadata['matched_keywords'][:3])}")
        print()

        # Generate prompt
        result = generator.generate(example["text"])
        print(f"✨ פרומפט שנוצר:")
        print(f"   תבנית: {result.template_used}")
        print()
        print("─" * 80)
        print(result.prompt)
        print("─" * 80)
        print()

        # Save to database
        prompt_id = db.save_prompt(
            input_text=example["text"],
            detected_intent=result.intent,
            generated_prompt=result.prompt,
            detected_style=str(result.metadata.get("style", {})),
            metadata=result.metadata
        )
        print(f"💾 נשמר במסד נתונים (ID: {prompt_id})")

        # Simulate feedback
        feedback = ["good", "good", "neutral", "good"][i-1]
        rating = [5.0, 4.5, 3.5, 5.0][i-1]
        db.update_feedback(prompt_id, feedback, rating)
        print(f"⭐ משוב סימולציה: {feedback} ({rating}/5.0)")

        print_separator()

    # Show statistics
    print("📊 סטטיסטיקות מערכת:")
    stats = db.get_statistics()
    print(f"   • סך הכל פרומפטים: {stats['total_prompts']}")
    print(f"   • דירוג ממוצע: {stats['average_rating']:.1f}/5.0")
    print(f"   • סוגי כוונות: {stats['total_intents']}")
    print(f"   • כוונות זמינות: {', '.join(stats['intents'])}")

    print_separator()

    # Show history
    print("📜 היסטוריה אחרונה:")
    history = db.get_prompt_history(limit=3)
    for record in history[:3]:
        print(f"\n   🎯 {record['detected_intent']}")
        print(f"      קלט: {record['input_text'][:60]}...")
        if record['rating']:
            print(f"      דירוג: {'⭐' * int(record['rating'])} ({record['rating']}/5.0)")

    print_separator()

    # Show best prompts for a specific intent
    print("🏆 הפרומפטים הטובים ביותר (formal_letter):")
    best = db.get_best_prompts("formal_letter", min_rating=4.0, limit=2)
    for record in best:
        print(f"\n   ⭐ דירוג: {record['rating']}/5.0")
        print(f"      {record['input_text'][:60]}...")

    print_separator()

    print("✅ Demo הושלם בהצלחה!")
    print("\n💡 כדי להריץ את הממשק המלא:")
    print("   streamlit run app.py")
    print()


if __name__ == "__main__":
    demo()
