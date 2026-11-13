"""Bilingual (English / Hebrew) texts for every message the API returns."""

MESSAGES: dict[str, dict[str, str]] = {
    "too_short": {
        "en": "Use at least 12 characters.",
        "he": "כדאי להשתמש ב־12 תווים לפחות.",
    },
    "add_upper": {"en": "Add an uppercase letter.", "he": "כדאי להוסיף אות גדולה."},
    "add_lower": {"en": "Add a lowercase letter.", "he": "כדאי להוסיף אות קטנה."},
    "add_digit": {"en": "Add a number.", "he": "כדאי להוסיף ספרה."},
    "add_symbol": {"en": "Add a symbol such as ! or #.", "he": "כדאי להוסיף סימן כמו ! או #."},
    "common": {
        "en": "This is one of the most common passwords. Choose something else.",
        "he": "זו אחת הסיסמאות הנפוצות ביותר. כדאי לבחור משהו אחר.",
    },
    "repeat": {
        "en": "Avoid repeated characters like 'aaa'.",
        "he": "כדאי להימנע מתווים חוזרים כמו 'aaa'.",
    },
    "sequence": {
        "en": "Avoid sequences like 'abc' or '123'.",
        "he": "כדאי להימנע מרצפים כמו 'abc' או '123'.",
    },
    "keyboard": {
        "en": "Avoid keyboard patterns like 'qwerty'.",
        "he": "כדאי להימנע מדפוסי מקלדת כמו 'qwerty'.",
    },
    "year": {
        "en": "Years are easy to guess. Leave them out.",
        "he": "שנים קלות לניחוש. עדיף לוותר עליהן.",
    },
    "passphrase_tip": {
        "en": "Tip: four random words make a strong password that is easy to remember.",
        "he": "טיפ: ארבע מילים אקראיות יוצרות סיסמה חזקה שקל לזכור.",
    },
    "pwned": {
        "en": "This password appeared in data breaches. Never use it.",
        "he": "הסיסמה הזו הופיעה בדליפות מידע. אסור להשתמש בה.",
    },
    "not_pwned": {
        "en": "Not found in known data breaches.",
        "he": "לא נמצאה בדליפות מידע מוכרות.",
    },
}

LABELS: dict[int, dict[str, str]] = {
    0: {"en": "Very weak", "he": "חלשה מאוד"},
    1: {"en": "Weak", "he": "חלשה"},
    2: {"en": "Fair", "he": "בינונית"},
    3: {"en": "Strong", "he": "חזקה"},
    4: {"en": "Very strong", "he": "חזקה מאוד"},
}

TIME_UNITS = {
    "en": ["instantly", "seconds", "minutes", "hours", "days", "years", "centuries"],
    "he": ["מיד", "שניות", "דקות", "שעות", "ימים", "שנים", "מאות שנים"],
}


def t(code: str, lang: str) -> str:
    return MESSAGES[code].get(lang, MESSAGES[code]["en"])
