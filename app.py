"""
Engineered Prompt - Streamlit Web Interface
Hebrew text to optimized prompts with focused templates
"""
import streamlit as st
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.prompt_generator import PromptGenerator, GeneratedPrompt
from src.database import PromptDatabase
from src.task_classifier import TaskClassifier
import config


# Page configuration
st.set_page_config(
    page_title="Engineered Prompt",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = PromptDatabase(config.DATABASE_URL)

if 'generator' not in st.session_state:
    st.session_state.generator = PromptGenerator(config.TEMPLATES_DIR)

if 'current_prompt_id' not in st.session_state:
    st.session_state.current_prompt_id = None

if 'generated_prompt' not in st.session_state:
    st.session_state.generated_prompt = None


def main():
    """Main application function."""

    # Header
    st.title("🎯 Engineered Prompt")
    st.markdown("### מערכת המרת טקסט עברי לפרומפטים ממוקדים")
    st.markdown("**3 סוגי טמפלטים:** חזותי (Visual) | טקסטואלי (Textual) | טכני (Technical)")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("📊 מידע")

        # Statistics
        try:
            stats = st.session_state.db.get_statistics()
            st.metric("סך הכל פרומפטים", stats["total_prompts"])
            st.metric("דירוג ממוצע", f"{stats['average_rating']:.1f}/5.0")
            st.metric("סוגי משימות", stats["total_intents"])

            if stats["intents"]:
                st.write("**סוגי משימות:**")
                for task_type in stats["intents"]:
                    emoji = {"visual": "🎨", "textual": "📝", "technical": "💻"}.get(task_type, "📋")
                    st.write(f"{emoji} {task_type}")
        except Exception as e:
            st.error(f"שגיאה בטעינת סטטיסטיקות: {e}")

        st.markdown("---")

        # View History
        if st.button("📜 הצג היסטוריה", use_container_width=True):
            st.session_state.show_history = True

        # Available Templates
        with st.expander("📋 טמפלטים זמינים"):
            templates = st.session_state.generator.get_available_templates()
            for template in templates:
                emoji = {"visual": "🎨", "textual": "📝", "technical": "💻"}.get(template['task_type'], "📋")
                st.write(f"{emoji} **{template['name']}**")
                st.caption(template['description'])
                st.write("")

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 קלט")

        # Task type selector (optional override)
        classifier = TaskClassifier()
        task_types_hebrew = {
            "אוטומטי (זיהוי אוטומטי)": None,
            "🎨 חזותי (Visual)": "visual",
            "📝 טקסטואלי (Textual)": "textual",
            "💻 טכני (Technical)": "technical"
        }

        selected_task_hebrew = st.selectbox(
            "סוג משימה (אופציונלי)",
            list(task_types_hebrew.keys()),
            help="השאר 'אוטומטי' לזיהוי אוטומטי של סוג המשימה"
        )

        selected_task = task_types_hebrew[selected_task_hebrew]

        # Text input
        hebrew_input = st.text_area(
            "הכנס טקסט בעברית:",
            height=150,
            placeholder="דוגמאות:\n• צור תמונה של חתול בחלל\n• כתוב מייל למנהל לבקש חופשה\n• תכנת פונקציה בפייתון למיון רשימה",
            help="כתוב בעברית מה אתה רוצה ליצור"
        )

        # Context input (new!)
        with st.expander("⚙️ הגדרות מתקדמות (אופציונלי)"):
            context_input = st.text_area(
                "הקשר נוסף (Context):",
                height=80,
                placeholder="הקשר נוסף או רקע למשימה...",
                help="מידע נוסף שעוזר להבין את ההקשר"
            )

            instructions_input = st.text_area(
                "הוראות מיוחדות (Special Instructions):",
                height=80,
                placeholder="הוראות ספציפיות, אילוצים, או דרישות מיוחדות...",
                help="הוראות או דרישות ספציפיות למשימה"
            )

        # Generate button
        generate_col1, generate_col2 = st.columns([3, 1])

        with generate_col1:
            generate_button = st.button(
                "🚀 צור פרומפט",
                type="primary",
                use_container_width=True,
                disabled=not hebrew_input.strip()
            )

        with generate_col2:
            clear_button = st.button("🗑️ נקה", use_container_width=True)

        if clear_button:
            st.rerun()

        # Generate prompt
        if generate_button and hebrew_input.strip():
            with st.spinner("מייצר פרומפט..."):
                try:
                    # Generate with context and instructions
                    result = st.session_state.generator.generate(
                        hebrew_input,
                        context=context_input.strip(),
                        instructions=instructions_input.strip(),
                        override_task=selected_task
                    )

                    # Save to database
                    prompt_id = st.session_state.db.save_prompt(
                        input_text=hebrew_input,
                        detected_intent=result.task_type,
                        generated_prompt=result.prompt,
                        detected_style=str(result.metadata.get("style", {})),
                        metadata=result.metadata
                    )

                    # Store in session
                    st.session_state.generated_prompt = result
                    st.session_state.current_prompt_id = prompt_id

                    st.success("✅ פרומפט נוצר בהצלחה!")

                except Exception as e:
                    st.error(f"❌ שגיאה ביצירת פרומפט: {e}")
                    import traceback
                    st.code(traceback.format_exc())

    with col2:
        st.header("✨ פלט - פרומפט מובנה")

        if st.session_state.generated_prompt:
            result = st.session_state.generated_prompt

            # Metadata
            with st.expander("ℹ️ מטא-דאטה", expanded=False):
                meta_col1, meta_col2, meta_col3 = st.columns(3)
                with meta_col1:
                    emoji = {"visual": "🎨", "textual": "📝", "technical": "💻"}.get(result.task_type, "📋")
                    st.metric("סוג משימה", f"{emoji} {result.task_type}")
                with meta_col2:
                    st.metric("ביטחון", f"{result.confidence:.0%}")
                with meta_col3:
                    st.metric("טמפלט", result.template_used.split()[0])

                if result.metadata.get("matched_keywords"):
                    st.write("**מילות מפתח שזוהו:**")
                    st.write(", ".join(result.metadata["matched_keywords"][:5]))

                # Show detected variables
                if result.variables:
                    st.write("**משתנים שזוהו:**")
                    for key, value in result.variables.items():
                        if value and value != "[to be specified]":
                            st.write(f"• {key}: {value[:50]}{'...' if len(value) > 50 else ''}")

            # Generated prompt
            st.text_area(
                "הפרומפט שנוצר:",
                value=result.prompt,
                height=350,
                help="העתק את הפרומפט הזה לשימוש ב-LLM"
            )

            # Action buttons
            action_col1, action_col2, action_col3 = st.columns(3)

            with action_col1:
                if st.button("📋 העתק", use_container_width=True):
                    st.code(result.prompt, language=None)
                    st.success("הפרומפט מוצג למעלה - ניתן להעתיק")

            with action_col2:
                # Download
                st.download_button(
                    label="⬇️ הורד",
                    data=result.prompt,
                    file_name=f"prompt_{result.task_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with action_col3:
                if st.button("🔄 נסה שוב", use_container_width=True):
                    st.session_state.generated_prompt = None
                    st.rerun()

            # Feedback section
            st.markdown("---")
            st.subheader("💭 משוב")

            feedback_col1, feedback_col2 = st.columns([2, 1])

            with feedback_col1:
                rating = st.select_slider(
                    "דרג את איכות הפרומפט:",
                    options=[1, 2, 3, 4, 5],
                    value=3,
                    format_func=lambda x: "⭐" * x
                )

            with feedback_col2:
                feedback_type = st.selectbox(
                    "סוג משוב:",
                    ["neutral", "good", "bad"],
                    format_func=lambda x: {"good": "👍 טוב", "bad": "👎 לא טוב", "neutral": "😐 ניטרלי"}[x]
                )

            if st.button("שלח משוב", type="secondary", use_container_width=True):
                if st.session_state.current_prompt_id:
                    success = st.session_state.db.update_feedback(
                        st.session_state.current_prompt_id,
                        feedback_type,
                        float(rating)
                    )
                    if success:
                        st.success("תודה על המשוב! 🙏")
                    else:
                        st.error("שגיאה בשמירת משוב")

        else:
            st.info("👈 הכנס טקסט בעברית בצד שמאל וצור פרומפט")

            # Show examples
            st.markdown("### 💡 דוגמאות לשימוש:")

            st.markdown("**🎨 חזותי (Visual):**")
            st.code("צור תמונה של חתול בחלל עם תאורה דרמטית")

            st.markdown("**📝 טקסטואלי (Textual):**")
            st.code("כתוב מייל רשמי למנהל לבקש חופשה לשבוע הבא")

            st.markdown("**💻 טכני (Technical):**")
            st.code("תכנת פונקציה בפייתון למיון רשימה באופן יעיל")

    # History view
    if st.session_state.get('show_history', False):
        st.markdown("---")
        st.header("📜 היסטוריית פרומפטים")

        try:
            history = st.session_state.db.get_prompt_history(limit=20)

            if history:
                for record in history:
                    task_emoji = {"visual": "🎨", "textual": "📝", "technical": "💻"}.get(
                        record['detected_intent'], "📋"
                    )
                    with st.expander(
                        f"{task_emoji} {record['detected_intent']} - {record['created_at'][:10]}"
                    ):
                        col_a, col_b = st.columns(2)

                        with col_a:
                            st.write("**טקסט מקורי:**")
                            st.text(record['input_text'][:200] + "..." if len(record['input_text']) > 200 else record['input_text'])

                        with col_b:
                            st.write("**משוב:**")
                            if record['rating']:
                                st.write(f"דירוג: {'⭐' * int(record['rating'])}")
                            if record['user_feedback']:
                                st.write(f"סוג: {record['user_feedback']}")

                        st.write("**פרומפט שנוצר:**")
                        st.code(record['generated_prompt'][:300] + "..." if len(record['generated_prompt']) > 300 else record['generated_prompt'])

            else:
                st.info("אין עדיין היסטוריה")

        except Exception as e:
            st.error(f"שגיאה בטעינת היסטוריה: {e}")

        if st.button("סגור היסטוריה"):
            st.session_state.show_history = False
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: gray;'>
        <small>Engineered Prompt v{config.APP_VERSION} |
        3 Focused Templates: Visual • Textual • Technical |
        Built with Streamlit ✨</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
