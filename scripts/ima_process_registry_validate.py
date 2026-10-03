#!/usr/bin/env python3
"""Validate the canonical IMA process registry without executing any process."""
import json
from pathlib import Path

REGISTRY = Path('.ima/process_registry.json')
REQUIRED = {
    'process_id', 'version', 'owner', 'enabled', 'trigger', 'risk_tier',
    'approval', 'side_effects', 'permissions', 'timeout_minutes',
    'concurrency_group', 'health_check', 'rollback'
}
ALLOWED_RISKS = {'low', 'medium', 'high', 'critical'}


def main():
    data = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if data.get('schema_version') != '1.0':
        raise SystemExit('invalid schema_version')
    processes = data.get('processes')
    if not isinstance(processes, list) or not processes:
        raise SystemExit('registry has no processes')
    ids = set()
    for item in processes:
        missing = REQUIRED - item.keys()
        if missing:
            raise SystemExit(f"{item.get('process_id', '<unknown>')}: missing {sorted(missing)}")
        pid = item['process_id']
        if pid in ids:
            raise SystemExit(f'duplicate process_id: {pid}')
        ids.add(pid)
        if item['risk_tier'] not in ALLOWED_RISKS:
            raise SystemExit(f'{pid}: invalid risk_tier')
        if not isinstance(item['timeout_minutes'], int) or item['timeout_minutes'] <= 0:
            raise SystemExit(f'{pid}: timeout_minutes must be positive integer')
        if not isinstance(item['side_effects'], list) or not isinstance(item['permissions'], list):
            raise SystemExit(f'{pid}: side_effects and permissions must be arrays')
    print(f'IMA process registry valid: {len(processes)} process(es)')


if __name__ == '__main__':
    main()
