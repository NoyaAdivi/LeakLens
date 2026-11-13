<div dir="rtl">

<p align="center">
  <a href="https://noyaadivi.github.io/LeakLens/?lang=he"><img src="docs/readme/banner-he.svg" width="100%" alt="LeakLens: ממשק API לבדיקת חוזק סיסמאות ודליפות מידע, בפרטיות מלאה"></a>
</p>

<p align="center"><a href="README.md"><img src="docs/readme/lang-en.svg" height="44" alt="English version"></a></p>

<p align="center">
  <a href="https://noyaadivi.github.io/LeakLens/?lang=he"><img src="https://img.shields.io/badge/%D7%9C%D7%A0%D7%A1%D7%95%D7%AA_%D7%91%D7%93%D7%A4%D7%93%D7%A4%D7%9F-FFD5C9?style=for-the-badge&logo=googlechrome&logoColor=A8483A" alt="לנסות בדפדפן"></a>
  <a href="#-api-at-a-glance"><img src="https://img.shields.io/badge/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%94%D6%BEAPI-D9F3E7?style=for-the-badge&logo=fastapi&logoColor=1F7350" alt="נקודות ה־API"></a>
  <a href="docs/SECURITY.he.md"><img src="https://img.shields.io/badge/%D7%9E%D7%95%D7%93%D7%9C_%D7%94%D7%90%D7%91%D7%98%D7%97%D7%94-DAD5FF?style=for-the-badge&logo=letsencrypt&logoColor=5548C8" alt="מודל האבטחה"></a>
</p>

<p align="center">
  <a href="https://github.com/NoyaAdivi/LeakLens/actions/workflows/tests.yml"><img src="https://github.com/NoyaAdivi/LeakLens/actions/workflows/tests.yml/badge.svg" alt="בדיקות"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/NoyaAdivi/LeakLens?color=DAD5FF&labelColor=5548C8" alt="רישיון"></a>
  <a href="https://github.com/NoyaAdivi/LeakLens/commits/main"><img src="https://img.shields.io/github/last-commit/NoyaAdivi/LeakLens?color=FFD5C9&labelColor=A8483A" alt="עדכון אחרון"></a>
  <a href="https://github.com/NoyaAdivi/LeakLens"><img src="https://img.shields.io/github/languages/top/NoyaAdivi/LeakLens?color=D9F3E7&labelColor=1F7350" alt="שפה עיקרית"></a>
</p>

<h3 align="center">לבדוק סיסמה בלי למסור אותה לאף אחד.</h3>

<p align="center">
  LeakLens הוא REST API שמדרג את חוזק הסיסמה, בודק אם היא הופיעה בדליפות מידע ויוצר סיסמאות מאובטחות.<br>
  הסיסמה לא נשמרת, לא נרשמת ביומן ולא נשלחת לשום מקום. רק 5 תווים מה־hash שלה יוצאים מהשרת.
</p>

<table align="center">
  <tr>
    <td align="center" width="25%"><a href="#-how-your-password-stays-private"><b>🔐 5 תווים</b></a><br><sub>זה כל מה שיוצא</sub></td>
    <td align="center" width="25%"><a href="#-api-at-a-glance"><b>⚡ 7</b></a><br><sub>נקודות REST</sub></td>
    <td align="center" width="25%"><a href="https://noyaadivi.github.io/LeakLens/?lang=he"><b>🌍 HE · EN</b></a><br><sub>כל הודעה בשתי השפות</sub></td>
    <td align="center" width="25%"><a href="https://github.com/NoyaAdivi/LeakLens/actions/workflows/tests.yml"><b>🧪 CI</b></a><br><sub>בדיקות בכל דחיפה</sub></td>
  </tr>
</table>

<a name="-what-it-does"></a>
<p align="center"><a href="#-how-your-password-stays-private"><img src="docs/readme/features-he.svg" width="100%" alt="מה זה עושה"></a></p>

