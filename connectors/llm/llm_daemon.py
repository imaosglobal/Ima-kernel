import time
from .discovery_engine import discover
from .model_selector import select


def cycle():

    while True:
        try:
            discover()
            select()
        except Exception:
            pass

        time.sleep(3600)


if __name__=="__main__":
    cycle()
