import json, pathlib

reg = pathlib.Path("../registry/connectors.json").resolve()

if reg.exists():
    data = json.loads(reg.read_text())
else:
    data = {"version":1,"connectors":[]}

default = [
    "beecomm",
    "square",
    "lightspeed",
    "clover",
    "toast",
    "shopify_pos",
    "oracle_micros",
    "odoo",
    "erply",
    "loyverse",
    "revel",
    "sumup",
    "stripe_terminal",
    "zoho_inventory",
    "sap_business_one",
    "microsoft_dynamics365",
    "netsuite",
    "quickbooks",
    "xero",
    "woocommerce",
    "magento",
    "prestashop"
]

known = {c["id"] for c in data["connectors"]}

for name in default:
    if name not in known:
        data["connectors"].append({
            "id": name,
            "status": "available",
            "installed": False
        })

reg.write_text(json.dumps(data,indent=2))
print("Connectors:",len(data["connectors"]))
