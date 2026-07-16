import time


class SourceRegistry:

    def __init__(self):
        self.sources=[]


    def register(self, name, handler, priority=0):

        self.sources.append(
            {
                "name":name,
                "handler":handler,
                "priority":priority,
                "enabled":True
            }
        )


    def collect(self, question):

        results=[]

        for source in sorted(
            self.sources,
            key=lambda x:x["priority"],
            reverse=True
        ):

            if not source["enabled"]:
                continue

            try:
                result=source["handler"](question)

                if result:

                    result["registry_source"]=source["name"]
                    result["retrieved_at"]=time.time()

                    results.append(result)

            except Exception:
                pass


        return results
