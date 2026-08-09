from founder.executive_ai.community.conversation_memory import save_message


def respond(user,message):

    save_message(
        user,
        message
    )

    return {

        "user":user,

        "response":
        "IMA received your message: " + message,

        "status":
        "processed"

    }
