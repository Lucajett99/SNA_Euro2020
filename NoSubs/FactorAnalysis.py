from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
import pandas as pd
from scipy.stats import skew, kurtosis
from sklearn.decomposition import PCA

#import file MeanMetrics.csv
df = pd.read_csv('./metrics/AllMetrics.csv', sep=',', encoding='utf-8')
df = df.drop(columns=['network_intensity'])
df.set_index(['team','match'], inplace=True)


#KMO test
kmo_all, kmo_model = calculate_kmo(df)
print(kmo_model)

#Barlett test
test_statistic, p_value = calculate_bartlett_sphericity(df)
#p-value: the probability of getting data as far or further from the null value as your data are, if the null were true
print(p_value)

pca = PCA(n_components=1)
df_transform = pca.fit_transform(df)

allMetrics = pd.read_csv('./metrics/AllMetricsPossession.csv', sep=',', encoding='utf-8')


allMetrics = allMetrics.drop(columns=['Co'])
allMetrics = allMetrics.drop(columns=['Ci'])
#allMetrics = allMetrics.drop(columns=['weight_centralization'])
allMetrics = allMetrics.drop(columns=['possession_percentage'])
allMetrics = allMetrics.drop(columns=['network_intensity'])
allMetrics = allMetrics.drop(columns=['I_normalized_percentage'])
allMetrics['Centralization'] = df_transform

allMetrics.to_csv('./metrics/AllMetricsRegression.csv', sep=',', encoding='utf-8', index=False)
allMetrics.to_excel('./metrics/AllMetricsRegression.xlsx', index=False)
