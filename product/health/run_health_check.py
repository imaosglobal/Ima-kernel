from product.health.health_manager import save_report

r = save_report()

print("=== IMA HEALTH REPORT ===")

for k,v in r.items():
    print(k,":",v)

print("=== COMPLETE ===")