<table dir="rtl">
  <tr valign="top">
    <td width="50%">
      <p><b>💪 ניתוח חוזק</b></p>
      <ul>
        <li><b>ציון בין 0 ל־4</b> עם אנטרופיה בביטים והערכה של זמן הפיצוח</li>
        <li><b>מזהה חולשות אמיתיות:</b> סיסמאות נפוצות, החלפת אותיות בסימנים (<code>P@ssw0rd</code>), רצפים, חזרות, דפוסי מקלדת ושנים</li>
        <li><b>טיפים ברורים</b> בעברית או באנגלית איך לחזק את הסיסמה</li>
      </ul>
    </td>
    <td width="50%">
      <p><b>🕵️ בדיקת דליפות</b></p>
      <ul>
        <li>חיפוש ב־<a href="https://haveibeenpwned.com/Passwords"><b>Have I Been Pwned</b></a>, מאגר של מאות מיליוני סיסמאות שדלפו</li>
        <li><b>k-anonymity:</b> נשלחים רק 5 התווים הראשונים של hash מסוג SHA-1</li>
        <li><b>נקודה שמקבלת רק hash</b>, ללקוחות שלא רוצים לשלוח את הסיסמה בכלל</li>
      </ul>
    </td>
  </tr>
  <tr valign="top">
    <td width="50%">
      <p><b>🎲 מחולל סיסמאות</b></p>
      <ul>
        <li>מבוסס על המודול <a href="https://docs.python.org/3/library/secrets.html"><code>secrets</code></a> של Python, מקור אקראיות מאובטח קריפטוגרפית</li>
        <li>תמיד כולל את כל סוגי התווים שבחרת, ואז מערבב</li>
        <li>אפשר לוותר על תווים שנראים דומים, כמו <code>l</code>, <code>1</code>, <code>O</code> ו־<code>0</code></li>
      </ul>
    </td>
    <td width="50%">
      <p><b>🧩 משפטי סיסמה</b></p>
      <ul>
        <li>מילים אקראיות כמו <code>Maple-Comet-Otter-Prism-42</code>, חזקות וקלות לזכירה</li>
        <li>בוחרים את מספר המילים ואת התו המפריד</li>
        <li>כל תוצאה מגיעה עם האנטרופיה שלה, כך שאפשר למדוד את החוזק</li>
      </ul>
    </td>
  </tr>
</table>

<a name="-how-your-password-stays-private"></a>
<p align="center"><a href="#-api-at-a-glance"><img src="docs/readme/privacy-he.svg" width="100%" alt="איך הסיסמה נשארת פרטית"></a></p>

<p align="center">
  <a href="https://haveibeenpwned.com/API/v3#PwnedPasswords"><img src="docs/readme/privacy-flow-he.svg" width="100%" alt="הסיסמה עוברת SHA-1, רק 5 התווים הראשונים נשלחים ל־HIBP, שמחזיר רשימת hash תואמים, וההשוואה נעשית אצלנו"></a>
</p>

<p align="center"><sub>HIBP מקבל רק <code>5BAA6</code>, תחילית שמשותפת למאות סיסמאות שונות, ולכן הוא לא יכול לדעת איזו סיסמה נבדקה. התשובות מרופדות, כך שגם הגודל שלהן לא מסגיר כלום.</sub></p>

<a name="-api-at-a-glance"></a>
<p align="center"><a href="#-try-it-in-your-browser"><img src="docs/readme/api-he.svg" width="100%" alt="ה־API במבט אחד"></a></p>

