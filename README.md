# 🎯 Engineered Prompt (V2.0 - Focused Templates)

**המרת טקסט עברי חופשי לפרומפטים ממוקדים ומותאמים עבור LLMs**

מערכת חכמה שמקבלת טקסט בעברית ומייצרת פרומפט מקצועי ומותאם אופטימלית לשימוש עם מודלי שפה (LLMs). המערכת משתמשת ב-3 טמפלטים ממוקדים עם ב-Hindsight Learning כדי להשתפר עם הזמן.

## ✨ תכונות עיקריות (V2.0)

- 🎨 **3 טמפלטים ממוקדים** - Visual, Textual, Technical
- 🔍 **סיווג אוטומטי** - המערכת מסווגת את המשימה לסוג המתאים
- ⚙️ **שדות Context & Instructions** - הזן הקשר והוראות מיוחדות בנפרד
- 💾 **אינדקס והיסטוריה** - כל הפרומפטים נשמרים ב-SQLite
- 📊 **מנגנון משוב** - דרג כל פרומפט ועזור למערכת להשתפר
- 🎨 **ממשק פשוט** - Streamlit UI ידידותי בעברית
- 🔄 **Hindsight Learning** - המערכת לומדת ממשוב המשתמשים

## 🚀 התחלה מהירה

### דרישות מקדימות
- Python 3.10 ומעלה
- pip

### התקנה

```bash
# שכפל את הפרויקט
git clone https://github.com/shkomig/Engineered-prompt.git
cd Engineered-prompt

# צור סביבה וירטואלית (מומלץ)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# או
venv\Scripts\activate  # Windows

# התקן תלויות
pip install -r requirements.txt

# העתק את קובץ הסביבה
cp .env.example .env
```

### הרצה

```bash
streamlit run app.py
```

הדפדפן ייפתח אוטומטית בכתובת `http://localhost:8501`

### דמו מהיר

```bash
python demo.py
```

## 📖 שימוש

1. **הכנס טקסט בעברית** - כתוב בצורה חופשית מה אתה רוצה ליצור
   ```
   דוגמאות:
   • צור תמונה של חתול בחלל עם תאורה דרמטית
   • כתוב מייל רשמי למנהל לבקש חופשה
   • תכנת פונקציה בפייתון למיון רשימה
   ```

2. **בחר סוג משימה (אופציונלי)** - או השאר זיהוי אוטומטי

3. **הוסף הקשר והוראות (אופציונלי)** - בהגדרות מתקדמות

4. **לחץ "צור פרומפט"** - המערכת תייצר פרומפט מובנה

5. **העתק או הורד** - השתמש בפרומפט ב-ChatGPT, Claude, Midjourney, וכו'

6. **דרג והשאר משוב** - עזור למערכת להשתפר

## 🎯 3 סוגי טמפלטים ממוקדים

### 🎨 Visual (חזותי)
**לתמונות, וידאו, ותוכן חזותי**

| שדה | תיאור | דוגמה |
|-----|--------|--------|
| Subject | נושא התמונה | "חתול בחלל" |
| Visual Style | סגנון חזותי | Photo-realistic, Digital Art, 3D Render |
| Lighting | תאורה | Dramatic Studio Light, Golden Hour |
| Composition/Angle | זווית וקומפוזיציה | Wide Shot, Close-up, Bird's Eye View |
| Quality | איכות | 4K, Ultra Detailed, Cinematic |
| Context | הקשר נוסף | "לפרויקט מדע בדיוני" |
| Instructions | הוראות מיוחדות | "ריאליסטי ככל האפשר" |

**דוגמה:**
```
קלט: "צור תמונה של חתול בחלל עם תאורה דרמטית ואיכות 4K"
פלט: פרומפט מפורט עם כל הספציפיקציות החזותיות
```

### 📝 Textual (טקסטואלי)
**למייל, מכתבים, סיכומים, מאמרים**

| שדה | תיאור | דוגמה |
|-----|--------|--------|
| Purpose | מטרת הטקסט | Inform, Persuade, Request, Summarize |
| Recipient | נמען | Boss, Colleague, Customer, General Audience |
| Tone | טון | Professional, Friendly, Urgent, Formal |
| Length | אורך | Concise (1-2 paras), Moderate (3-5), Extensive (1000+) |
| Key Points | נקודות עיקריות | מה צריך לכסות |
| Context | הקשר נוסף | רקע ומידע נוסף |
| Instructions | הוראות מיוחדות | דרישות ספציפיות |

**דוגמה:**
```
קלט: "כתוב מייל רשמי למנהל לבקש חופשה"
פלט: פרומפט עם Purpose: Request, Recipient: Boss, Tone: Formal
```

### 💻 Technical (טכני)
**לקוד, פונקציות, אלגוריתמים, נוסחאות**

