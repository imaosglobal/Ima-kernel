from .manager import recall, remember


def get_context():
    return recall()


def store_interaction(message, response):
    remember(
        "last_interaction",
        {
            "message": message,
            "response": response[:500]
        }
    )
