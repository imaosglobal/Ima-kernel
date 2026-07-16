from pathlib import Path
import sys

ROOT=Path(".ima/agi_evolution").resolve()
sys.path.insert(0,str(ROOT))

import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))

from agi_orchestrator import AGI


class IMAGIBridge:

    def __init__(self):
        self.agi=AGI


    def process(self,message,context=None):

        result=self.agi.process(
            message,
            context or {}
        )

        return {
            "source":"IMA_AGI_LAYER",
            "message":message,
            "capabilities":result
        }


IMA_AGI=IMAGIBridge()


if __name__=="__main__":
    print(
        IMA_AGI.process(
            "איך אמא יכולה ללמוד להשתפר?"
        )
    )
