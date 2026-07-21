import os
import json

print("=== IMA FULL SYSTEM CHECK ===")

# 1 MEMORY
print("\n[MEMORY]")
try:
    from ima_system import load_memory, memory_store
    mem = load_memory()
    print("memory.json:", os.path.exists(".ima/memory.json"))
    print("topics:", mem.get("topics", [])[-5:])
    print("history:", len(mem.get("history", [])))
except Exception as e:
    print("MEMORY ERROR:", e)


# 2 LEARNING LOOP
print("\n[LEARNING]")
try:
    from learning.ima_learning_loop import run_ima_learning_loop
    print("learning loop import: OK")
    print("function:", run_ima_learning_loop)
except Exception as e:
    print("LEARNING ERROR:", e)


# 3 KNOWLEDGE ENGINE
print("\n[KNOWLEDGE]")
try:
    from engines.knowledge_engine import search_knowledge
    result = search_knowledge("מנוע בעירה")
    print("knowledge engine: OK")
    print("sample:", result)
except Exception as e:
    print("KNOWLEDGE ERROR:", e)


# 4 LLM
print("\n[LLM]")
try:
    from ima_system import llm_answer
    print("llm layer exists: OK")
except Exception as e:
    print("LLM ERROR:", e)


# FILE INVENTORY
print("\n[FILES]")
for path in [
    ".ima/memory.json",
    ".ima/ledger.jsonl",
    ".ima/personality.json",
    ".ima/voice.json"
]:
    print(path, "OK" if os.path.exists(path) else "MISSING")


print("\n=== CHECK COMPLETE ===")
