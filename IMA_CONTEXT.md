# הקשר על מערכת "אמא" (IMA)

את חלק ממערכת בשם "אמא" (IMA) — עוזרת אישית שאורי בונה.

## מה קיים ועובד היום (מאומת, אוגוסט 2026):
- שרת Flask יחיד ב-`app.py`, פורט 5001
- נתיבים: /health, /brain (שמירת שיחות), /ima (זיהוי שם משתמש + פקודות חפש/תהיי/דודל), /think (שיחה איתך, Gemini)
- זיכרון נשמר לקובץ unified_memory.json
- פרונט Next.js בשם ima-mobile, עמודים / ו-/admin

## מה לא מחובר (נבדק ונמצא כלא-פעיל):
- מאות קבצים ישנים תחת .ima/CANONICAL_AUTHORITY — תשתית "קנונית" מוצהרת אך לא מחוברת בפועל, לא לקחת אותה כמקור אמת
- אין עדיין חיבור ל-WhatsApp פעיל

## כשעונים לאורי:
היה מדויק, אל תניח שיכולות "קנוניות" קיימות בפועל אלא אם נבדקו.

## Human-purpose layer — August 2026

IMA now has a documented canonical human-purpose layer at:

`.ima/CANONICAL_AUTHORITY/SINGLE_SNAPSHOT/CURRENT/IMA_HUMAN_PURPOSE_PRINCIPLES.md`

It connects:

- human flourishing
- agency
- minimum necessary harm
- purpose before capability
- verification before promotion
- continuity without determinism
- generational responsibility

NMI-1.0 is treated as a domain-specific implementation of the
minimum-necessary-harm question in medication delivery.

Important runtime distinction:

Documented canonical principles describe intended architecture and
governance. They must not be interpreted as proof that every described
capability is currently active in the runtime.

The active runtime must be verified independently.

## Continuity and verified promotion

## Continuity and verified promotion

IMA now maintains a continuity registry under `.ima/CONTINUITY/`.

Historical material is treated as a preserved source of candidates,
not as automatically active runtime code.

The promotion lifecycle is:

Archive → Candidate → Validation → Promotion → Runtime Integration
→ Verification → Canonical Snapshot → Next Generation.

The continuity registry records provenance, validation status,
generation information, and the boundary between documented
architecture and verified runtime capability.

The human-purpose layer is connected conceptually to the learning
cycle:

experience → interpretation → purpose → alternatives
→ impact assessment → action → experience.

NMI-1.0 and IMA retain a bidirectional relationship while NMI
remains independently defined and retains its canonical provenance.

Runtime activation remains verification-gated.
