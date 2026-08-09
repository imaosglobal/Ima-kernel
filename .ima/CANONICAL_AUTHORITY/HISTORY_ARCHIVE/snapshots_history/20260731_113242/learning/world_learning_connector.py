
from learning.external_knowledge_source import fetch_external
from learning.knowledge_validator import validate
from learning.world_knowledge_store import save
from learning.world_graph_updater import add_node
from learning.world_memory import remember
from learning.provenance_store import save_provenance


def learn(question):

    source=fetch_external(question)

    if not source:
        return {
            "state":"NO_SOURCE",
            "question":question
        }


    ok,confidence=validate(source)

    if not ok:
        return {
            "state":"REJECTED"
        }


    stored=save(question,{
        **source,
        "confidence":confidence
    })


    save_provenance(
        question,
        stored.get("content",""),
        stored.get("source","unknown"),
        {
            "confidence":confidence,
            "provider":stored.get("provider","unknown")
        }
    )


    node=add_node(question,stored)

    remember(question,stored)


    return {
        "state":"LEARNED",
        "store":stored,
        "node":node,
        "memory":True
    }
