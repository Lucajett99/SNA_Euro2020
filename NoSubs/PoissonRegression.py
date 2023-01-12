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
mask = np.random.rand(len(df)) < 0.8
df_train = df[mask]
df_test = df[~mask]
print('Training data set length='+str(len(df_train)))
print('Testing data set length='+str(len(df_test)))

expr = """goal_scored ~ possession_minutes + I_normalized_minutes + Centralization"""
y_train, X_train = dmatrices(expr, df_train, return_type='dataframe')
y_test, X_test = dmatrices(expr, df_test, return_type='dataframe')

poisson_model = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()
print(poisson_model.summary())
#print(poisson_model.params)
#poisson_predictions = poisson_model.get_prediction(X_test)
#summary_frame() returns a pandas DataFrame
#predictions_summary_frame = poisson_predictions.summary_frame()
#print(predictions_summary_frame)
