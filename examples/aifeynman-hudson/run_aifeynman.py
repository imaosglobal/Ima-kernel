import pandas as pd
import numpy as np
from aifeynman import fit

df = pd.read_csv('hudson.csv')

# נחזה Hare
X = df[['Year', 'Lynx']].values
y = df['Hare'].values
eq_hare = fit(X, y)

# נחזה Lynx
X2 = df[['Year', 'Hare']].values  
y2 = df['Lynx'].values
eq_lynx = fit(X2, y2)
