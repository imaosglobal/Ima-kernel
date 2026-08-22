import pandas as pd
import numpy as np
from gplearn.genetic import SymbolicRegressor
from gplearn.functions import make_function

df = pd.read_csv('hudson.csv')
X = df[['Year', 'Lynx']].values
y = df['Hare'].values

model = SymbolicRegressor(
    population_size=1000,
    generations=20,
    function_set=['add', 'sub', 'mul', 'div'],
    random_state=42,
    verbose=1
)
model.fit(X, y)
print('=== Equation for Hare ===')
print(model._program)

X2 = df[['Year', 'Hare']].values
y2 = df['Lynx'].values
model2 = SymbolicRegressor(population_size=1000, generations=20, random_state=42, verbose=1)
model2.fit(X2, y2)
print('\n=== Equation for Lynx ===')
print(model2._program)
