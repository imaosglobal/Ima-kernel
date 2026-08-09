from pathlib import Path
import json
from datetime import datetime

BASE=Path.home()/".ima/evolution"
BASE.mkdir(parents=True, exist_ok=True)

brain=BASE/"evolution_brain.json"

data={
    "generated": datetime.now().isoformat(),

    "system":"IMA",

    "source":{
        "git_history":"loaded",
        "capabilities":"385 extracted",
        "knowledge_graph":"connected"
    },

    "current_state":{
        "domains":[
            "kernel",
            "memory_learning",
            "product",
            "interface",
            "automation",
            "knowledge"
        ],

        "engines_created_today":[
            "pattern_engine",
            "principle_engine",
            "compression_engine",
            "self_expansion_engine",
            "relation_learning_engine",
            "meta_learning"
        ]
    },

    "analysis":{

        "strong_capabilities":[
            "kernel",
            "automation",
            "memory"
        ],

        "missing_capabilities":[
            "planning",
            "decision",
            "evaluation",
            "goal_management"
        ]
    },

    "next_plan":[
        {
            "priority":1,
            "task":"connect knowledge router to kernel",
            "reason":"knowledge exists but runtime cannot fully consume it"
        },
        {
            "priority":2,
            "task":"build lightweight planning engine",
            "reason":"convert understanding into actions"
        },
        {
            "priority":3,
            "task":"daily evolution scheduler",
            "reason":"continue without overload"
        }
    ]
}


brain.write_text(
    json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )
)

print("EVOLUTION BRAIN CREATED")
