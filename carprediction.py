# -*- coding: utf-8 -*-
"""carPrediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1i3rLhfit4Yljp9OuehRVVv2nQqOBsk_D
"""

# Commented out IPython magic to ensure Python compatibility.
# importing libraries
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import seaborn as sns
sns.set()
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# %matplotlib inline

# reading data
data=pd.read_csv("/content/data.csv")
data.info()

data.head()

data.shape

#check if there is null values help us to hundle missing values in training phases
data.isnull().sum()

data.duplicated().sum()

# scaler = MinMaxScaler()
# data[['engine_hp', 'popularity']] = scaler.fit_transform(data[['engine_hp', 'popularity']])

# pca = PCA(n_components=2)
# data_reduced = pca.fit_transform(data)

data

#cleaning data =editing in dataset
data.columns=data.columns.str.lower().str.replace(' ','_')

stringColumns=list(data.dtypes[data.dtypes=='object'].index)

for col in stringColumns:
  data[col]=data[col].str.lower().str.replace(' ','_')

#change column name msrp to price
data.rename(columns = {'msrp': 'price'}, inplace = True)

#2 floating point after (,)
pd.options.display.float_format='{:,.2f}'.format
data.describe()

data

#suppose we want to count number of cars in make column
data.make.value_counts()

#calc the average price in price column after year >2015
data[data['year'] >= 2015]['price'].mean()

#Visualization of data
plt.figure(figsize=(7, 4))

sns.histplot(data.price[data.price < 80000], bins=20)
plt.ylabel('Frequency')
plt.xlabel('Price')
plt.title('Distribution of prices')

plt.show()

# Example line plot
plt.figure(figsize=(8, 6))
sns.lineplot(data.price[data.price < 80000])
plt.title('Line Plot')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Example scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(data.popularity)
plt.title('Scatter Plot')
plt.xlabel('popularity')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(8, 6))
sns.barplot(data.engine_hp[data.engine_hp >800])
plt.title('Bar Plot')
plt.xlabel('engine_hp')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(18, 16))
plt.pie(data['make'].value_counts(), labels=data['make'].unique(), autopct='%1.1f%%', startangle=140)
plt.title('Pie Chart')
plt.show()

figsize = (12, 1.2 * len(data['vehicle_size'].unique()))
plt.figure(figsize=figsize)
sns.violinplot(data, x='year', y='vehicle_size', inner='box', palette='Dark2')

# sns.despine(top=True, right=True, bottom=True, left=True)

plt.figure(figsize=(15, 7))

sns.histplot(data.price, bins=40)
plt.ylabel('Frequency')
plt.xlabel('Price')
plt.title('Distribution of prices')

plt.show()
#problem!!!!!

data['log_price'] = np.log1p(data.price)

plt.figure(figsize=(6, 4))

sns.histplot(data.log_price, bins=40)
plt.ylabel('Frequency')
plt.xlabel('Log(Price + 1)')
plt.title('Distribution of prices after log tranformation')

plt.show()
#normal Distribution

data.price.skew()

data.log_price.skew()

#start Validation

np.random.seed(2)     # Fixes the random seed to make sure that the results are reproducible

n = len(data)

n_val = int(0.2 * n)
n_test = int(0.2 * n)
n_train = n - (n_val + n_test)

print('No. of rows for training : ', n_train)
print('No. of rows for validation : ', n_val)
print('No. of rows for testing : ', n_test)

idx = np.arange(n)
print(idx)
np.random.shuffle(idx)
print(idx)

df_shuffled = data.iloc[idx]
print(data.index)
print(df_shuffled.index)

df_shuffled

data

df_train = df_shuffled.iloc[:n_train].copy()
df_val = df_shuffled.iloc[n_train:n_train+n_val].copy()
df_test = df_shuffled.iloc[n_train+n_val:].copy()

df_train.shape

df_val.shape

df_test.shape

#split target
y_train = df_train.log_price.values
y_val = df_val.log_price.values
y_test = df_test.log_price.values

#Baseline Solution
base = ['engine_hp', 'engine_cylinders', 'highway_mpg', 'city_mpg', 'popularity']   # Think about Numerical only

data[base]

data[base].isnull().sum()

#function to Handling Missing Values
def prepare_X(data):
    data_num = data[base]
    data_num = data_num.fillna(data_num.mean())
    X = data_num.values
    return X

