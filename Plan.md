<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# עבודה טובה! אני רוצה תעזור לי אני רוצה לבנות מערכת יחסית פשוטה שבה אני כותב טקטס בעברית ואני מקבל פרומפט מובנה ברמה גבוהה

הנה תכנית פעולה לבניית מערכת פשוטה שתמיר טקסט חופשי בעברית לפרומפט מובנה ואיכותי, כולל דוגמה מעשית, הנחות ו"שלד קוד" עליו תוכל לבנות בקלות:

***

### יעדי המערכת

- **קלט:** טקסט עברי בשפה חופשית (למשל: "כתוב לי הודעה למורה על איחור של התלמיד")
- **פלט:** פרומפט מובנה ברמה גבוהה, שמוכן להזנה ל-LLM או בוט ב-AI (בפורמט באנגלית ככל הנדרש, בהיר ומנוסח אופטימלית)

***

### שלבים (מומלץ):

1. **קבלת הטקסט מהמשתמש.**
2. **זיהוי הכוונה (Intent Recognition):** מה המשימה? (כתיבה, תרגום, עיצוב תוכן)
3. **אפיון סגנון/קונטקסט:** מה סוג התשובה הרצויה? (פורמלי, ידידותי, קצר וכו')
4. **תרגום והמרה לפרומפט באנגלית** (אם צריך ל-LLMs בינלאומיים), כולל ניסוח best practices:
    - בקש מענה ישיר, ממוקד, במבנה ברור (markdown לדוג’)
    - ציין שמדובר בהנחיה או משימה (instruction)
    - בקש הפרדה לתחומים אם רלוונטי (output structure)
5. **הצגת הפרומפט המובנה ומאפשרות להעתיק או להוריד.**

***

### דוגמה מעשית

**קלט:**
כתוב לי הודעה למורה על איחור של התלמיד

**פלט (פרומפט מובנה באנגלית):**

```
You are an expert writer.  
Task: Write a short, polite note to a school teacher in Hebrew, informing about a student's tardiness.  
Constraints:
- The text should be formal and respectful.
- Mention the student's name should be easy to replace.
- Reason for tardiness can be added optionally.

Format the message in clear Hebrew.
Return only the message, without any extra commentary.
```


***

### מבנה קוד מוצע (Python דמוי קוד)

```python
# שלד ראשוני לדוגמה
def build_prompt(hebrew_text):
    # שלב 1: ניתוח טקסט עם מודל כוונה/כלים (רגקס/LLM/השלמה עצמית)
    intent = detect_intent(hebrew_text)
    style = detect_style(hebrew_text)
    
    # שלב 2: מחולל תבניות
    if intent == "הודעה למורה":
        prompt = f"""You are an expert writer.
Task: Write a formal notice in Hebrew to a school teacher about a student's tardiness.
Constraints:
- Keep it formal and clear.
- Easy to edit name and reason.
Format in Hebrew.
Return only the letter content, nothing else."""
        return prompt
    # הוסף תנאים נוספים לפי צורך

    # ברירת מחדל
    return "Task: ..."

# דוגמה:
print(build_prompt("כתוב לי הודעה למורה על איחור של התלמיד"))
```


***

### המלצות להמשך

- אפשר לפתח את הקוד לכלול ממשק web קטן (Flask/Streamlit), לבחור סגנון מתקדם (formality, creativity) ולהוסיף תיקוני עברית/תרגום אוטומטיים.
- תוכל לאמן או fine-tune T5, Mistral, Llama או Claude המקומיים למשימות זיהוי כוונה, אבל ניתן להתחיל גם עם openai / mistral API.
- לכלול אפשרות להוריד את התוצאה כ-Markdown.

רוצה דוגמה מלאה (כולל קוד שלם, קובץ markdown, או סקריפט הערכה מתקדמת)?

