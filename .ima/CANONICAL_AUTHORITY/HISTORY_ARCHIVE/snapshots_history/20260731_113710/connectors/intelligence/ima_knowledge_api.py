import sys
from knowledge_router import ask
import json

if __name__=="__main__":

    if len(sys.argv)>1:
        result=ask(sys.argv[1])

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )
