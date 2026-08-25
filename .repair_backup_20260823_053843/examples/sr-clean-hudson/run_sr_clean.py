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

# אותו דבר ל-Lynx
X2 = np.column_stack([
    df['Year'].values,
    df['Hare'].values,
    df['Hare'].values**2,
    np.ones(len(df))
])
y2 = df['Lynx'].values
coef2 = np.linalg.lstsq(X2, y2, rcond=None)[0]
