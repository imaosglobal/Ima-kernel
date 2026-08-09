
def validate(answer):
    if not answer:
        return False
    bad=["html","doctype","javascript","stylesheet","cookie"]
    text=str(answer).lower()
    return not any(x in text for x in bad)
