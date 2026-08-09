def role_from_trust(score):

    if score >= 80:
        return "core_maintainer"

    if score >= 50:
        return "reviewer"

    if score >= 20:
        return "contributor"

    return "member"
