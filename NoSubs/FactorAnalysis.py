from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity
import pandas as pd
from scipy.stats import skew, kurtosis
from sklearn.decomposition import PCA

#import file MeanMetrics.csv
df = pd.read_csv('./metrics/AllMetrics.csv', sep=',', encoding='utf-8')
df = df.drop(columns=['network_intensity'])
df.set_index(['team','match'], inplace=True)

print(df)

#KMO test
kmo_all, kmo_model = calculate_kmo(df)

#Barlett test
values = calculate_bartlett_sphericity(df)

pca = PCA(n_components=1)
pca.fit(df)
df_transform = pca.transform(df)
print(pca.get_feature_names_out())

'''
#using scikit-learn library to do the pca factor analysis only one factor with an eigenvalue greater than 1 is retrieved
from sklearn.decomposition import PCA
pca = PCA(n_components=1)
pca.fit(df)
print(pca.components_)
df_transform = pca.transform(df)
print(df_transform)

# Calculate the skewness
print(skew(df_transform, axis=0, bias=True))

# Calculate the kurtosis
print(kurtosis(df_transform, axis=0, bias=True))
'''
