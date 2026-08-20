from founder.executive_ai.learning_journal.journal_store import add_entry
from founder.executive_ai.memory.autobiography_bus import ima_event


def emit_event(
    module,
    event,
    data=None,
    importance=0
):

    result = add_entry(

        event_type=event,

        title=event,

        source=module,

        category="system_event",

        importance=importance,

        metadata=data or {}

    )

    # CANONICAL IMA AUTOBIOGRAPHY
    try:
        ima_event(
            event_type=event,
            event={
                "module": module,
                "event": event,
                "data": data or {},
                "importance": importance,
            },
            source=module,
            metadata={
                "origin": "learning_journal.event_bus",
            },
        )
    except Exception:
        pass

    return result


def record_problem(
    module,
    problem,
    solution
):

    return add_entry(

        event_type="problem_solution",

        title=problem,

        problem=problem,

        solution=solution,

        source=module,

        category="learning",

        importance=90

    )
