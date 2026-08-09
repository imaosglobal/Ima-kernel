from .model_selector import current
from .executor import execute
from .identity_guard import wrap_response


def ask(message):

    selection=current()

    model=selection.get("selected",{}).get("model")

    if not model:
        return {
            "identity":"IMA",
            "status":"no_model"
        }

    result=execute(model,message)

    return wrap_response(result,"IMA")
