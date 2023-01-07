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

'''
df = pd.read_csv('./metrics/AllMetricsRegression.csv', sep=',', encoding='utf-8')
df.set_index(['team','match'], inplace=True)
df_y = df['goal_scored']
df_x = df.drop(columns=['goal_scored'])

#train and split test sklearn
X_train, X_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.2, random_state=0)

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_train, y_train)

# Make predictions using the testing set
y_pred = regr.predict(X_test)

# The coefficients
print("Coefficients: \n", regr.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))


# Plot outputs
plt.scatter(X_test['I_normalized_minutes'], y_test, color="black")
plt.plot(X_test['I_normalized_minutes'], y_pred, color="blue", linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
'''

'''

df.set_index(['team','match'], inplace=True)
Y = df['goal_scored']
X = df.drop(columns=['goal_scored'])
preds, scores = [], []
kfold = KFold(n_splits=10, shuffle=True, random_state=1)
for train_idx, test_idx in kfold.split(df):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = Y.iloc[train_idx], Y.iloc[test_idx]
    expr =  "y_train ~ possession_minutes + I_normalized_minutes + Centralization"
    #poisson_model = smf.glm(formula=expr, data=X_train, family=sm.families.Poisson()).fit()
    poisson_model = sm.GLM(formula=expr, data=X_train, family=sm.families.Poisson()).fit()
    preds.append(poisson_model.get_prediction(X_test))
    #scores.append(poisson_model.score(X_test, y_test))
#print(score)
print(poisson_model.summary())
print(poisson_model.params)
'''


'''
mask = np.random.rand(len(df)) < 0.8
df_train = df[mask]
df_test = df[~mask]
print('Training data set length='+str(len(df_train)))
print('Testing data set length='+str(len(df_test)))

expr = """goal_scored ~ possession_minutes + I_normalized_minutes + Centralization"""
y_train, X_train = dmatrices(expr, df_train, return_type='dataframe')
y_test, X_test = dmatrices(expr, df_test, return_type='dataframe')

poisson_model = sm.GLM(y_train, X_train, family=sm.families.Poisson()).fit()
#print(poisson_model.summary())
print(poisson_model.params)
poisson_predictions = poisson_model.get_prediction(X_test)
#summary_frame() returns a pandas DataFrame
predictions_summary_frame = poisson_predictions.summary_frame()
print(predictions_summary_frame)
'''
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

