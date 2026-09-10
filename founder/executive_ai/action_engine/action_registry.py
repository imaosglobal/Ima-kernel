ACTIONS = {

    "find_leads": {
        "description": "מציאת חברות AI מתאימות",
        "external_side_effect": False,
    },

    "rank_leads": {
        "description": "דירוג התאמה לפי IMA fit",
        "external_side_effect": False,
    },

    "generate_outreach": {
        "description": "יצירת הודעות אישיות",
        "external_side_effect": False,
    },

    "send_outreach": {
        "description": "שליחת הודעות",
        "external_side_effect": True,
        "requires_approval": True,
    },

    "collect_feedback": {
        "description": "איסוף תגובות ולמידה",
        "external_side_effect": False,
    },

    "analyze_feedback": {
        "description": "ניתוח משוב",
        "external_side_effect": False,
    },

    "update_product": {
        "description": "הצעת עדכון מוצר",
        "external_side_effect": True,
        "requires_approval": True,
    },

    "prepare_public_impact_message": {
        "description": "הכנת מסר להשפעה ציבורית",
        "external_side_effect": False,
        "requires_approval": False,
    },

    "monitor": {
        "description": "ניטור הזדמנות",
        "external_side_effect": False,
        "requires_approval": False,
    },
}


def list_actions():
    return ACTIONS
