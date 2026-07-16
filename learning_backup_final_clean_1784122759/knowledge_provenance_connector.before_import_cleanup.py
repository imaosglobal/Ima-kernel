
from learning.source_manager from learning.sources.html_extractor import extract_text
import get_real_source
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

