import pandas as pd
import numpy as np

df = # pd.read_csv('hudson.csv')

dt = 1
dH = np.gradient(df['Hare'].values, dt)
dL = np.gradient(df['Lynx'].values, dt)

H = df['Hare'].values
L = df['Lynx'].values
Year = df['Year'].values
Theta = np.column_stack([np.ones(len(H)), H, L, H**2, L**2, H*L, Year])

from numpy.linalg import lstsq
coef_H = lstsq(Theta, dH, rcond=None)[0]
coef_L = lstsq(Theta, dL, rcond=None)[0]

terms = ['1', 'H', 'L', 'H^2', 'L^2', 'H*L', 'Year']
eqH = ''
for c, t in zip(coef_H, terms):
    if abs(c) > 0.01: eqH += f' {c:.4f}*{t} +'

eqL = ''
for c, t in zip(coef_L, terms):
    if abs(c) > 0.01: eqL += f' {c:.4f}*{t} +'
