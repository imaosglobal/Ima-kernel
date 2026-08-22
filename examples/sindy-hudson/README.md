# SINDy Hudson Bay Example

Sparse Identification of Nonlinear Dynamics ב-100% numpy.
מגלה משוואות דיפרנציאליות מדאטה.

## תוצאה
dH/dt = 58.8872 + 0.1911*H - 2.2760*L + 0.0848*L^2 - 0.0490*H*L - 0.0234*Year
dL/dt = 381.7716 - 0.1625*H - 1.3829*L + 0.0423*L^2 + 0.0118*H*L - 0.2022*Year

## הרצה
cd examples/sindy-hudson && python run_sindy.py
