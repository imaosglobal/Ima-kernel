from pathlib import Path
import py_compile

p=Path("learning/source_registry.py")

text=p.read_text(encoding="utf8")

start=text.index("    def collect(self, question):")

new_method='''    def collect(self, question):
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

                if not result:
                    continue

                content=result.get("content","")

                # חסימת HTML זבל
                bad=[
                    "<html",
                    "<!doctype",
                    "javascript",
                    "function(",
                    "document.",
                    "window.",
                    "css",
                    "gform"
                ]

                lower=content.lower()

                if any(x in lower for x in bad):
                    continue

                if len(content.strip()) < 80:
                    continue

                result["registry_source"]=source["name"]
                result["retrieved_at"]=time.time()

                results.append(result)

            except Exception as e:
                print("[SOURCE ERROR]",source.get("name"),e)

        return results
'''

text=text[:start]+new_method

p.write_text(text,encoding="utf8")

py_compile.compile(
    "learning/source_registry.py",
    doraise=True
)

print("[OK] Knowledge Gate installed")
