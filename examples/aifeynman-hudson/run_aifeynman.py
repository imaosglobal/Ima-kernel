import pandas as pd
import numpy as np
from aifeynman import fit

df = pd.read_csv('hudson.csv')

# נחזה Hare
X = df[['Year', 'Lynx']].values
y = df['Hare'].values
print('=== Fitting Hare ===')
eq_hare = fit(X, y)
print('Equation for Hare:', eq_hare)

# נחזה Lynx
X2 = df[['Year', 'Hare']].values  
y2 = df['Lynx'].values
print('\n=== Fitting Lynx ===')
eq_lynx = fit(X2, y2)
print('Equation for Lynx:', eq_lynx)
