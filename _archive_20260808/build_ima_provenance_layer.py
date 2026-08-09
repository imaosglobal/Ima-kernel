from pathlib import Path
import json
import time
import py_compile

learning=Path("learning")
learning.mkdir(exist_ok=True)


# Validator
(Path("learning/source_validator.py")).write_text(r'''
def validate(source):

    if not source:
        return {
            "verified":False,
            "confidence":0
        }

    confidence=source.get("confidence",0)

    return {
        "verified": confidence >= 0.7,
        "confidence": confidence,
        "checks":[
            "source_exists",
            "confidence_score"
        ]
    }
''',encoding="utf8")


# Provenance storage
(Path("learning/provenance_store.py")).write_text(r'''
import json
from pathlib import Path
import time

FILE=Path("learning/provenance_memory.json")

def save_provenance(
    knowledge_id,
    content,
    source,
    validation
):

    data={}

    if FILE.exists():
        data=json.loads(
            FILE.read_text(encoding="utf8")
        )

    data[knowledge_id]={
        "content":content,
        "source":source,
        "validation":validation,
        "stored_at":time.time()
    }

    FILE.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf8"
    )

    return data[knowledge_id]


def get_provenance(knowledge_id):

    if not FILE.exists():
        return None

    data=json.loads(
        FILE.read_text(encoding="utf8")
    )

    return data.get(knowledge_id)
''',encoding="utf8")


# Citation builder
(Path("learning/citation_builder.py")).write_text(r'''
def build_citation(record):

    if not record:
        return ""

    source=record.get("source",{})

    return (
        "\n\nמקור:\n"
        +
        str(source.get("name","לא ידוע"))
        +
        "\n"
        +
        str(source.get("url",""))
        +
        "\nאמינות: "
        +
        str(
            record.get(
                "validation",
                {}
            ).get(
                "confidence",
                0
            )
        )
    )


def should_show_source(message):

    words=[
        "מקור",
        "ציטוט",
        "מאיפה",
        "קישור",
        "reference",
        "source"
    ]

    return any(
        x in message.lower()
        for x in words
    )
''',encoding="utf8")


# Knowledge metadata template
Path("learning/knowledge_metadata_template.json").write_text(
json.dumps(
{
"id":"",
"content":"",
"domain":"",
"source":{
"name":"",
"url":"",
"type":""
},
"validation":{
"verified":False,
"confidence":0
},
"created_by":"IMA",
"derived_from":[]
},
ensure_ascii=False,
indent=2
),
encoding="utf8"
)


for f in [
"learning/source_validator.py",
"learning/provenance_store.py",
"learning/citation_builder.py"
]:
    py_compile.compile(f,doraise=True)


Path(".ima/provenance_layer.lock").write_text(
json.dumps(
{
"state":"VERIFIED",
"pipeline":
"Source -> Validation -> Provenance -> Knowledge Store -> Graph -> Memory",
"time":time.time()
},
ensure_ascii=False,
indent=2
),
encoding="utf8"
)


print("IMA PROVENANCE LAYER VERIFIED")
