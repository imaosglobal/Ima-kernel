from founder.core import run_founder_cycle

print("=== FOUNDER CORE TEST ===")

try:
    result = run_founder_cycle()

    print("[OK] cycle completed")
    print("\nKEYS:")
    print(result.keys())

    print("\nDECISION:")
    print(result.get("decision"))

    print("\nACTIONS:")
    print(result.get("actions"))

except Exception as e:
    print("[FAILED]")
    print(type(e).__name__, e)
