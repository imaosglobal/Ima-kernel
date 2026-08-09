from founder.executive_ai.learning_journal.journal_store import add_entry


def emit_event(
    module,
    event,
    data=None,
    importance=0
):

    return add_entry(

        event_type=event,

        title=event,

        source=module,

        category="system_event",

        importance=importance,

        metadata=data or {}

    )


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