def linear_regression(xi):
    n =len(xi)                # Number of features used

    pred = w0                 # Initial / Base prediction

    for j in range(n):
        pred += w[j]*xi[j]     # Formula = w0 +sigma[0:n-1]{w[j]*xi[j]}

    return pred

def train_linear_regression(X, y):
    ones = np.ones(X.shape[0])
    X = np.column_stack([ones, X])

    XTX = X.T.dot(X)
    XTX_inv = np.linalg.inv(XTX)
    w = XTX_inv.dot(X.T).dot(y)

    return w[0], w[1:]

X_train = prepare_X(df_train)
w_0, w = train_linear_regression(X_train, y_train)
y_pred = w_0 + X_train.dot(w)

sns.histplot(y_train, label='target')
sns.histplot(y_pred, label='prediction', color='red')

plt.legend()

plt.ylabel('Frequency')
plt.xlabel('Log(Price + 1)')
plt.title('Predictions vs actual distribution')

plt.show()

def rmse(y, y_pred):
    error = y_pred - y
    mse = (error ** 2).mean()
    return np.sqrt(mse)

rmse(y_train, y_pred)

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)

rmse(y_val, y_pred)

#feature Engineering
sorted(data.year.unique())

def prepare_X(df):
    df = df.copy()
    features = base.copy()

    df['age'] = 2017 - df.year    # Because the dataset was created in 2017 (which we can verify by checking df_train.year.max())
    features.append('age')

    df_num = df[features]
    df_num = df_num.fillna(df_num.mean())
    X = df_num.values
    return X

X_train = prepare_X(df_train)
w_0, w = train_linear_regression(X_train, y_train)
y_pred = w_0 + X_train.dot(w)
print('Train RMSE: ', rmse(y_train, y_pred))

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)
print('Validation RMSE: ', rmse(y_val, y_pred))

#Handling Categorical Variables(oneHotEncoding)
data.number_of_doors.value_counts()

data['make'].unique()

data['make'].value_counts().head(5)

def prepare_X(df):
    df = df.copy()
    features = base.copy()

    df['age'] = 2017 - df.year
    features.append('age')

    for v in [2, 3, 4]:
        feature = 'num_doors_%s' % v
        df[feature] = (df['number_of_doors'] == v).astype(int)
        features.append(feature)

    for v in ['chevrolet', 'ford', 'volkswagen', 'toyota', 'dodge']:
        feature = 'is_make_%s' % v
        df[feature] = (df['make'] == v).astype(int)
        features.append(feature)

    df_num = df[features]
    df_num = df_num.fillna(df_num.mean())
    X = df_num.values
    return X

X_train = prepare_X(df_train)
w_0, w = train_linear_regression(X_train, y_train)

y_pred = w_0 + X_train.dot(w)
print('train:', rmse(y_train, y_pred))

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)
print('validation:', rmse(y_val, y_pred))

data['engine_fuel_type'].value_counts().head(4)

def prepare_X(df):
    df = df.copy()
    features = base.copy()

    df['age'] = 2017 - df.year
    features.append('age')

    for v in [2, 3, 4]:
        feature = 'num_doors_%s' % v
        df[feature] = (df['number_of_doors'] == v).astype(int)
        features.append(feature)

    for v in ['chevrolet', 'ford', 'volkswagen', 'toyota', 'dodge']:
        feature = 'is_make_%s' % v
        df[feature] = (df['make'] == v).astype(int) #add to this feature new column in df
        features.append(feature)

    for v in ['regular_unleaded', 'premium_unleaded_(required)',
              'premium_unleaded_(recommended)', 'flex-fuel_(unleaded/e85)']:
        feature = 'is_type_%s' % v
        df[feature] = (df['engine_fuel_type'] == v).astype(int)
        features.append(feature)

    df_num = df[features]
    df_num = df_num.fillna(0)
    X = df_num.values
    return X

X_train = prepare_X(df_train)
w_0, w = train_linear_regression(X_train, y_train)

y_pred = w_0 + X_train.dot(w)
print('train:', rmse(y_train, y_pred))

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)
print('validation:', rmse(y_val, y_pred))

data['transmission_type'].value_counts()

data['driven_wheels'].value_counts()

