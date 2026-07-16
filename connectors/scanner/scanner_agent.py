import json
from pathlib import Path
import sys

sys.path.append(
    str(Path(__file__).parent.parent / "intelligence")
)

from knowledge_engine import learn,update_graph


SOURCES=[
 {
  "name":"beecomm",
  "type":"pos",
  "abilities":[
   "sales",
   "inventory",
   "customers"
  ]
 },
 {
  "name":"odoo",
  "type":"erp",
  "abilities":[
   "accounting",
   "inventory",
   "business_processes"
  ]
 },
 {
  "name":"shopify",
  "type":"ecommerce",
  "abilities":[
   "products",
   "orders",
   "customers"
  ]
 }
]


for software in SOURCES:
    for ability in software["abilities"]:
        learn(
            ability,
            software["name"],
            0.8
        )

update_graph()

print(
 "SCAN COMPLETE:",
 len(SOURCES),
 "software profiles"
)
