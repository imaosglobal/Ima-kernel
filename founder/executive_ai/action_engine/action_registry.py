ACTIONS = {

    "find_leads": {
        "description": "מציאת חברות AI מתאימות"
    },

    "rank_leads": {
        "description": "דירוג התאמה לפי IMA fit"
    },

    "generate_outreach": {
        "description": "יצירת הודעות אישיות"
    },

    "send_outreach": {
        "description": "שליחת הודעות"
    },

    "collect_feedback": {
        "description": "איסוף תגובות ולמידה"
    }

}


def list_actions():
    return ACTIONS
