def permissions(role):

    table={

        "member":[
            "read"
        ],

        "contributor":[
            "read",
            "submit"
        ],

        "reviewer":[
            "read",
            "submit",
            "review"
        ],

        "core_maintainer":[
            "read",
            "submit",
            "review",
            "approve"
        ]

    }

    return table.get(
        role,
        []
    )
