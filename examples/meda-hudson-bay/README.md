# MEDA Hudson Bay Example

דוגמה מלאה של הרצת MEDA data_anchored על דאטה אמיתי של ארנבים ולינקסים.
נעשה דרך אמא + Termux.

## תוצאה
dH/dt = +0.3076*H -0.0010*H^2 
dL/dt = +0.0282*H -0.0043*L^2
Fitness: 0.8455

## הרצה
cd external/MEDA && python3 skills/meda/scripts/main.py --mode data_anchored --setup ../../examples/meda-hudson-bay/setup.yaml --problem ../../examples/meda-hudson-bay/problem.json --data ../../examples/meda-hudson-bay/hudson.csv --output results.json
