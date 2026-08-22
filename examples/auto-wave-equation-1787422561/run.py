import numpy as np
print("=== IMA Auto: Wave Equation ===")
x = np.linspace(0, 10, 100); y = np.sin(x) + 0.1*np.random.randn(100)
print(f"Generated {len(x)} points. Mean: {y.mean():.3f}")
