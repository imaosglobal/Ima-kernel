import numpy as np
price=100*np.cumprod(1+0.01*np.random.randn(100))
print('Stock sim done. Final:', price[-1])