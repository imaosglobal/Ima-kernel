import os
import json


# 1 MEMORY
try:
    from ima_system import load_memory, memory_store
    mem = load_memory()
except Exception as e:


# 2 LEARNING LOOP
try:
    from learning.ima_learning_loop import run_ima_learning_loop
except Exception as e:


# 3 KNOWLEDGE ENGINE
try:
    from engines.knowledge_engine import search_knowledge
    result = search_knowledge("מנוע בעירה")
except Exception as e:


# 4 LLM
try:
    from ima_system import llm_answer
except Exception as e:


# FILE INVENTORY
for path in [
    ".ima/memory.json",
    ".ima/ledger.jsonl",
    ".ima/personality.json",
    ".ima/voice.json"
]:


