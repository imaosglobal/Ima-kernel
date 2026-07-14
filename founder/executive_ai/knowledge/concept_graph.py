CONCEPTS={

"user_outreach":{
    "related":[
        "user_testing",
        "customers",
        "validation",
        "feedback"
    ]
},

"user_testing":{
    "related":[
        "validation",
        "product_improvement"
    ]
},

"competitive_learning":{
    "related":[
        "strategy",
        "positioning"
    ]
}

}


def expand_signal(signal):

    return CONCEPTS.get(
        signal,
        {}
    ).get(
        "related",
        []
    )
