"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../../../..");
const DIR = path.join(ROOT, ".ima", "runtime", "memory");
const FILE = path.join(DIR, "memory.jsonl");

const TYPES = Object.freeze([
  "working",
  "episodic",
  "semantic",
  "personal",
  "artifact",
  "relationship"
]);

function ensure() {
  fs.mkdirSync(DIR, { recursive: true });
  if (!fs.existsSync(FILE)) fs.writeFileSync(FILE, "", "utf8");
}

function idFor(record) {
  return crypto
    .createHash("sha256")
    .update(JSON.stringify(record))
    .digest("hex");
}

function append(input) {
  if (!input || !TYPES.includes(input.type)) {
    throw new Error("Invalid memory type");
  }

  ensure();

  const record = {
    id: idFor({
      type: input.type,
      content: input.content,
      provenance: input.provenance || null
    }),
    type: input.type,
    content: input.content,
    provenance: input.provenance || null,
    status: input.status || "active",
    created_at: new Date().toISOString()
  };

  fs.appendFileSync(FILE, JSON.stringify(record) + "\n", "utf8");
  return record;
}

function list(type = null) {
  ensure();

  return fs.readFileSync(FILE, "utf8")
    .split("\n")
    .filter(Boolean)
    .map(line => JSON.parse(line))
    .filter(record => !type || record.type === type);
}

function search(query) {
  const q = String(query || "").toLowerCase();

  return list().filter(record =>
    JSON.stringify(record).toLowerCase().includes(q)
  );
}

function status() {
  return {
    file: FILE,
    types: TYPES.slice(),
    records: list().length
  };
}

module.exports = {
  TYPES,
  append,
  list,
  search,
  status
};
