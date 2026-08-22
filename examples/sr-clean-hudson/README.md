# SR-Clean Hudson Bay Example

Symbolic Regression נקי ב-100% numpy. 
בלי PySR, בלי gplearn, בלי תלויות כבדות.

## תוצאה
dH/dt = 0.3147*Year + 5.9787*Lynx + -0.2526*Lynx^2 + -567.2518
dL/dt = 0.2710*Year + -0.2752*Hare + 0.0021*Hare^2 + -485.6417

## הרצה
cd examples/sr-clean-hudson && python run_sr_clean.py
