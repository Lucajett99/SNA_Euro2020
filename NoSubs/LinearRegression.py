
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import mean_squared_error, r2_score
from patsy import dmatrices
import statsmodels.api as sm
import statsmodels.formula.api as smf
import researchpy as rp

df = pd.read_csv('./metrics/AllMetricsRegression.csv', sep=',', encoding='utf-8')

print(df)
# Crea il modello di regressione per verificare la relazione tra intensità e prestazioni
intensity_model = sm.OLS(df["goal_scored"], df["I_normalized_minutes"]).fit()
print(f"Coefficient {intensity_model.params}: ")

# Crea il modello di regressione per verificare la relazione tra centralità e prestazioni
centrality_model = sm.OLS(df["goal_scored"], df["Centralization"]).fit()
print(f"Coefficient {centrality_model.params}: ")

# Stampa il test di significatività per il coefficiente di regressione dell'intensità
print(f"Test di significatività intensità: p = {intensity_model.pvalues[0]}")

# Stampa il test di significatività per il coefficiente di regressione della centralità
print(f"Test di significatività centralità: p = {centrality_model.pvalues[0]}")

# Stampa se il coefficiente di regressione è significativo
print(intensity_model.pvalues[0] < 0.05)
print(centrality_model.pvalues[0] < 0.05)