| שיטה | נקודה | מה היא עושה |
|---|---|---|
| `POST` | `/v1/strength` | ציון, אנטרופיה, זמן פיצוח, בדיקות וטיפים |
| `POST` | `/v1/pwned` | בדיקת דליפות לסיסמה, בשיטת k-anonymity |
| `POST` | `/v1/pwned/hash` | בדיקת דליפות לפי hash מסוג SHA-1 שנוצר אצלך |
| `POST` | `/v1/check` | חוזק ודליפות יחד, עם תשובה סופית `safe` |
| `POST` | `/v1/generate` | סיסמה אקראית מאובטחת |
| `POST` | `/v1/passphrase` | משפט סיסמה ממילים אקראיות |
| `GET` | `/health` | מצב השירות |

כל בקשה מקבלת `"lang": "he"` או `"lang": "en"`. התיעוד האינטראקטיבי נפתח ב־`/docs` אחרי שהשרת עולה.

<details>
<summary><b>📬 דוגמה לבקשה ולתשובה</b></summary>
<br>

```bash
curl -X POST http://localhost:8000/v1/check \
  -H "Content-Type: application/json" \
  -d '{"password": "Summer2024!", "lang": "he"}'
```

```json
{
  "safe": false,
  "strength": {
    "score": 0,
    "label": "חלשה מאוד",
    "entropy_bits": 10.0,
    "crack_time_display": "מיד",
    "checks": { "length_12": false, "not_common": false, "no_years": false, "...": true },
    "feedback": ["זו אחת הסיסמאות הנפוצות ביותר. כדאי לבחור משהו אחר.", "..."]
  },
  "breach": { "pwned": true, "count": 4216, "message": "הסיסמה הזו הופיעה בדליפות מידע. אסור להשתמש בה." }
}
```
<sub>מספר הדליפות כאן להמחשה. המספרים האמיתיים גדלים ככל שמתווספות דליפות חדשות.</sub>
</details>

<a name="-try-it-in-your-browser"></a>
<p align="center"><a href="https://noyaadivi.github.io/LeakLens/?lang=he"><img src="docs/readme/playground-he.svg" width="100%" alt="לנסות בדפדפן"></a></p>

<p align="center">
  <a href="https://noyaadivi.github.io/LeakLens/?lang=he"><img src="docs/images/playground-he.png" width="85%" alt="מגרש המשחקים של LeakLens: מד חוזק, בדיקות, בדיקת דליפות, מחולל סיסמאות ומשפטי סיסמה"></a>
</p>

<p align="center">
  <a href="https://noyaadivi.github.io/LeakLens/?lang=he"><b>לפתוח בעברית</b></a> ·
  <a href="https://noyaadivi.github.io/LeakLens/?lang=en"><b>לפתוח באנגלית</b></a> ·
  <a href="docs/index.html"><b>קוד המקור</b></a>
</p>

<p align="center"><sub>מגרש המשחקים מריץ את אותם כללים ב־JavaScript, מחשב hash עם Web Crypto של הדפדפן ופונה ל־HIBP ישירות. בלי שרת ובלי מעקב.</sub></p>

<a name="-security-by-design"></a>
<p align="center"><a href="#-tech-stack"><img src="docs/readme/hardening-he.svg" width="100%" alt="אבטחה מהיסוד"></a></p>

| הגנה | איך |
|---|---|
| הסיסמה לא נשמרת ולא נרשמת | נשמרת ב־`SecretStr` של Pydantic, אין מסד נתונים, יומן הגישה כבוי ב־Docker |
| שום דבר לא נשמר בדפדפן או בשרתי ביניים | `Cache-Control: no-store` בכל תשובה של `/v1` |
| ניחוש בכוח ושימוש לרעה | הגבלת קצב לכל IP עם חלון נע, תשובת `429` עם `Retry-After` |
| בקשות גדולות מדי | גוף מעל 4KB נדחה עם `413`, וסיסמה מוגבלת ל־256 תווים |
| התקפות דפדפן | `nosniff`, חסימת הטמעה במסגרת, CSP קפדני, `no-referrer`, HSTS |
| קריאות מאתרים אחרים | CORS סגור כברירת מחדל, ונפתח רק לאתרים שמגדירים |
| קונטיינר | תמונה רזה שרצה כמשתמש בלי הרשאות root |

