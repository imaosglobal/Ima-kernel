from pathlib import Path
import json
import time
import py_compile

p=Path("learning/knowledge_provenance_connector.py")

p.write_text(r'''
from learning.source_manager import get_real_source
from learning.source_validator import validate
from learning.provenance_store import save_provenance


def import_external_knowledge(question):

    source=get_real_source(question)

    if not source:
        return {
            "state":"NO_SOURCE",
            "question":question
        }


    validation=validate(source)

    if not validation["verified"]:
        return {
            "state":"LOW_CONFIDENCE",
            "validation":validation
        }


    record=save_provenance(
        question,
        source["content"],
        {
            "name":source.get("source"),
            "url":source.get("url","")
        },
        validation
    )


    return {
        "state":"IMPORTED",
        "knowledge":record
    }

''',
encoding="utf8")


py_compile.compile(
    "learning/knowledge_provenance_connector.py",
    doraise=True
)


Path(".ima/knowledge_provenance_connector.lock").write_text(
json.dumps(
{
"state":"VERIFIED",
"pipeline":
"Source -> Validation -> Provenance -> Store",
"time":time.time()
},
ensure_ascii=False,
indent=2
),
encoding="utf8"
)


print("KNOWLEDGE PROVENANCE CONNECTOR VERIFIED")
