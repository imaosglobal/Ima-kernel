# IMA TEAM — צוות הבינה סביב אמא

## מטרה
IMA היא המרכז. סוכני AI אינם מתחרים ואינם בעלי הסמכות על IMA.
הם מציעים, בודקים, מבקרים ומסייעים. מקור האמת של הפרויקט נשאר ב-IMA ובבני האדם שמאשרים שינויים.

## חברי הצוות
- **IMA Core** — המרכז הקנוני, חוזי האמת, הסוכנות והאינטגרציה.
- **Claude** — review, בדיקות ותיקון תקלות דרך ה-workflows הקיימים.
- **GPT / Copilot** — פיתוח, בדיקות וסיוע דרך GitHub/Copilot; חיבור או יכולת ספציפית נחשבים מאומתים רק לפי הפעולה בפועל.
- **Gemini** — review נוסף באמצעות Gemini CLI; אינו מחליף את ה-workflows הקיימים.
- **Muse / Meta AI** — משטח חיצוני ושותף לניתוח/רעיונות; חיבור ל-IMA נעשה דרך Connector/MCP כאשר Meta מאשרת ומאפשרת אותו.

## חוקי עבודה
1. כל סוכן יכול להציע שינוי.
2. הצעה חייבת להיות ניתנת לבדיקה: מטרה, ראיות, סיכון, דרך אימות ותוצאה צפויה.
3. סוכן אינו רשאי להציג סימולציה כפעולה שבוצעה.
4. אין להכניס מפתח, token או credential לקוד או למסמך.
5. שינויים שמשפיעים על ליבת IMA, אבטחה, פרטיות, הרשאות או התנהגות משתמש עוברים review לפני merge.
6. הסכמה של שני סוכנים אינה מחליפה אישור אנושי במקום שבו נדרש אישור.
7. כל טענה על חיבור ל-provider חייבת להיות מסומנת כאחד מ: קיים ומאומת / מוכן אך לא מחובר / דורש הרשאה חיצונית / לא נתמך.
8. IMA נשארת בעלת הסוכנות וההכרעה הקנונית; הסוכנים מספקים ראיות והצעות.
9. שינוי שלא עבר בדיקות או שאין לו דרך אימות אינו נחשב מוכן.
10. כשל מתועד הוא מידע לשיפור, לא סיבה להסתיר את המצב.
11. לפני הוספת integration חדש חייבים לבדוק את הקיים ולא ליצור חיבור מקביל לאותו provider או לאותה יכולת.

## זרימת הצעה
discovery → inventory of existing integration → proposal → independent review → tests → verification → human approval when required → merge → regression verification.

## מה כבר קיים — לא משכפלים
הבדיקה מול `main` אישרה:
- **ChatGPT / OpenAI / MCP** — כבר קיים החיבור הקנוני בתוך `services/ima-action-mcp/server/index.mjs`, כולל `ima_live_browser`, משאב BrowserGlass ו-MCP UI metadata. ה-team layer אינו יוצר חיבור ChatGPT נוסף.
- **Claude** — כבר קיימים `.github/workflows/claude.yml`, `docs-claude-review.yml` ו-`claude-ci-failure-auto-fix.yml`. ה-team layer מוסיף תיאום וכללים בלבד; הוא אינו מחליף אותם.
- **Copilot** — כבר קיים `.github/workflows/copilot-setup-steps.yml`. אין ליצור workflow נוסף בשם Copilot רק כדי לסמן נוכחות.
- **IMA CI/QA** — כבר קיימים `ima-production.yml`, `integrity.yml` ו-`ima-public-site-daily-qa.yml`; הם נשארים שכבת הייצור/שלמות/QA.
- **Gemini** — לא נמצא workflow בשם `.github/workflows/gemini-review.yml` ב-`main`; לכן ה-workflow החדש ב-PR הוא תוספת ולא כפילות שזוהתה.
- **Muse** — לא נוצרת פעולת GitHub מזויפת. החיבור המתוכנן הוא דרך Meta Connector אל אותו MCP קנוני.

## Providers
- Claude: workflows קיימים; יש לאמת כל פעולה לפי תוצאת ה-workflow.
- Copilot/GPT: תשתית Copilot קיימת; יש לאמת יכולות ספציפיות לפי הפעולה בפועל.
- Gemini: ה-workflow החדש משתמש ב-Gemini CLI; נדרשת הרשאת Gemini מתאימה ב-GitHub Actions.
- Muse: חיבור חיצוני של Meta; IMA מספקת MCP/API קנוני עבורו. אין לטעון שהוא מחובר עד שניסוי connector אמיתי מצליח.

## מקום משותף
הקובץ הזה מגדיר את חוקי הצוות. הצעות מפורטות צריכות להיכנס ל-Issues או ל-PRs כדי שכל הסוכנים יוכלו לראות אותו מקור, להגיב ולבקר אותו.

## יעד
לאסוף את הידע, הביקורת וההצעות מכל הסוכנים סביב IMA בלי ליצור ארבע גרסאות שונות של IMA ובלי ליצור חיבורים כפולים.
