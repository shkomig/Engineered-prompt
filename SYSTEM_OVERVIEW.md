# 📋 סקירת מערכת - Engineered Prompt

## 📊 סטטוס המערכת
✅ **מערכת פעילה ותפעולית**  
**גרסה:** 0.1.0  
**תאריך עדכון:** November 17, 2025

---

## 🎯 מטרת המערכת

המערכת מאפשרת המרת טקסט חופשי בעברית לפרומפט מובנה ברמה גבוהה, מעוצב לשימוש אופטימלי עם מודלי שפה (LLMs). המערכת משלבת:

- **זיהוי כוונה** (Intent Recognition) - מזהה מה תרצה האדם לכתוב
- **זיהוי סגנון** (Style Detection) - מבחינה בין רשמי, יצירתי, קליל וכו'
- **יצירת פרומפט** (Prompt Generation) - בונה פרומפט מובנה
- **למידה בדיעבד** (Hindsight Learning) - משתפרת מתוך feedback

---

## 🏗️ ארכיטקטורת המערכת

```
┌─────────────────────────────────────────┐
│   Streamlit Web Interface (app.py)      │
│   - קלט טקסט עברי                      │
│   - בחירת סוג כוונה (אופציונלי)        │
│   - הצגת פרומפט שנוצר                  │
│   - עמודים פידבק                       │
└──────────────┬──────────────────────────┘
               │
      ┌────────┴─────────┐
      │                  │
      ▼                  ▼
┌──────────────────┐  ┌──────────────────────┐
│ Intent Detector  │  │ Prompt Generator     │
│ ─────────────────│  │ ──────────────────── │
│ • Keyword match  │  │ • Template selection │
│ • Pattern detect │  │ • Variable filling   │
│ • Style infer    │  │ • Prompt building    │
└────────┬─────────┘  └──────────┬───────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │  Template Library      │
         │ ────────────────────── │
         │ • formal_letter.json   │
         │ • creative_writing.json│
         │ • email.json           │
         │ • summary.json         │
         │ • translation.json     │
         │ • question_answer.json │
         │ • business_proposal.json
         │ • general.json         │
         └────────────┬───────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │  Prompt Database       │
         │ ────────────────────── │
         │ • Save prompts         │
         │ • Store feedback       │
         │ • Retrieve history     │
         │ • Generate stats       │
         └────────────────────────┘
```

---

## 📁 מבנה הקבצים

```
Engineered-prompt/
│
├── app.py                           # ממשק Streamlit ראשי
├── config.py                        # קונפיגורציה כללית
├── requirements.txt                 # תלויויות Python
├── .env.example                     # דוגמה לקובץ environment
│
├── src/
│   ├── __init__.py
│   ├── intent_detector.py          # מודול זיהוי כוונה
│   ├── prompt_generator.py         # מנוע יצירת פרומפטים
│   ├── database.py                 # מודול database
│   │
│   └── templates/                  # ספריית תבניות JSON
│       ├── formal_letter.json       # תבנית מכתבים רשמיים
│       ├── creative_writing.json    # תבנית כתיבה יצירתית
│       ├── email.json               # תבנית דוא"ל
│       ├── summary.json             # תבנית סיכומים
│       ├── translation.json         # תבנית תרגומים
│       ├── question_answer.json     # תבנית שאלות ותשובות
│       ├── business_proposal.json   # תבנית הצעות עסקיות
│       └── general.json             # תבנית כללית
│
├── tests/                           # יחידות בדיקה
├── hindsight-prompting-research.md # מחקר מקיף
├── Plan.md                          # תוכנית הפיתוח
└── README.md                        # תיעוד

```

---

## 🔧 מודולים עיקריים

### 1. **Intent Detector** (`src/intent_detector.py`)
```python
Class: IntentDetector
Supported Intents:
  • formal_letter       - מכתבים רשמיים
  • creative_writing    - כתיבה יצירתית
  • email               - הודעות דוא"ל
  • summary             - סיכומים וקצורים
  • translation         - תרגומים
  • question_answer     - שאלות ותשובות
  • business_proposal   - הצעות עסקיות
```

**תכונות:**
- זיהוי ככוונה based on keywords (עברית)
- זיהוי סגנון (רשמי/קליל)
- זיהוי טון (חיובי/שלילי)
- scoring ודירוג ביטחון

### 2. **Prompt Generator** (`src/prompt_generator.py`)
```python
Class: PromptGenerator
Methods:
  • generate()              - יצירת פרומפט מיטבי
  • get_available_templates() - רשימת תבניות
  • apply_style()           - יישום סגנון
```

**תכונות:**
- טעינת תבניות מ-JSON
- שילוב intent + style + constraints
- מילוי משתנים בתבנית
- הוספת best practices

### 3. **Database Module** (`src/database.py`)
```python
Class: PromptDatabase
Methods:
  • save_prompt()      - שמירת פרומפט בדאטאבייס
  • update_feedback()  - עדכון feedback משתמש
  • get_history()      - קבלת היסטוריה
  • get_statistics()   - סטטיסטיקות
```

