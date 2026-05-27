#!/bin/bash

echo "=== IMA ONTOLOGY CHECK ==="
echo

echo "Core ontology:"
cat .ima/ontology/core.json | sed 's/},{/},\n{/g'

echo
echo "Git status:"
git status
