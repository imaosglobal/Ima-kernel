import json
import time
from pathlib import Path

ROOT = Path.home() / "ima_kernel"
DATA = ROOT / ".ima" / "research" / "embodied_language"
DATA.mkdir(parents=True, exist_ok=True)

DOMAIN_FILE = DATA / "domain.json"
OBSERVATIONS = DATA / "observations.jsonl"
HYPOTHESES = DATA / "hypotheses.jsonl"

SEED = {
    "domain": "embodied_language",
    "description": (
        "Cross-linguistic study of mappings between body, perception, "
        "action, space, metaphor, concepts and language."
    ),

    "languages": [
        "Hebrew",
        "Arabic",
        "English",
        "Spanish",
        "French",
        "Greek",
        "Persian",
        "Turkish",
        "Japanese",
        "Mandarin Chinese",
        "Vietnamese",
        "Indonesian",
        "Hungarian",
        "Czech",
        "Marathi",
        "Wolof",
        "Khoekhoe"
    ],

    "concepts": [
        "head", "hand", "foot", "eye", "ear",
        "mouth", "tongue", "heart", "back", "belly",
        "face", "arm", "leg", "finger",

        "see", "hear", "touch", "hold", "release",
        "move", "fall", "rise", "enter", "exit",
        "open", "close",

        "near", "far", "up", "down",
        "front", "back", "inside", "outside",
        "center", "edge", "depth",

        "light", "dark", "heavy", "lightness",
        "connection", "separation",
        "support", "control",
        "knowledge", "understanding",
        "emotion", "time", "change"
    ],

    "mapping_layers": [
        "body",
        "perception",
        "action",
        "space",
        "object",
        "relation",
        "emotion",
        "cognition",
        "social",
        "time",
        "grammar"
    ],

    "rules": [
        "similar spelling is not evidence of common etymology",
        "separate cognitive mapping from historical etymology",
        "store evidence and uncertainty",
        "compare unrelated languages",
        "hypotheses must remain hypotheses until validated",
        "distinguish universal, cultural, linguistic and individual mappings",
        "never promote an unverified hypothesis to fact"
    ],

    "created": time.time()
}

if not DOMAIN_FILE.exists():
    DOMAIN_FILE.write_text(
        json.dumps(SEED, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_domain():
    return json.loads(
        DOMAIN_FILE.read_text(encoding="utf-8")
    )


def record_observation(observation):
    observation = {
        "timestamp": time.time(),
        **observation
    }

    with OBSERVATIONS.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                observation,
                ensure_ascii=False
            ) + "\n"
        )


def record_hypothesis(hypothesis):
    hypothesis = {
        "timestamp": time.time(),
        "status": "hypothesis",
        **hypothesis
    }

    with HYPOTHESES.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                hypothesis,
                ensure_ascii=False
            ) + "\n"
        )


def research_domain():
    return load_domain()


if __name__ == "__main__":
    d = load_domain()

    print("IMA Embodied Language Domain")
    print("Languages:", len(d["languages"]))
    print("Concepts:", len(d["concepts"]))
    print("Layers:", len(d["mapping_layers"]))
    print("Rules:", len(d["rules"]))
    print("Status: READY")
