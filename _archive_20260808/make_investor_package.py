from pathlib import Path

files = {
"investor/architecture_diagram.md": [
"# IMA Architecture",
"",
"USER",
" |",
" v",
"Product Gateway",
" |",
" v",
"IMA Master Runtime",
" |",
"+----------------+",
"| Brain          |",
"| Memory         |",
"| Learning Loop  |",
"+----------------+",
" |",
" v",
"Historical Inference",
" |",
" v",
"Personal Intelligence",
" |",
" v",
"Web / Android / API / Devices",
"",
"Principle:",
"Memory -> Learning -> Understanding"
],

"investor/demo_script.md": [
"# IMA Investor Demo",
"",
"1. User asks: What did you learn from me?",
"2. IMA retrieves memory.",
"3. IMA extracts patterns.",
"4. IMA creates historical conclusions.",
"5. IMA demonstrates controlled learning."
],

"investor/valuation.md": [
"# IMA Valuation Hypothesis",
"",
"Stage: Early AI prototype.",
"",
"Value:",
"- AI memory architecture",
"- Learning system",
"- Personal intelligence layer",
"",
"Future:",
"- Investment",
"- Partnerships",
"- Commercial product"
],

"docs/IMA_STATUS_v1.md": [
"# IMA Status",
"",
"Working:",
"- Runtime",
"- Brain",
"- Memory",
"- Learning",
"- Historical inference",
"- Product layer",
"",
"Next:",
"- Team",
"- Partnerships",
"- Users"
]
}

for name, lines in files.items():
    p=Path(name)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lines)+"\n", encoding="utf-8")

print("DONE")
