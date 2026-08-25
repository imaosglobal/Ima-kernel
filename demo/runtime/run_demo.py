from product.gateway.product_gateway import ask
from product.health.health_manager import health_report

print("=== IMA DEMO ===")

print("\nSYSTEM:")
print(health_report())

print("\nQUESTION:")
print("What did you learn from me?")

print("\nIMA:")
print(
    ask("מה למדת ממני?")["response"]
)
