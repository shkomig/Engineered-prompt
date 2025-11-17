# 🎨 Visual Guide - Engineered Prompt Interface

## Web Interface Layout

```
╔════════════════════════════════════════════════════════════════════════════╗
║                          🎯 Engineered Prompt                             ║
║                    המרת טקסט עברי לפרומפט מובנה                          ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────┬────────────────────────────────────────┐
│                                     │                                        │
│  SIDEBAR                            │  MAIN CONTENT (2 COLUMNS)              │
│  ═══════════════════════════════════│                                        │
│                                     │                                        │
│  📊 STATISTICS                      │  LEFT COLUMN: INPUT                    │
│  ├─ סך הכל: 42 פרומפטים            │  ═════════════════════════════════    │
│  ├─ דירוג: 4.2/5.0                │                                        │
│  └─ סוגים: 7                       │  📝 קלט - טקסט עברי                   │
│                                     │                                        │
│  📜 HISTORY                         │  [Dropdown: סוג כוונה]                │
│  └─ Show History                    │  ┌─────────────────────────────────┐ │
│     (will show 20 recent prompts)    │  │                                 │ │
│                                     │  │  הכנס טקסט בעברית...            │ │
│  📋 TEMPLATES                       │  │  [Large text area - 250px]       │ │
│  ├─ Formal Letter                   │  │                                 │ │
│  ├─ Creative Writing                │  │  דוגמה: כתוב לי מכתב...        │ │
│  ├─ Email                           │  │                                 │ │
│  ├─ Summary                         │  └─────────────────────────────────┘ │
│  ├─ Translation                     │                                        │
│  ├─ Q&A                             │  [🚀 צור פרומפט] [🗑️ נקה]           │
│  ├─ Business                        │                                        │
│  └─ General                         │                                        │
│                                     │  RIGHT COLUMN: OUTPUT                  │
└─────────────────────────────────────┤  ═════════════════════════════════    │
                                      │                                        │
                                      │  ✨ פלט - פרומפט מובנה               │
                                      │                                        │
                                      │  ℹ️ META-DATA (expandable)            │
                                      │  ├─ Intent: formal_letter             │
                                      │  ├─ Confidence: 92%                   │
                                      │  └─ Template: Formal...               │
                                      │                                        │
                                      │  ┌─────────────────────────────────┐  │
                                      │  │                                 │  │
                                      │  │  You are a professional writer..│  │
                                      │  │  Task: Write a formal letter... │  │
                                      │  │  Requirements: ...              │  │
                                      │  │  [Prompt text area - 300px]     │  │
                                      │  │                                 │  │
                                      │  └─────────────────────────────────┘  │
                                      │                                        │
                                      │  [📋 Copy] [⬇️ Download] [🔄 Retry]    │
                                      │                                        │
                                      │  ─────────────────────────────────    │
                                      │  💭 משוב                              │
                                      │                                        │
                                      │  דירוג: [⭐⭐⭐⭐⭐] 4/5               │
                                      │  סוג:   [dropdown: טוב/ניטרלי/לא טוב] │
                                      │                                        │
                                      │  [שלח משוב]                          │
                                      │                                        │
└─────────────────────────────────────┴────────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════════════════╗
║ Engineered Prompt v0.1.0 | Built with Streamlit | Hindsight Learning ✨   ║
╚════════════════════════════════════════════════════════════════════════════╝
```

---

## User Workflow Diagram

```
START
  │
  ├─→ Open http://localhost:8501
  │
  ├─→ Type Hebrew text in LEFT panel
  │   Example: "כתוב לי מכתב רשמי למורה על איחור של תלמיד"
  │
  ├─→ (Optional) Select specific intent type
  │   Or leave as "אוטומטי" for auto-detection
  │
  ├─→ Click "🚀 צור פרומפט" button
  │   ├─ System detects intent (formal_letter)
  │   ├─ Selects appropriate template
  │   └─ Generates optimized prompt
  │
  ├─→ View generated prompt in RIGHT panel
  │
  ├─→ Choose action:
  │   │
  │   ├─ 📋 Copy to clipboard
  │   │   └─ Use in ChatGPT/Claude/etc.
  │   │
  │   ├─ ⬇️ Download as .txt file
  │   │   └─ Save for later use
  │   │
  │   ├─ 🔄 Try again
  │   │   └─ Different intent or style
  │   │
  │   └─ 💭 Submit feedback
  │       ├─ Rate quality (1-5 stars)
  │       ├─ Select feedback type (Good/Neutral/Bad)
  │       └─ System learns from feedback
  │
  └─→ END (or repeat)
```

