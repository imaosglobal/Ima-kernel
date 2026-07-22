# IMA MANAGEMENT

מטרת תיקייה זו:
לשמור אינדקסים וניהול מבנה כדי למנוע בלבול בין קוד פעיל, קנוניקל, גיבויים וארכיונים.

## מבנה

### ACTIVE_RUNTIME_INDEX.json
מצביע על הקוד הפעיל שנמצא בשימוש בהרצה הנוכחית.

מקור:
- `.ima/ACTIVE_RUNTIME_MANIFEST.json`

### BACKUP_INDEX.json
מכיל מיקומים של גיבויים ושחזור:

- `.ima/REPAIR_BACKUPS`
- `.ima/archive_final`
- `.ima/snapshots`

### ARCHIVE_INDEX.json
מכיל מיקומי ארכיונים היסטוריים:

- `.ima/archive_final`
- `.ima/canonical_snapshots`
- `.ima/runtime_snapshots`

## כללי עבודה

1. אין להריץ קוד מתוך תיקיות archive או backup.
2. שינויי מערכת פעילים עוברים דרך ה־CANONICAL_AUTHORITY.
3. לפני שינוי גדול יוצרים snapshot.
4. הקוד הפעיל נבדק מול manifest.
5. גיבויים נשמרים לצורך שחזור בלבד.

## היררכיית אמון

1. CANONICAL_AUTHORITY — מקור אמת.
2. ACTIVE_RUNTIME_MANIFEST — מצב פעיל מאומת.
3. MANAGEMENT — אינדקס וניהול.
4. BACKUPS / ARCHIVE — היסטוריה ושחזור.

סטטוס:
MANAGEMENT_LAYER_ACTIVE
