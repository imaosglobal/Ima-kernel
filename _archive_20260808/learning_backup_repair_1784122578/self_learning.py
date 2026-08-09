
from learning.learning_memory import store_pattern
import time

SELF_FILE="learning/self_learning.json"

def learn_self(pattern):
    store_pattern("SELF:"+pattern)

    return {
        "time":time.time(),
        "learned":pattern,
        "status":"self_learning"
    }
