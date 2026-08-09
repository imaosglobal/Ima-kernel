from .problem_solver import solve
from .learning import teach
from .writing import write
from .planning import plan

def choose(intent, message):
    if intent in ["learn","study"]:
        return teach(message)

    if intent in ["write","create"]:
        return write(message)

    if intent in ["plan","goal"]:
        return plan(message)

    return solve(message)