עוד פרטים ב־[docs/SECURITY.he.md](docs/SECURITY.he.md).

<a name="-tech-stack"></a>
<p align="center"><a href="#-run-it-locally"><img src="docs/readme/stack-he.svg" width="100%" alt="טכנולוגיות"></a></p>

<p align="center"><b>API</b><br>
<a href="https://www.python.org"><img src="https://img.shields.io/badge/Python_3.12-DAD5FF?style=for-the-badge&logo=python&logoColor=5548C8" alt="Python 3.12"></a>
<a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/FastAPI-DAD5FF?style=for-the-badge&logo=fastapi&logoColor=5548C8" alt="FastAPI"></a>
<a href="https://docs.pydantic.dev"><img src="https://img.shields.io/badge/Pydantic-DAD5FF?style=for-the-badge&logo=pydantic&logoColor=5548C8" alt="Pydantic"></a>
<a href="https://www.python-httpx.org"><img src="https://img.shields.io/badge/HTTPX-DAD5FF?style=for-the-badge&logo=python&logoColor=5548C8" alt="HTTPX"></a>
</p>

<p align="center"><b>אבטחה</b><br>
<a href="https://haveibeenpwned.com/API/v3#PwnedPasswords"><img src="https://img.shields.io/badge/Have_I_Been_Pwned-FBD5E0?style=for-the-badge&logo=letsencrypt&logoColor=A03A5C" alt="Have I Been Pwned"></a>
<a href="https://docs.python.org/3/library/secrets.html"><img src="https://img.shields.io/badge/secrets_CSPRNG-FBD5E0?style=for-the-badge&logo=python&logoColor=A03A5C" alt="secrets CSPRNG"></a>
<a href="https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API"><img src="https://img.shields.io/badge/Web_Crypto-FBD5E0?style=for-the-badge&logo=javascript&logoColor=A03A5C" alt="Web Crypto"></a>
</p>

<p align="center"><b>השקה</b><br>
<a href="https://docs.pytest.org"><img src="https://img.shields.io/badge/pytest-D9F3E7?style=for-the-badge&logo=pytest&logoColor=1F7350" alt="pytest"></a>
<a href="https://github.com/NoyaAdivi/LeakLens/actions"><img src="https://img.shields.io/badge/GitHub_Actions-D9F3E7?style=for-the-badge&logo=githubactions&logoColor=1F7350" alt="GitHub Actions"></a>
<a href="https://www.docker.com"><img src="https://img.shields.io/badge/Docker-FFD5C9?style=for-the-badge&logo=docker&logoColor=A8483A" alt="Docker"></a>
<a href="https://pages.github.com"><img src="https://img.shields.io/badge/GitHub_Pages-FFD5C9?style=for-the-badge&logo=githubpages&logoColor=A8483A" alt="GitHub Pages"></a>
</p>

<a name="-run-it-locally"></a>
<p align="center"><a href="#contact"><img src="docs/readme/run-he.svg" width="100%" alt="הרצה מקומית"></a></p>

