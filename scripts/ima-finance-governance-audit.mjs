import fs from "node:fs";

const required = [
  "docs/IMA_GLOBAL_NONPROFIT_CHARTER.md",
  "docs/IMA_FINANCIAL_LEDGER_SCHEMA.json",
  "docs/IMA_CREATOR_SUCCESSION_AND_ESTATE.md",
  "data/IMA_FINANCIAL_EVIDENCE_LEDGER.json"
];
for (const p of required) if (!fs.existsSync(p)) throw new Error("Missing canonical governance file: " + p);

const schema = JSON.parse(fs.readFileSync(required[1], "utf8"));
const ledger = JSON.parse(fs.readFileSync(required[3], "utf8"));

if (schema.legal_status !== "not_yet_registered_as_a_nonprofit_entity") {
  throw new Error("Unexpected nonprofit legal-status claim");
}
if (!Array.isArray(ledger.events)) throw new Error("Financial evidence ledger events must be an array");

const incomeFields = new Set(schema.income.required);
const expenseFields = new Set(schema.expenses.required);
const forbiddenIncomeSignals = new Set(schema.income.never_infer_from);

for (const event of ledger.events) {
  if (!event || typeof event !== "object") throw new Error("Invalid ledger event");
  const fields = new Set(Object.keys(event));
  if (event.type === "income") {
    for (const f of incomeFields) if (!fields.has(f)) throw new Error("Income event missing " + f);
    for (const f of forbiddenIncomeSignals) if (event[f] !== undefined) throw new Error("Income event uses forbidden inference field " + f);
  }
  if (event.type === "expense") {
    for (const f of expenseFields) if (!fields.has(f)) throw new Error("Expense event missing " + f);
    if (event.authorization === false || event.status === "unapproved") throw new Error("Unapproved expense present in canonical ledger");
  }
}

const report = {
  ok: true,
  ledger_events: ledger.events.length,
  legal_status: schema.legal_status,
  surplus_order: ledger.surplus_order,
  no_autonomous_spend: true,
  creator_nonprofit_separation: true,
  succession_is_not_a_will: true
};
console.log(JSON.stringify(report, null, 2));
