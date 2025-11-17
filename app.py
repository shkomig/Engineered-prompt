"""
Engineered Prompt - Streamlit Web Interface
Hebrew text to optimized prompts with hindsight learning
"""
import streamlit as st
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.prompt_generator import PromptGenerator, GeneratedPrompt
from src.database import PromptDatabase
from src.intent_detector import IntentDetector
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
    st.markdown("### המרת טקסט עברי לפרומפט מובנה ואופטימלי")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("📊 מידע")

        # Statistics
        try:
            stats = st.session_state.db.get_statistics()
            st.metric("סך הכל פרומפטים", stats["total_prompts"])
            st.metric("דירוג ממוצע", f"{stats['average_rating']:.1f}/5.0")
            st.metric("סוגי כוונות", stats["total_intents"])

            if stats["intents"]:
                st.write("**כוונות נתמכות:**")
                for intent in stats["intents"]:
                    st.write(f"- {intent}")
        except Exception as e:
            st.error(f"שגיאה בטעינת סטטיסטיקות: {e}")

        st.markdown("---")

        # View History
        if st.button("📜 הצג היסטוריה", use_container_width=True):
            st.session_state.show_history = True

        # Available Templates
        with st.expander("📋 תבניות זמינות"):
            templates = st.session_state.generator.get_available_templates()
            for template in templates:
                st.write(f"**{template['name']}**")
                st.caption(template['description'])
                st.write("")

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 קלט - טקסט עברי")

        # Intent selector (optional override)
        detector = IntentDetector()
        all_intents = ["אוטומטי (זיהוי אוטומטי)"] + detector.get_supported_intents()

        selected_intent = st.selectbox(
            "סוג כוונה (אופציונלי)",
            all_intents,
            help="השאר 'אוטומטי' לזיהוי אוטומטי של הכוונה"
        )

        # Text input
        hebrew_input = st.text_area(
            "הכנס טקסט בעברית:",
            height=250,
            placeholder="לדוגמה: כתוב לי מכתב רשמי למורה על איחור של תלמיד...",
            help="כתוב בעברית מה אתה רוצה ליצור"
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
                    # Determine intent override
                    intent_override = None if selected_intent.startswith("אוטומטי") else selected_intent

                    # Generate
                    result = st.session_state.generator.generate(
                        hebrew_input,
                        override_intent=intent_override
                    )

                    # Save to database
                    prompt_id = st.session_state.db.save_prompt(
                        input_text=hebrew_input,
                        detected_intent=result.intent,
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

    with col2:
        st.header("✨ פלט - פרומפט מובנה")

        if st.session_state.generated_prompt:
            result = st.session_state.generated_prompt

            # Metadata
            with st.expander("ℹ️ מטא-דאטה", expanded=False):
                meta_col1, meta_col2, meta_col3 = st.columns(3)
                with meta_col1:
                    st.metric("כוונה", result.intent)
                with meta_col2:
                    st.metric("ביטחון", f"{result.confidence:.0%}")
                with meta_col3:
                    st.metric("תבנית", result.template_used.split()[0])

                if result.metadata.get("matched_keywords"):
                    st.write("**מילות מפתח שזוהו:**")
                    st.write(", ".join(result.metadata["matched_keywords"]))

            # Generated prompt
            st.text_area(
                "הפרומפט שנוצר:",
                value=result.prompt,
                height=300,
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
                    file_name=f"prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
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

    # History view
    if st.session_state.get('show_history', False):
        st.markdown("---")
        st.header("📜 היסטוריית פרומפטים")

        try:
            history = st.session_state.db.get_prompt_history(limit=20)

            if history:
                for record in history:
                    with st.expander(
                        f"🎯 {record['detected_intent']} - {record['created_at'][:10]}"
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
        Built with Streamlit |
        Hindsight Learning Enabled ✨</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
