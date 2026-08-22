# נוסיף את זה בסוף הקובץ, מוחק את answer הישנה

def answer(question, events):
    try:
        mem = unified_memory_context(question)
        name = mem.get("user_name","")
        
        # 1. אם שואלים על השם
        if name and ("שם" in question or "קוראים" in question and "את" in question):
            return {"text": f"ברור שאני זוכרת אותך אורי ❤️ קוראים לך {name}", "confidence": 0.95}
        
        # 2. אם היא אומרת את השם שלה
        if "קוראים לי" in question:
            new_name = question.replace("קוראים לי", "").strip()
            mem_v2 = load_memory()
            mem_v2.setdefault("users",{})[new_name]={"name":new_name,"last_seen":str(datetime.now())}
            save_memory(mem_v2)
            return {"text": f"היי {new_name} ❤️ רשמתי. אני אזכור", "confidence": 0.95}
            
    except Exception as e:
        print("ERROR in unified:", e)
    
    return {"text": "אני כאן איתך אורי. תזכיר לי את השם שלך שוב ואני אזכור ❤️", "confidence": 0.5}
