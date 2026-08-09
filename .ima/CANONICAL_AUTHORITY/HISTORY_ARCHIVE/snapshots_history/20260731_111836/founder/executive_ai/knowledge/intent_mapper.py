INTENTS={

"product_improvement":[
    "שיפור מוצר",
    "לשפר את המוצר",
    "שדרוג מוצר",
    "פיתוח מוצר"
],

"customers":[
    "לקוחות",
    "משתמשים",
    "לקוחות ראשונים",
    "שוק"
],

"user_testing":[
    "ניסויי משתמשים",
    "בדיקות משתמשים",
    "פידבק"
]

}


def detect_intents(text):

    found=[]

    for intent,words in INTENTS.items():
        for word in words:
            if word in text:
                found.append(intent)
                break

    return found
