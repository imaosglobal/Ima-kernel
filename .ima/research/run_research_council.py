import sys
import json
import traceback

from ima_research_council import (
    IMAResearchCouncil
)


if len(sys.argv) < 2:

    print(
        'Usage: python3 run_research_council.py "question"'
    )

    raise SystemExit(2)


question = sys.argv[1]


try:

    council = IMAResearchCouncil(
        live_log=True
    )

    result = council.investigate(
        question
    )

    print()
    print("=" * 78)
    print("IMA RESEARCH COUNCIL RESULT")
    print("=" * 78)

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )


except KeyboardInterrupt:

    print()
    print("=" * 78)
    print("RESEARCH INTERRUPTED BY USER")
    print("=" * 78)

    raise SystemExit(130)


except Exception:

    print()
    print("=" * 78)
    print("IMA RESEARCH COUNCIL ERROR")
    print("=" * 78)

    print(
        traceback.format_exc()
    )

    raise
