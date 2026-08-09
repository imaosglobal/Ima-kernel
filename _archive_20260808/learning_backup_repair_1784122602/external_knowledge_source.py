
def fetch_external(question):
    # placeholder connector
    # כאן יתחבר בעתיד API / ספריות / מסמכים
    knowledge={
        "מה זה חתול":{
            "content":"חתול הוא יונק ממשפחת החתוליים.",
            "domain":"biology"
        },
        "מה זה קוואנטום":{
            "content":"קוואנטום הוא תחום בפיזיקה המתאר מערכות ברמה האטומית והתת אטומית.",
            "domain":"physics"
        }
    }

    return knowledge.get(question)
