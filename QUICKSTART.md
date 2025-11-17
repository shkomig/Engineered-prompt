# 🚀 QUICK START GUIDE - Engineered Prompt

## Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Windows PowerShell or Command Prompt

---

## Step 1: Install Dependencies

```powershell
cd c:\Vs-Pro\Prompt_engineered\Engineered-prompt

# Install required packages
pip install -r requirements.txt
```

**Required packages:**
- streamlit >=1.28.0
- python-dotenv >=1.0.0
- pydantic >=2.0.0
- sqlalchemy >=2.0.0

---

## Step 2: Configure Environment (Optional)

```powershell
# Copy example env file
Copy-Item .env.example .env

# Edit .env if you need custom settings
notepad .env
```

Current settings in `config.py`:
- Database: SQLite (local)
- Templates directory: `src/templates/`
- App version: 0.1.0

---

## Step 3: Run the Demo (Recommended First)

Test the system without starting the web server:

```powershell
python demo.py
```

This will:
- ✅ Test intent detection
- ✅ Generate sample prompts
- ✅ Show available templates
- ✅ Test database operations
- ✅ Display supported intents

**Expected Output:**
```
╔════════════════════════════════════╗
║  🎯 ENGINEERED PROMPT - System Demo║
╚════════════════════════════════════╝

🎯 DEMO 1: Intent Detection
...
✅ All Demos Completed Successfully!
```

---

## Step 4: Launch the Web Interface

```powershell
streamlit run app.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The browser should automatically open. If not, visit:
👉 **http://localhost:8501**

---

## Using the Web Interface

### Main Panel (Left Column)
1. **Type Hebrew text** - Enter your request in Hebrew
2. **Optional: Select Intent** - Choose specific type or let AI detect it
3. **Click "🚀 Generate Prompt"** - Create the optimized prompt

### Output Panel (Right Column)
1. **View Generated Prompt** - See the structured prompt
2. **Copy Button** - Copy to clipboard
3. **Edit & Download** - Modify or save as file
4. **Submit Feedback** - Rate the quality (Good/Neutral/Bad)

### Sidebar Features
- **📊 Statistics** - View system stats
- **📜 History** - See previous prompts
- **📋 Templates** - Available templates info

---

## Example Workflows

### Example 1: Formal Letter

```
Input:    כתוב לי מכתב רשמי למורה על איחור של תלמיד
Intent:   formal_letter (detected automatically)
Output:   Professional letter template with variables
```

### Example 2: Creative Writing

```
Input:    כתוב לי סיפור קצר על ילד בחלל
Intent:   creative_writing
Output:   Creative writing prompt template
```

### Example 3: Summary

```
Input:    סיכם לי את הטקסט הזה בקצרה
Intent:   summary
Output:   Summarization prompt template
```

---

## Troubleshooting

### Issue: "Module not found" error
**Solution:**
```powershell
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: Port 8501 already in use
**Solution:**
```powershell
# Use a different port
streamlit run app.py --server.port=8502
```

### Issue: Database error
**Solution:**
```powershell
# Delete old database and recreate
Remove-Item prompts.db -ErrorAction SilentlyContinue
# Run again - new database will be created
python demo.py
```

### Issue: Hebrew text not displaying correctly
**Solution:**
- Ensure Windows Regional Settings support Hebrew
- Check if browser supports RTL (Right-to-Left) text
- Try clearing browser cache

---

## System Architecture Quick Overview

```
┌─────────────────────────────────────┐
│  Web Interface (Streamlit)          │ ← You interact here
└─────────────┬───────────────────────┘
              │
      ┌───────┴──────────┐
      │                  │
      ▼                  ▼
┌──────────────┐   ┌──────────────────┐
│ Intent       │   │ Prompt Generator │
│ Detector     │   │                  │
│ (Identifies) │   │ (Creates Prompt) │
└──────┬───────┘   └────────┬─────────┘
       │                    │
       └────────┬───────────┘
                │
                ▼
        ┌──────────────────┐
        │ Template Library │  ← 8 templates
        │ (JSON files)     │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Database (SQLite)│  ← Stores history
        │                  │
        └──────────────────┘
```

---

## Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit web interface |
| `config.py` | Configuration settings |
| `requirements.txt` | Python dependencies |
| `demo.py` | System demonstration script |
| `src/intent_detector.py` | Intent detection engine |
| `src/prompt_generator.py` | Prompt generation engine |
| `src/database.py` | Database operations |
| `src/templates/` | Prompt templates (JSON) |
| `SYSTEM_OVERVIEW.md` | Detailed system documentation |
| `hindsight-prompting-research.md` | Academic research |
| `Plan.md` | Development plan |

---

## Supported Intent Types

| Intent | Hebrew Description | Example |
|--------|-------------------|---------|
| `formal_letter` | מכתבים רשמיים | "כתוב מכתב למורה..." |
| `creative_writing` | כתיבה יצירתית | "כתוב סיפור על..." |
| `email` | הודעות דוא"ל | "כתוב אימייל ל..." |
| `summary` | סיכומים | "סיכם לי את..." |
| `translation` | תרגומים | "תרגם לי ל..." |
| `question_answer` | שאלות ותשובות | "תסביר לי מה זה..." |
| `business_proposal` | הצעות עסקיות | "כתוב הצעה עסקית..." |

---

## Database Information

**Location:** `prompts.db` (local SQLite)

**Tables:**
- `prompts` - Stores all generated prompts and feedback

**Stored Data:**
- Input text (Hebrew)
- Detected intent
- Detected style
- Generated prompt (English)
- User feedback (good/neutral/bad)
- Rating (1-5 stars)
- Metadata
- Timestamp

---

## Performance Tips

1. **First run is slower** - Database initializes on first use
2. **Keep templates updated** - JSON files are loaded once per session
3. **Clear history** - Delete prompts.db if database grows large
4. **Browser cache** - Clear cache for responsive UI

---

## Next Steps

1. ✅ Run `python demo.py` - Verify system works
2. ✅ Start `streamlit run app.py` - Launch web interface
3. ✅ Try sample prompts - Test different intent types
4. ✅ Submit feedback - Help system learn and improve
5. ✅ Check history - Review previous generation

---

## Support & Documentation

- **System Overview:** Read `SYSTEM_OVERVIEW.md`
- **Full Documentation:** See `README.md`
- **Research:** Check `hindsight-prompting-research.md`
- **Development:** See `Plan.md`

---

**Version:** 0.1.0  
**Last Updated:** November 17, 2025  
**Status:** ✅ Ready to Run

🎉 **System is ready! Start with Step 3 or 4 above.**
