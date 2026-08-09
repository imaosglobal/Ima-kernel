
ENTITY_TYPES={

    "company":{
        "signals":[
            "AI",
            "startup",
            "product",
            "software"
        ]
    },

    "government":{
        "signals":[
            "ministry",
            "government",
            "municipality",
            "public"
        ]
    },

    "nonprofit":{
        "signals":[
            "foundation",
            "ngo",
            "charity",
            "social"
        ]
    },

    "education":{
        "signals":[
            "university",
            "school",
            "research"
        ]
    },

    "investment":{
        "signals":[
            "fund",
            "VC",
            "investor"
        ]
    }

}


def list_entity_types():
    return ENTITY_TYPES