1. התקנה והפעלה:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # במק או בלינוקס: source .venv/bin/activate
   pip install -r requirements-dev.txt
   uvicorn app.main:app --reload
   ```
2. פותחים את [http://localhost:8000/docs](http://localhost:8000/docs) ומנסים כל נקודה.
3. מריצים את הבדיקות:
   ```bash
   pytest -q
   ```
4. או עם Docker:
   ```bash
   docker build -t leaklens .
   docker run -p 8000:8000 leaklens
   ```

ההגדרות נמצאות ב־[`.env.example`](.env.example): הגבלת הקצב והאתרים שמורשים לפנות ל־API מהדפדפן.

<details>
<summary><b>📂 מבנה הפרויקט</b></summary>

```
├── app/
│   ├── main.py        אפליקציית FastAPI, מודלים ונתיבים
│   ├── strength.py    דירוג חוזק, זיהוי דפוסים, זמן פיצוח
│   ├── pwned.py       SHA-1, חיפוש k-anonymity, מטמון עם תפוגה
│   ├── generator.py   סיסמאות ומשפטי סיסמה מאובטחים
│   ├── security.py    כותרות אבטחה, הגבלת קצב, הגבלת גודל
│   ├── messages.py    כל ההודעות בעברית ובאנגלית
│   └── data/          סיסמאות נפוצות ורשימת המילים
├── tests/             בדיקות pytest (לוגיקה ו־API)
├── docs/
│   ├── index.html     מגרש המשחקים החי (GitHub Pages)
│   ├── SECURITY.md    מודל האבטחה
│   └── readme/        העיצובים של ה־README
├── .github/workflows/ CI
└── Dockerfile
```
</details>

<details>
<summary><b>🙏 קרדיטים</b></summary>
<br>
נתוני הדליפות מגיעים מ־<a href="https://haveibeenpwned.com">Have I Been Pwned</a> של Troy Hunt, דרך ה־API החינמי של Pwned Passwords, ברישיון <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
</details>

<a name="contact"></a>
<p align="center"><a href="https://www.linkedin.com/in/noya-adivi/"><img src="docs/readme/footer-he.svg" width="100%" alt="נבנה באהבה על ידי נויה אדיבי"></a></p>

<p align="center">
  <a href="https://noyaadivi.github.io/LeakLens/?lang=he"><img src="https://img.shields.io/badge/%D7%9C%D7%A0%D7%A1%D7%95%D7%AA_%D7%90%D7%AA_LeakLens-FFD5C9?style=for-the-badge&logo=googlechrome&logoColor=A8483A" alt="לנסות את LeakLens"></a>
  <a href="https://www.linkedin.com/in/noya-adivi/"><img src="https://img.shields.io/badge/LinkedIn-DAD5FF?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzU1NDhDOCIgZD0iTTIwLjQ1IDIwLjQ1aC0zLjU2di01LjU3YzAtMS4zMy0uMDMtMy4wNC0xLjg1LTMuMDQtMS44NiAwLTIuMTQgMS40NS0yLjE0IDIuOTR2NS42N0g5LjM1VjloMy40MXYxLjU2aC4wNWMuNDgtLjkgMS42NC0xLjg1IDMuMzctMS44NSAzLjYgMCA0LjI3IDIuMzcgNC4yNyA1LjQ2djYuMjh6TTUuMzQgNy40M2EyLjA2IDIuMDYgMCAxIDEgMC00LjEzIDIuMDYgMi4wNiAwIDAgMSAwIDQuMTN6TTcuMTIgMjAuNDVIMy41NlY5aDMuNTZ2MTEuNDV6TTIyLjIyIDBIMS43N0MuNzkgMCAwIC43NyAwIDEuNzN2MjAuNTRDMCAyMy4yMy43OSAyNCAxLjc3IDI0aDIwLjQ1Yy45OCAwIDEuNzgtLjc3IDEuNzgtMS43M1YxLjczQzI0IC43NyAyMy4yIDAgMjIuMjIgMHoiLz48L3N2Zz4=" alt="LinkedIn"></a>
  <a href="https://noyaadivi.github.io/noya-website"><img src="https://img.shields.io/badge/%D7%AA%D7%99%D7%A7_%D7%A2%D7%91%D7%95%D7%93%D7%95%D7%AA-D9F3E7?style=for-the-badge&logo=githubpages&logoColor=1F7350" alt="תיק עבודות"></a>
  <a href="https://github.com/NoyaAdivi"><img src="https://img.shields.io/badge/%D7%A2%D7%95%D7%93_%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98%D7%99%D7%9D-FBD5E0?style=for-the-badge&logo=github&logoColor=A03A5C" alt="עוד פרויקטים"></a>
</p>

</div>