data['market_category'].value_counts().head(5)

data['vehicle_size'].value_counts().head(5)

data['vehicle_style'].value_counts().head(5)

def prepare_X(df):
    df = df.copy()
    features = base.copy()

    df['age'] = 2017 - df.year
    features.append('age')

    for v in [2, 3, 4]:
        feature = 'num_doors_%s' % v
        df[feature] = (df['number_of_doors'] == v).astype(int)
        features.append(feature)

    for v in ['chevrolet', 'ford', 'volkswagen', 'toyota', 'dodge']:
        feature = 'is_make_%s' % v
        df[feature] = (df['make'] == v).astype(int)
        features.append(feature)

    for v in ['regular_unleaded', 'premium_unleaded_(required)',
              'premium_unleaded_(recommended)', 'flex-fuel_(unleaded/e85)']:
        feature = 'is_type_%s' % v
        df[feature] = (df['engine_fuel_type'] == v).astype(int)
        features.append(feature)

    for v in ['automatic', 'manual', 'automated_manual']:
        feature = 'is_transmission_%s' % v
        df[feature] = (df['transmission_type'] == v).astype(int)
        features.append(feature)

    df_num = df[features]
    df_num = df_num.fillna(df_num.mean())
    X = df_num.values
    return X

X_train = prepare_X(df_train)
w_0, w = train_linear_regression(X_train, y_train)

y_pred = w_0 + X_train.dot(w)
print('train:', rmse(y_train, y_pred))

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)
print('validation:', rmse(y_val, y_pred))

def prepare_X(df):
    df = df.copy()
    features = base.copy()

    df['age'] = 2017 - df.year
    features.append('age')

    for v in [2, 3, 4]:
        feature = 'num_doors_%s' % v
        df[feature] = (df['number_of_doors'] == v).astype(int)
        features.append(feature)

    for v in ['chevrolet', 'ford', 'volkswagen', 'toyota', 'dodge']:
        feature = 'is_make_%s' % v
        df[feature] = (df['make'] == v).astype(int)
        features.append(feature)

    for v in ['regular_unleaded', 'premium_unleaded_(required)',
              'premium_unleaded_(recommended)', 'flex-fuel_(unleaded/e85)']:
        feature = 'is_type_%s' % v
        df[feature] = (df['engine_fuel_type'] == v).astype(int)
        features.append(feature)

    for v in ['automatic', 'manual', 'automated_manual']:
        feature = 'is_transmission_%s' % v
        df[feature] = (df['transmission_type'] == v).astype(int)
        features.append(feature)

    for v in ['front_wheel_drive', 'rear_wheel_drive', 'all_wheel_drive', 'four_wheel_drive']:
        feature = 'is_driven_wheels_%s' % v
        df[feature] = (df['driven_wheels'] == v).astype(int)
        features.append(feature)

    for v in ['crossover', 'flex_fuel', 'luxury', 'luxury,performance', 'hatchback']:
        feature = 'is_mc_%s' % v
        df[feature] = (df['market_category'] == v).astype(int)
        features.append(feature)

    for v in ['compact', 'midsize', 'large']:
        feature = 'is_size_%s' % v
        df[feature] = (df['vehicle_size'] == v).astype(int)
        features.append(feature)

    for v in ['sedan', '4dr_suv', 'coupe', 'convertible', '4dr_hatchback']:
        feature = 'is_style_%s' % v
        df[feature] = (df['vehicle_style'] == v).astype(int)
        features.append(feature)

    df_num = df[features]
    df_num = df_num.fillna(df_num.mean())
    X = df_num.values
    return X

X_train = prepare_X(df_train)
w_0, w = train_linear_regression(X_train, y_train)

y_pred = w_0 + X_train.dot(w)
print('train:', rmse(y_train, y_pred))

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)
print('validation:', rmse(y_val, y_pred))

w_0         #linear combination search about singular maxtrix

w.astype(int)

#Regularization
def train_linear_regression_reg(X, y, r=0.0):
    ones = np.ones(X.shape[0])
    X = np.column_stack([ones, X])

    XTX = X.T.dot(X)
    reg = r * np.eye(XTX.shape[0])
    XTX = XTX + reg

    XTX_inv = np.linalg.inv(XTX)
    w = XTX_inv.dot(X.T).dot(y)

    return w[0], w[1:]