---

## Intent Detection Flow

```
Input Text (Hebrew)
  │
  ├─→ Check for keywords
  │   Examples:
  │   • "מכתב", "מורה" → formal_letter
  │   • "סיפור", "שיר" → creative_writing
  │   • "אימייל", "מייל" → email
  │   • "סיכום", "תמצית" → summary
  │   • "תרגם" → translation
  │   • "מה זה", "איך" → question_answer
  │   • "הצעה", "עסקים" → business_proposal
  │
  └─→ Calculate confidence score
      ├─ Strong match: 90-100%
      ├─ Good match: 70-89%
      └─ Weak match: <70% (use "general")
```

---

## Prompt Generation Pipeline

```
Step 1: Input Analysis
  ├─ Detect intent
  ├─ Detect style (formal/casual)
  ├─ Detect tone (positive/negative)
  └─ Extract key information

Step 2: Template Selection
  └─ Choose best-fit template based on intent

Step 3: Variable Extraction
  ├─ Topic
  ├─ Recipient
  ├─ Formality level
  ├─ Content length
  └─ Additional context

Step 4: Template Rendering
  ├─ Fill template variables
  ├─ Apply style modifications
  └─ Add best practices

Step 5: Output Generation
  └─ Return structured English prompt
```

---

## Data Flow Diagram

```
                         User Interface (Streamlit)
                              ▲       ▲
                              │       │
                         Input │       │ Generated Prompt
                              │       │
                              ▼       │
                     ┌─────────────────────────────┐
                     │  Prompt Generator            │
                     │  - Template selection        │
                     │  - Variable extraction       │
                     │  - Prompt building          │
                     └──────────┬───────────────────┘
                                │
                    Template → [selection]
                                │
                     ┌──────────▼──────────┐
                     │  Intent Detector    │
                     │  - Keyword matching │
                     │  - Style detection  │
                     └──────────┬──────────┘
                                │
                    Intent ← [detection]
                                │
                              Input
                                ▲
                                │
                    ┌───────────────────────────┐
                    │   Feedback Collection     │
                    │  Rating + Comment Storage │
                    └────────────┬──────────────┘
                                 │
                              (saves)
                                 │
                      ┌──────────▼──────────┐
                      │  SQLite Database    │
                      │  (prompts.db)       │
                      │  - History          │
                      │  - Feedback         │
                      │  - Statistics       │
                      └─────────────────────┘
```

---

## Template Structure

```
formal_letter.json
├─ intent: "formal_letter"
├─ name: "Formal Letter Template"
├─ description: "For official correspondence"
│
├─ template: "You are a professional writer...
│            Task: Write a formal letter about {topic}...
│            Constraints:
│            - Maintain {formality_level} tone..."
│
├─ variables: [
│  ├─ "topic" → extracted from input
│  ├─ "recipient" → extracted from input
│  ├─ "formality_level" → from style detection
│  ├─ "target_length" → from style detection
│  ├─ "context" → from input text
│  └─ "additional_instructions" → from metadata
│  ]
│
└─ examples: [
   ├─ { input: "...", output: "..." }
   └─ { input: "...", output: "..." }
   ]
```

---

## Feedback Loop

```
User Creates Prompt
  │
  ├─ Prompt saved to database with:
  │  ├─ Original Hebrew input
  │  ├─ Detected intent
  │  ├─ Generated prompt
  │  └─ Metadata
  │
  └─→ User rates & submits feedback
      ├─ Rating: 1-5 stars
      ├─ Type: Good/Neutral/Bad
      │
      └─→ Feedback saved to database
          │
          └─→ Used for future improvements:
              ├─ Template refinement
              ├─ Intent detection tuning
              └─ Quality metrics tracking
```

---

## Statistics Dashboard

