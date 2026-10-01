#!/usr/bin/env node
import fs from 'node:fs';

const file = process.argv[2] || 'ima-next-action-report.json';
const report = JSON.parse(fs.readFileSync(file, 'utf8'));

if (report.tool !== 'IMA Next Action') throw new Error('Unexpected tool name');
if (!Array.isArray(report.next_actions)) throw new Error('next_actions must be an array');
if (report.unresolved_count !== report.next_actions.length) throw new Error('unresolved_count mismatch');

for (let i = 0; i < report.next_actions.length; i += 1) {
  const row = report.next_actions[i];
  if (row.priority !== i + 1) throw new Error('priority sequence mismatch');
  if (!row.id || !row.status || !row.next_step || !row.boundary) throw new Error('incomplete action row');
}

console.log('IMA next-action report: PASS');
