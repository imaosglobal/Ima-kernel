import pandas as pd
import numpy as np

df = # pd.read_csv('hudson.csv')

# נבנה פיצ'רים ידנית: Year, L, L^2, 1
X = np.column_stack([
    df['Year'].values,
    df['Lynx'].values,
    df['Lynx'].values**2,
    np.ones(len(df))
])
y = df['Hare'].values

# רגרסיה לינארית
coef = np.linalg.lstsq(X, y, rcond=None)[0]
print('=== Equation for Hare ===')
print(f'dH/dt = {coef[0]:.4f}*Year + {coef[1]:.4f}*Lynx + {coef[2]:.4f}*Lynx^2 + {coef[3]:.4f}')

# אותו דבר ל-Lynx
X2 = np.column_stack([
    df['Year'].values,
    df['Hare'].values,
    df['Hare'].values**2,
    np.ones(len(df))
])
y2 = df['Lynx'].values
coef2 = np.linalg.lstsq(X2, y2, rcond=None)[0]
print('\n=== Equation for Lynx ===')
print(f'dL/dt = {coef2[0]:.4f}*Year + {coef2[1]:.4f}*Hare + {coef2[2]:.4f}*Hare^2 + {coef2[3]:.4f}')
