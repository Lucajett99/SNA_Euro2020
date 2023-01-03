import pandas as pd
from patsy import dmatrices
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import researchpy as rp

''''
df = pd.read_csv('./metrics/AllMetricsRegression.csv', sep=',', encoding='utf-8')
summary = rp.summary_cont(df.groupby(["team"])["I_normalized_minutes"])
print(summary)
'''

df = pd.read_csv('./metrics/AllMetricsRegression.csv', sep=',', encoding='utf-8')
df.set_index(['team','match'], inplace=True)
print(df)
mask = np.random.rand(len(df)) < 0.8
df_train = df[mask]
df_test = df[~mask]
print('Training data set length='+str(len(df_train)))
print('Testing data set length='+str(len(df_test)))
expr = """goal_scored ~ C(team) + C(match) + possession_percentage + I_normalized_minutes + Centralization"""
y_train, X_train = dmatrices(expr, df_train, return_type='dataframe')
y_test, X_test = dmatrices(expr, df_test, return_type='dataframe')
poisson_training_results = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()
#print(poisson_training_results.summary())
print(X_train)
print(X_test)

poisson_predictions = poisson_training_results.get_prediction(X_test)
#summary_frame() returns a pandas DataFrame
predictions_summary_frame = poisson_predictions.summary_frame()
print(predictions_summary_frame)