/* FAQ content for noya-app.js */
window.NOYA_FAQ = {
 "topics": [
  {
   "id": "safe",
   "icon": "🛡️",
   "he": "בטיחות",
   "en": "Safety"
  },
  {
   "id": "strength",
   "icon": "💪",
   "he": "חוזק",
   "en": "Strength"
  },
  {
   "id": "tools",
   "icon": "🧰",
   "he": "הכלים",
   "en": "The tools"
  },
  {
   "id": "app",
   "icon": "📲",
   "he": "אפליקציה",
   "en": "App"
  }
 ],
 "items": [
  {
   "t": "safe",
   "he": [
    "בטוח להקליד כאן את הסיסמה האמיתית שלי?",
    "כן. הניתוח לא יוצא מהדפדפן, ובדיקת הדליפות שולחת רק 5 תווים של hash. אפשר אפילו לפתוח את הדף, לנתק את האינטרנט, והמעבדה עדיין עובדת."
   ],
   "en": [
    "Is it safe to type my real password here?",
    "Yes. The analysis never leaves your browser, and the leak check sends only 5 characters of a hash. You can even open the page, disconnect from the internet, and the lab still works."
   ]
  },
  {
   "t": "safe",
   "he": [
    "איך בדיקת הדליפות לא חושפת את הסיסמה?",
    "מחושב לסיסמה hash מסוג SHA-1, ורק 5 התווים הראשונים נשלחים לשירות Have I Been Pwned. הוא מחזיר מאות התאמות, והדפדפן בודק מקומית אם שלכם ביניהן (k-anonymity)."
   ],
   "en": [
    "How does the leak check avoid exposing my password?",
    "Your password is hashed with SHA-1 and only the first 5 characters go to Have I Been Pwned. It returns hundreds of matches and your browser checks locally whether yours is among them (k-anonymity)."
   ]
  },
  {
   "t": "safe",
   "he": [
    "נשמר משהו במחשב או בשרת?",
    "לא. אין חשבון, אין אנליטיקס ואין מעקב. השדה גם מתנקה לבד אחרי זמן קצר כדי שאף אחד לא יראה את הסיסמה."
   ],
   "en": [
    "Is anything saved on my computer or a server?",
    "No. No account, no analytics, no tracking. The field also clears itself after a short while so nobody can see your password."
   ]
  },
  {
   "t": "strength",
   "he": [
    "למה P@ssw0rd מקבלת ציון נמוך?",
    "כי החלפת a ב-@ ו-o ב-0 היא הטריק הראשון שכלי פריצה מנסים. אורך ואקראיות אמיתית מנצחים החלפות חכמות בכל פעם."
   ],
   "en": [
    "Why does P@ssw0rd score low?",
    "Because swapping a for @ and o for 0 is the first trick cracking tools try. Length and real randomness beat clever swaps every time."
   ]
  },
  {
   "t": "strength",
   "he": [
    "משפט סיסמה באמת עדיף?",
    "כן. כמה מילים אקראיות יוצרות סיסמה ארוכה וקלה לזכירה. העיקר הוא אקראיות: מילים שבוחרים לבד קלות לניחוש בהרבה ממילים שמכונת המזל בוחרת."
   ],
   "en": [
    "Is a passphrase really better?",
    "Yes. A few random words make a long password that is easy to remember. The key is randomness: words you pick yourself are far easier to guess than words the slot machine picks."
   ]
  },
  {
   "t": "strength",
   "he": [
    "איך מחושב הזמן לפריצה?",
    "לפי מספר הניחושים שכלי פריצה אמיתי צריך, אחרי שהוא מנסה קודם דליפות, מילים, תאריכים ורצפים, מול ארבעה סוגי תוקפים: מאתר אונליין ועד בוטנט."
   ],
   "en": [
    "How is the time to crack calculated?",
    "From the number of guesses a real cracking tool needs after it tries leaks, words, dates and sequences first, against four attackers: from an online login to a botnet."
   ]
  },
  {
   "t": "tools",
   "he": [
    "מה זה פרח טביעת האצבע?",
    "הוא מצויר מה-hash מסוג SHA-256 של מה שהקלדתם. אי אפשר לשחזר ממנו את הסיסמה, אבל אותה סיסמה תמיד מצמיחה אותו פרח, כך שאפשר לדעת שהקלדתם נכון גם כשהשדה מוסתר."
   ],
   "en": [
    "What is the fingerprint flower?",
    "It is drawn from the SHA-256 hash of what you typed. It cannot be turned back into your password, but the same password always grows the same flower, so you can tell you typed it right even when the field is hidden."
   ]
  },
  {
   "t": "tools",
   "he": [
    "כמה אקראיות יש בסיסמאות מהמחולל?",
    "הן נוצרות ב-crypto.getRandomValues של הדפדפן, אותו מקור אקראיות שמשמש להצפנה. אפשר לבחור תווים אקראיים או מילים, להוסיף מספרים וסימנים ולהעתיק בלחיצה."
   ],
   "en": [
    "How random are the generated passwords?",
    "They come from the browser's crypto.getRandomValues, the same randomness used for encryption. Choose random characters or words, add numbers and symbols, and copy with one tap."
   ]
  },
  {
   "t": "tools",
   "he": [
    "יש גם API?",
    "כן. אותו מנוע רץ כשירות FastAPI בפייתון עם Docker, בדיקות ו-CI, עם נקודות קצה לחוזק, לדליפות ולמחולל."
   ],
   "en": [
    "Is there an API too?",
    "Yes. The same engine runs as a Python FastAPI service with Docker, tests and CI, with endpoints for strength, leaks and the generator."
   ]
  },
  {
   "t": "app",
   "he": [
    "אפשר להתקין את LeakLens כאפליקציה?",
    "כן. בכרום או באדג׳ לוחצים על כפתור ההתקנה שמופיע בתחתית המסך או בשורת הכתובת, ובאייפון בוחרים שיתוף ואז \"הוספה למסך הבית\". האפליקציה נפתחת בחלון משלה עם אייקון משלה."
   ],
   "en": [
    "Can I install LeakLens as an app?",
    "Yes. In Chrome or Edge tap the install button at the bottom of the screen or in the address bar. On iPhone tap Share, then \"Add to Home Screen\". It opens in its own window with its own icon."
   ]
  },
  {
   "t": "app",
   "he": [
    "זה עובד גם בלי אינטרנט?",
    "אחרי הביקור הראשון הקבצים של האתר נשמרים במכשיר, כך שהוא נפתח מהר ועובד גם כשהחיבור נופל. פעולות שצריכות שרת חיצוני יחכו שהחיבור יחזור."
   ],
   "en": [
    "Does it work offline?",
    "After your first visit the site files are kept on your device, so it opens fast and keeps working when the connection drops. Anything that needs an outside server waits until you are back online."
   ]
  },
  {
   "t": "app",
   "he": [
    "זה עולה כסף?",
    "לא. הכל חינם, בלי פרסומות ובלי הרשמה, והקוד פתוח בגיטהאב."
   ],
   "en": [
    "Does it cost anything?",
    "No. It is free, with no ads and no sign up, and the code is open on GitHub."
   ]
  }
 ]
};