**אחסון:**
- SQLite (local) / PostgreSQL (production)
- טבלה: `prompts`
- שדות: input_text, intent, prompt, feedback, rating, metadata

---

## 🚀 הוראות הפעלה

### 1. **התקנת תלויויות**
```bash
cd c:\Vs-Pro\Prompt_engineered\Engineered-prompt
pip install -r requirements.txt
```

### 2. **הגדרת Environment**
```bash
cp .env.example .env
# ערוך את .env עם ההגדרות שלך אם נדרש
```

### 3. **הפעלת האפליקציה**
```bash
streamlit run app.py
```

האפליקציה תפתח ב-browser בכתובת:
```
http://localhost:8501
```

---

## 💡 דוגמאות שימוש

### דוגמה 1: מכתב רשמי למורה
**קלט:**
```
כתוב לי מכתב רשמי למורה על איחור של תלמיד
```

**פלט (Prompt):**
```
You are a professional writer specializing in formal correspondence.

Task: Write a formal letter about student tardiness to teacher.

Requirements:
- Maintain a formal and respectful tone throughout
- Use appropriate formal language and structure
- Include proper greeting and closing
- Keep the length moderate
- Ensure clarity and professionalism

Context: A student has been arriving late to class

Please write the letter in a well-structured format with clear paragraphs.
```

### דוגמה 2: כתיבה יצירתית
**קלט:**
```
כתוב לי סיפור קצר על ילד שמגלה כוח קסום
```

**סוג כוונה שזוהה:** creative_writing  
**סגנון:** creative, imaginative

---

## 📊 כמויות נתמכות

| מדד | ערך |
|-----|------|
| **סוגי כוונה** | 7 סוגים |
| **תבניות** | 8 תבניות |
| **שפות קלט** | עברית |
| **שפות פלט** | אנגלית (עברית בעתיד) |
| **סוגי סגנון** | 4+ (רשמי, קליל, יצירתי, וכו') |

---

## 🎛️ פיצ'רים זמינים

### ✅ כרגע מוגבל
- [x] זיהוי כוונה
- [x] זיהוי סגנון
- [x] יצירת פרומפט
- [x] שמירה בדאטאבייס
- [x] feedback mechanism
- [x] היסטוריה
- [x] סטטיסטיקות
- [x] עדכון templates

### ⏳ בתוכניות
- [ ] תרגום אוטומטי לעברית
- [ ] fine-tuning מודל
- [ ] hindsight experience replay
- [ ] A/B testing
- [ ] advanced analytics
- [ ] export to file
- [ ] multi-language support

---

## 🔐 נתונים ומידע

### Database Schema
```sql
CREATE TABLE prompts (
    id INTEGER PRIMARY KEY,
    input_text TEXT NOT NULL,
    detected_intent VARCHAR(100) NOT NULL,
    detected_style VARCHAR(50),
    generated_prompt TEXT NOT NULL,
    user_feedback VARCHAR(20),
    rating FLOAT,
    metadata_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Feedback Options
- ✅ **Good** (טוב)
- ➖ **Neutral** (בינוני)
- ❌ **Bad** (גרוע)
- 📊 **Rating** (1-5)

---

## 📈 KPIs ומטרות

| מטרה | יעד | סטטוס |
|------|------|--------|
| Intent Recognition Accuracy | 95% | ⏳ בתהליך |
| Prompt Quality | 4.0+/5.0 | ⏳ בתהליך |
| Response Time | <2 seconds | ✅ מושג |
| User Adoption | 10+ users | ⏳ בתהליך |
| Code Coverage | 80%+ | ⏳ בתהליך |

---

## 🐛 Known Issues & Limitations

1. **שפה:** כרגע רק עברית לקלט
2. **תרגום:** לא מיושם תרגום אוטומטי לעברית
3. **Hindsight:** עדיין לא מיושמת למידה בדיעבד
4. **Templates:** מספר קטן של תבניות

---

## 📝 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Backend | Python 3.10+ |
| Database | SQLite (SQLAlchemy ORM) |
| Pattern Matching | Regex + Rule-based |
| Environment | .env (python-dotenv) |

---

## 🔄 Workflow זרימת עבודה

```
1. משתמש כותב טקסט בעברית
        │
        ▼
2. IntentDetector מזהה כוונה וסגנון
        │
        ▼
3. PromptGenerator בוחר תבנית מתאימה
        │
        ▼
4. ממלא משתנים ויוצר prompt
        │
        ▼
5. הצגת prompt למשתמש
        │
        ▼
6. משתמש מוקיד feedback
        │
        ▼
7. שמירה בדאטאבייס + סטטיסטיקות
```

---

## 📞 התקשרות ועזרה

לשאלות או בעיות:
1. בדוק את `README.md`
2. ראה דוגמאות ב-`Plan.md`
3. קרא מחקר בקובץ `hindsight-prompting-research.md`

---

**Last Updated:** November 17, 2025  
**Maintained by:** GitHub Copilot  
**Repository:** https://github.com/shkomig/Engineered-prompt
