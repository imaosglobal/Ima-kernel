from .router_auto import choose_model
from .identity_guard import wrap_response


def run(message):

    selected = choose_model()

    # כרגע רק בחירה.
    # חיבור המנוע בפועל נשמר מופרד כדי לא להפיל את הקרנל.

    return wrap_response({
        "model": selected.get("model",
                 selected.get("provider","none")),
        "response": "",
        "status": "selected"
    })
