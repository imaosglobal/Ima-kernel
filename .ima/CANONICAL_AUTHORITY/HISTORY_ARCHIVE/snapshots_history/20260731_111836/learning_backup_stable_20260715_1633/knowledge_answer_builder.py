def build_answer(result, question):

    if not result:
        return None

    if isinstance(result,str):
        return result

    if isinstance(result,dict):

        domain=result.get(
            "domain",
            result.get("topic","")
        )

        content=result.get(
            "content",
            result.get("answer","")
        )

        if content:
            if domain:
                return (
                    "תחום: "
                    + str(domain)
                    + "\n\n"
                    + str(content)
                )

            return str(content)

    return None