X_train = prepare_X(df_train)

for r in [0, 0.001, 0.01, 0.1, 1, 10]:
    w_0, w = train_linear_regression_reg(X_train, y_train, r=r)
    print('%5s, %.2f, %.2f, %.2f' % (r, w_0, w[13], w[21]))

X_train = prepare_X(df_train)
w_0, w = train_linear_regression_reg(X_train, y_train, r=0.0)

y_pred = w_0 + X_train.dot(w)
print('train', rmse(y_train, y_pred))

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)
print('val', rmse(y_val, y_pred))

X_train = prepare_X(df_train)
w_0, w = train_linear_regression_reg(X_train, y_train, r=0.01)

y_pred = w_0 + X_train.dot(w)
print('train', rmse(y_train, y_pred))

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)
print('val', rmse(y_val, y_pred))

X_train = prepare_X(df_train)
X_val = prepare_X(df_val)

for r in [0.000001, 0.0001, 0.001, 0.01, 0.1, 1, 5, 10]:
    w_0, w = train_linear_regression_reg(X_train, y_train, r=r)
    y_pred = w_0 + X_val.dot(w)
    print('%6s' %r, rmse(y_val, y_pred))

X_train = prepare_X(df_train)
w_0, w = train_linear_regression_reg(X_train, y_train, r=0.01)

X_val = prepare_X(df_val)
y_pred = w_0 + X_val.dot(w)
print('validation:', rmse(y_val, y_pred))

X_test = prepare_X(df_test)
y_pred = w_0 + X_test.dot(w)
print('test:', rmse(y_test, y_pred))

i = 2
ad = df_test.iloc[i].to_dict()
ad

X_test = prepare_X(pd.DataFrame([ad]))
y_pred = w_0 + X_test.dot(w)
suggestion = np.expm1(y_pred)
suggestion

# KNN model with 5 neighbors
knn = KNeighborsRegressor(n_neighbors=5)

# Train the KNN model
knn.fit(X_train, y_train)

# Predict prices using KNN
y_pred_knn = knn.predict(X_val)

# Calculate RMSE for KNN
rmse_knn = rmse(y_val, y_pred_knn)
print('KNN validation RMSE:', rmse_knn)
print('Linear Regression validation RMSE:', rmse(y_val, y_pred))

# Create a Decision Tree regressor
dt = DecisionTreeRegressor()

# Train the Decision Tree model
dt.fit(X_train, y_train)

# Predict prices using Decision Tree
y_pred_dt = dt.predict(X_val)

# Calculate RMSE for Decision Tree
rmse_dt = rmse(y_val, y_pred_dt)
print('Decision Tree validation RMSE:', rmse_dt)

# Create a Random Forest regressor
rf = RandomForestRegressor()

# Train the Random Forest model
rf.fit(X_train, y_train)

# Predict prices using Random Forest
y_pred_rf = rf.predict(X_val)

# Calculate RMSE for Random Forest
rmse_rf = rmse(y_val, y_pred_rf)
print('Random Forest validation RMSE:', rmse_rf)

# Create an SVM regressor
svm = SVR()

# Train the SVM model
svm.fit(X_train, y_train)

# Predict prices using SVM
y_pred_svm = svm.predict(X_val)

# Calculate RMSE for SVM
rmse_svm = rmse(y_val, y_pred_svm)
print('SVM validation RMSE:', rmse_svm)

print('Linear Regression validation RMSE:', rmse(y_val, y_pred))
print('KNN validation RMSE:', rmse(y_val, y_pred_knn))
print('Decision Tree validation RMSE:', rmse_dt)
print('Random Forest validation RMSE:', rmse_rf)
print('SVM validation RMSE:', rmse_svm)

y_pred = w_0 + X_test.dot(w)
mse = rmse(y_test, y_pred)
print('Test MSE:', mse)

# y_pred = w_0 + X_test.dot(w)
# mae = mean_absolute_error(y_test, y_pred)
# print('Test MAE:', mae)

# y_pred = w_0 + X_test.dot(w)
# r2 = r2_score(y_test, y_pred)
# print('Test R²:', r2)

# kmeans = KMeans(n_clusters=k)
# kmeans.fit(X_train)
# cluster_labels = kmeans.predict(X_val)