"""
Demo script for Engineered Prompt system (UPGRADED VERSION)
Demonstrates the new focused template workflow: Visual, Textual, Technical
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.prompt_generator import PromptGenerator
from src.database import PromptDatabase
from src.task_classifier import TaskClassifier
import config


def print_separator():
    """Print a visual separator."""
    print("\n" + "="*80 + "\n")


def demo():
    """Run the upgraded demo with 3 focused templates."""
    print("🎯 Engineered Prompt - UPGRADED Demo\n")
    print("מערכת המרת טקסט עברי לפרומפטים ממוקדים")
    print("🎨 Visual | 📝 Textual | 💻 Technical\n")
    print_separator()

    # Initialize components
    print("🔧 מאתחל רכיבי מערכת...")
    generator = PromptGenerator(config.TEMPLATES_DIR)
    db = PromptDatabase(config.DATABASE_URL)
    classifier = TaskClassifier()

    print(f"✓ נטענו {len(generator.get_available_templates())} טמפלטים ממוקדים")
    print("✓ מסד נתונים מוכן")
    print("✓ מסווג משימות מוכן")

    print_separator()

    # Demo examples - one for each template type
    examples = [
        {
            "title": "דוגמה 1: 🎨 חזותי (Visual)",
            "text": "צור תמונה של חתול בחלל עם תאורה דרמטית ואיכות 4K",
            "context": "לפרויקט מדע בדיוני",
            "instructions": "ריאליסטי ככל האפשר",
            "expected_type": "visual"
        },
        {
            "title": "דוגמה 2: 📝 טקסטואלי (Textual)",
            "text": "כתוב מייל רשמי למנהל לבקש חופשה לשבוע הבא",
            "context": "עובד במשך 3 שנים ללא חופשה",
            "instructions": "שמור על טון מקצועי ומכבד",
            "expected_type": "textual"
        },
        {
            "title": "דוגמה 3: 💻 טכני (Technical)",
            "text": "תכנת פונקציה בפייתון למיון רשימה של מספרים באופן מהיר",
            "context": "לעבודה עם רשימות גדולות",
            "instructions": "אופטימיזציה לביצועים",
            "expected_type": "technical"
        }
    ]

    for i, example in enumerate(examples, 1):
        emoji = {"visual": "🎨", "textual": "📝", "technical": "💻"}.get(example['expected_type'], "📋")
        print(f"{emoji} {example['title']}")
        print(f"{'─'*80}")
        print(f"\n📥 קלט עברי:")
        print(f'   "{example["text"]}"')
        if example['context']:
            print(f'\n📌 הקשר: "{example["context"]}"')
        if example['instructions']:
            print(f'📌 הוראות: "{example["instructions"]}"')
        print()

        # Classify task
        task_result = classifier.classify_task(example["text"])
        print(f"🔍 סיווג משימה:")
        print(f"   • סוג: {task_result.task_type}")
        print(f"   • ביטחון: {task_result.confidence:.0%}")
        if task_result.metadata.get('matched_keywords'):
            print(f"   • מילות מפתח: {', '.join(task_result.metadata['matched_keywords'][:3])}")
        print()

        # Generate prompt with context and instructions
        result = generator.generate(
            example["text"],
            context=example['context'],
            instructions=example['instructions']
        )

        print(f"✨ פרומפט שנוצר:")
        print(f"   טמפלט: {result.template_used}")
        print()
        print("─" * 80)
        print(result.prompt)
        print("─" * 80)
        print()

        # Save to database
        prompt_id = db.save_prompt(
            input_text=example["text"],
            detected_intent=result.task_type,
            generated_prompt=result.prompt,
            detected_style=str(result.metadata.get("style", {})),
            metadata=result.metadata
        )
        print(f"💾 נשמר במסד נתונים (ID: {prompt_id})")

        # Simulate feedback
        feedback_ratings = [
            ("good", 5.0),
            ("good", 4.5),
            ("good", 5.0)
        ]
        feedback, rating = feedback_ratings[i-1]
        db.update_feedback(prompt_id, feedback, rating)
        print(f"⭐ משוב סימולציה: {feedback} ({rating}/5.0)")

        print_separator()

    # Show statistics
    print("📊 סטטיסטיקות מערכת:")
    stats = db.get_statistics()
    print(f"   • סך הכל פרומפטים: {stats['total_prompts']}")
    print(f"   • דירוג ממוצע: {stats['average_rating']:.1f}/5.0")
    print(f"   • סוגי משימות: {stats['total_intents']}")
    print(f"   • משימות זמינות: {', '.join(stats['intents'])}")

    print_separator()

    # Show best prompts per task type
    print("🏆 הפרומפטים הטובים ביותר לכל סוג:")

    for task_type in ["visual", "textual", "technical"]:
        emoji = {"visual": "🎨", "textual": "📝", "technical": "💻"}[task_type]
        best = db.get_best_prompts(task_type, min_rating=4.0, limit=1)
        if best:
            record = best[0]
            print(f"\n   {emoji} {task_type.upper()}")
            print(f"      ⭐ דירוג: {record['rating']}/5.0")
            print(f"      📝 {record['input_text'][:60]}...")

    print_separator()

    print("✅ Demo הושלם בהצלחה!")
    print("\n💡 שינויים עיקריים במערכת המשודרגת:")
    print("   • 3 טמפלטים ממוקדים (Visual, Textual, Technical)")
    print("   • שדות Context ו-Instructions נפרדים")
    print("   • סימון משתנים ב-$$ $$ במקום {}")
    print("   • הסרת הערות גנריות מיותרות")
    print("\n💻 כדי להריץ את הממשק המלא:")
    print("   streamlit run app.py")
    print()


if __name__ == "__main__":
    demo()
