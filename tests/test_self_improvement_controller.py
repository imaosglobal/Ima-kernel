import ast
from pathlib import Path
p=Path('.ima/evolution/self_improvement_controller.py')
ast.parse(p.read_text(encoding='utf-8'))
s=p.read_text(encoding='utf-8')
assert 'unified git diff' in s
assert '.github/' in s and 'DENIED' in s
assert 'git apply --check' in s
print('SELF_IMPROVEMENT_CONTROLLER_OK')