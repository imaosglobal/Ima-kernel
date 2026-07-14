
COUNTRIES={

    "Israel":{
        "languages":["Hebrew","Arabic","English"]
    },

    "USA":{
        "languages":["English"]
    },

    "Japan":{
        "languages":["Japanese"]
    }

}


def add_person(person):

    country=person.get(
        "country",
        "unknown"
    )

    return {
        "country":country,
        "person":person
    }


def group_by_country(people):

    result={}

    for person in people:

        country=person.get(
            "country",
            "unknown"
        )

        if country not in result:
            result[country]=[]

        result[country].append(person)

    return result

