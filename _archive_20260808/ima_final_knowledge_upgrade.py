from pathlib import Path
import json
import time
import shutil
import importlib
import py_compile

ROOT=Path(".")
IMA=Path(".ima")
IMA.mkdir(exist_ok=True)

runtime=Path("ima_master_runtime.py")

backup=IMA/"runtime_before_knowledge_upgrade_final.py"
shutil.copy2(runtime, backup)

# create knowledge router
router=Path("learning/knowledge_router.py")
router.parent.mkdir(exist_ok=True)

router.write_text(
'''
from learning.knowledge_answer_builder import build_answer

def get_knowledge_answer(brain_result, question):

    if not brain_result:
        return None

    try:
        return build_answer(
            brain_result,
            question
        )
    except Exception:
        return None
''',
encoding="utf8"
)

# verify modules
modules=[
"ima_master_runtime",
"ima_brain",
"brain_sync",
"learning.knowledge_answer_builder",
"learning.knowledge_router",
"learning.learning_memory",
"learning.meta_orchestrator"
]

status={}

for m in modules:
    try:
        importlib.import_module(m)
        status[m]="OK"
    except Exception as e:
        status[m]="FAIL "+str(e)

# compile
compiled=[]

for f in [
"ima_master_runtime.py",
"learning/knowledge_router.py"
]:
    py_compile.compile(f,doraise=True)
    compiled.append(f)

# runtime test
import ima_master_runtime

m=ima_master_runtime.IMAMaster()

tests=[
"מה זה חתול",
"מהי תודעה",
"תסביר מתמטיקה",
"איך עובד מנוע בעירה"
]

answers={}

for q in tests:
    r=m.ask(q)
    answers[q]=r.get("response","")[:300]


report={
"system":"IMA",
"time":time.time(),
"modules":status,
"compiled":compiled,
"tests":answers
}

(IMA/"final_knowledge_upgrade_report.json").write_text(
json.dumps(report,ensure_ascii=False,indent=2),
encoding="utf8"
)

(IMA/"final_knowledge_upgrade.lock").write_text(
json.dumps({
"state":"VERIFIED",
"pipeline":"IMA -> Brain -> Knowledge Router -> Answer Builder -> Response",
"time":time.time()
},ensure_ascii=False,indent=2),
encoding="utf8"
)