| שדה | תיאור | דוגמה |
|-----|--------|--------|
| Target Language | שפת תכנות | Python, JavaScript, SQL, LaTeX |
| Environment | סביבה/פריימוורק | React, Django, Console Only, Jupyter |
| Key Functionality | פונקציונליות נדרשת | מה הקוד צריך לעשות |
| Optimization | אופטימיזציה | Speed, Readability, Low memory |
| Context | הקשר נוסף | "לעבודה עם רשימות גדולות" |
| Instructions | הוראות מיוחדות | דרישות טכניות ספציפיות |

**דוגמה:**
```
קלט: "תכנת פונקציה בפייתון למיון רשימה"
פלט: פרומפט עם Language: Python, Functionality: מיון רשימה, Optimization: Speed
```

## 📁 מבנה הפרויקט

```
Engineered-prompt/
├── app.py                          # Streamlit web interface
├── demo.py                         # Demo script
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── src/
│   ├── __init__.py
│   ├── task_classifier.py         # Task classification (V/T/T)
│   ├── prompt_generator.py        # Prompt generation engine
│   ├── database.py                # Database handler (SQLite)
│   └── templates/                 # 3 Focused templates (JSON)
│       ├── visual.json            # 🎨 Visual template
│       ├── textual.json           # 📝 Textual template
│       └── technical.json         # 💻 Technical template
├── tests/                         # Unit tests
│   ├── test_task_classifier.py
│   ├── test_prompt_generator.py
│   └── test_database.py
├── Plan.md                        # Initial project plan
├── start.md                       # Detailed work plan
└── hindsight-prompting-research.md # Research documentation
```

## 🧪 הרצת טסטים

```bash
# הרץ דמו
python demo.py

# הרץ טסטים ספציפיים
python tests/test_task_classifier.py
python tests/test_prompt_generator.py
python tests/test_database.py
```

## 🛠️ Stack טכנולוגי

- **Backend**: Python 3.10+
- **UI**: Streamlit
- **Database**: SQLite + SQLAlchemy
- **Task Classification**: Rule-based patterns (expandable to ML)
- **Templates**: JSON-based modular system with `$$variable$$` syntax

## 📊 תכונות מתקדמות

### Template Variables System
- משתמשים ב-`$$variable$$` במקום `{variable}`
- כל טמפלט מכיל משתנים ספציפיים לסוג המשימה
- שדות שאינם מזוהים מסומנים כ-`[to be specified]`

### Context & Instructions
- שדות נפרדים שניתן להזין בממשק
- מופיעים בפרומפט הסופי
- עוזרים לספק הקשר והנחיות מדויקות

### Hindsight Learning
המערכת אוספת משוב ומשתמשת בו כדי:
- לזהות פרומפטים מוצלחים
- לשפר תבניות קיימות
- להתאים אוטומטית את סיווג המשימות

### Database Schema
```sql
prompts:
  - id (primary key)
  - input_text (Hebrew)
  - detected_intent (visual/textual/technical)
  - detected_style
  - generated_prompt
  - user_feedback (good/bad/neutral)
  - rating (1-5)
  - metadata_json
  - created_at
```

## 🎨 שינויים ב-V2.0 (Focused Templates)

### ✅ מה השתנה:
- ✨ **3 טמפלטים ממוקדים** במקום 7 גנריים
- 🔄 **סיווג משימות חדש** - Visual, Textual, Technical
- ⚙️ **שדות Context & Instructions** - קלט נפרד בממשק
- 🧹 **ניקיון פלט** - הסרת הערות גנריות מיותרות
- 💎 **משתנים עם `$$`** - במקום `{}`
- 📋 **דרישות ספציפיות** - כל טמפלט עם שדות רלוונטיים

### ❌ מה הוסר:
- הערות גנריות: "Please complete the task..."
- הערות גנריות: "Note: Please think through..."
- 7 טמפלטים ישנים (formal_letter, creative_writing, email, וכו')
- טמפלט General עם Length: 3-5 paragraphs

## 🔮 פיתוחים עתידיים

- [ ] Fine-tuning של מודל ML לסיווג משימות
- [ ] תבניות נוספות (Audio, Multimodal)
- [ ] שילוב API של LLMs לבדיקת איכות פרומפט
- [ ] A/B testing של תבניות
- [ ] ייצוא לפורמטים שונים (Markdown, PDF, JSON)
- [ ] API RESTful
- [ ] אפליקציית Mobile

## 🤝 תרומה

רוצה לתרום? מעולה!

1. Fork את הפרויקט
2. צור branch חדש (`git checkout -b feature/AmazingFeature`)
3. Commit את השינויים (`git commit -m 'Add some AmazingFeature'`)
4. Push ל-branch (`git push origin feature/AmazingFeature`)
5. פתח Pull Request

## 📝 רישיון

MIT License

## 📧 יצירת קשר

שאלות? הצעות? פתח [Issue](https://github.com/shkomig/Engineered-prompt/issues)

## 🙏 הכרת תודה

- מבוסס על מחקר של [Hindsight Prompting](hindsight-prompting-research.md)
- בהשראת Chain of Hindsight (CoH) - UC Berkeley
- תודה לקהילת Streamlit

---

**V2.0 - Focused Templates Edition**
**נבנה עם ❤️ עבור קהילת הפרומפט אינג'ינרים**