```
📊 Statistics Panel (Sidebar)

┌─────────────────────────────┐
│ סך הכל פרומפטים             │
│      47                      │
└─────────────────────────────┘

┌─────────────────────────────┐
│ דירוג ממוצע                 │
│      4.2 / 5.0              │
└─────────────────────────────┘

┌─────────────────────────────┐
│ סוגי כוונות                 │
│      7                       │
└─────────────────────────────┘

כוונות נתמכות:
✓ formal_letter
✓ creative_writing
✓ email
✓ summary
✓ translation
✓ question_answer
✓ business_proposal
✓ general
```

---

## Color & Icon Legend

| Icon | Meaning |
|------|---------|
| 🎯 | System/Intent |
| 📝 | Input/Text |
| ✨ | Output/Generated |
| ℹ️ | Information |
| 📊 | Statistics |
| 📜 | History |
| 📋 | Templates |
| 🚀 | Action/Generate |
| 🗑️ | Clear |
| 📋 | Copy |
| ⬇️ | Download |
| 🔄 | Retry |
| 💭 | Feedback |
| ⭐ | Rating |
| 👍 | Good |
| 😐 | Neutral |
| 👎 | Bad |

---

## Example Interaction

### Scenario: Writing a Formal Letter

```
STEP 1: Input
┌──────────────────────────────────────────┐
│ כתוב לי מכתב רשמי למורה על איחור של    │
│ תלמיד. התלמיד אחר באופן קבוע.           │
│ עליי לרשום זאת בצורה מתאימה.            │
└──────────────────────────────────────────┘

STEP 2: System Processing
┌──────────────────────────────────────────┐
│ Intent Detector:                         │
│ ✓ Detected: formal_letter                │
│ ✓ Confidence: 95%                        │
│ ✓ Style: formal                          │
│ ✓ Tone: neutral                          │
└──────────────────────────────────────────┘

STEP 3: Template Selection
┌──────────────────────────────────────────┐
│ Selected Template: Formal Letter         │
│ Variables:                               │
│  • topic: student tardiness              │
│  • recipient: teacher                    │
│  • formality: formal                     │
│  • length: moderate                      │
└──────────────────────────────────────────┘

STEP 4: Generated Prompt
┌──────────────────────────────────────────┐
│ You are a professional writer.           │
│                                          │
│ Task: Write a formal letter about       │
│ student tardiness to teacher.           │
│                                          │
│ Requirements:                           │
│ - Maintain formal and respectful tone   │
│ - Use professional language             │
│ - Include proper greeting and closing   │
│ - Keep length moderate                  │
│ - Ensure clarity and professionalism    │
│                                          │
│ Context: Student has been arriving      │
│ late consistently.                      │
│                                          │
│ Please write in a well-structured       │
│ format with clear paragraphs.           │
└──────────────────────────────────────────┘

STEP 5: User Feedback
┌──────────────────────────────────────────┐
│ Rating: ⭐⭐⭐⭐⭐ (5/5)                  │
│ Feedback: Good 👍                        │
│ [שלח משוב]                              │
└──────────────────────────────────────────┘

Result: Prompt saved → System learns ✨
```

---

## Keyboard Shortcuts & Tips

| Action | How To |
|--------|--------|
| Generate Prompt | Click "🚀 צור פרומפט" or Enter in text area |
| Clear Input | Click "🗑️ נקה" button |
| Copy Prompt | Click "📋 Copy" button |
| Download | Click "⬇️ Download" button |
| Rate Prompt | Use star slider (1-5) |
| Submit Feedback | Click "שלח משוב" button |
| View History | Click "📜 הצג היסטוריה" in sidebar |
| Change Intent | Select from dropdown before generating |

---

## Mobile Responsiveness

The interface is optimized for:
- ✅ Desktop (1920x1080 and up)
- ✅ Laptop (1366x768)
- ⚠️ Tablet (limited - single column mode)
- ⚠️ Mobile (basic support - single column)

---

## Performance Indicators

```
Generation Time: 
┌────────────────────────────────────────┐
│████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ <500ms ✓
└────────────────────────────────────────┘

Database Operation:
┌────────────────────────────────────────┐
│████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ <100ms ✓
└────────────────────────────────────────┘

UI Responsiveness:
┌────────────────────────────────────────┐
│████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│ Instant ✓
└────────────────────────────────────────┘
```

---

**Last Updated:** November 17, 2025  
**Version:** 0.1.0  
**Status:** ✅ Ready to Use
