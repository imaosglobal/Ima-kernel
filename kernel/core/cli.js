#!/usr/bin/env node

const { idea } = require('./idea_engine');

async function main() {
  const input = process.argv.slice(2).join(' ');

  if (!input) {
    console.log("Usage: node cli.js <idea in Hebrew>");
    process.exit(0);
  }

  console.log("[INPUT]", input);
  await idea(input);
}

main();
