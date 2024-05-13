# importing libraries
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import tkinter as tk
from tkinter import ttk
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

# Create GUI window
window = tk.Tk()
window.title("Car Price Prediction")

# reading data
data=pd.read_csv("data.csv")


# Function to show data 
def dataRead():
  print(data)

# Function to show data head
def dataInfo():
  data.info()

# Function to show data head
def dataHead():
  print(data.head())

# Function to show Dimension on data
def dataShape():
  print(data.shape)

# Function to show null values
def dataNullValues():
  print(data.isnull().sum())

# Function to show duplicated values
def dataDuplicatedValues():
  print(data.duplicated().sum())





data_read = ttk.Button(window, text="Show Data", command=dataRead)
data_read.grid(row=1, column=0,padx=(10)  ,pady=10)

data_info = ttk.Button(window, text="Data Information", command=dataInfo)
data_info.grid(row=1, column=1,padx=(0,10) , pady=10)

data_head = ttk.Button(window, text="Data Head", command=dataHead)
data_head.grid(row=1, column=2, padx=(0,10) , pady=10)

data_shape = ttk.Button(window, text="Data Shape", command=dataShape)
data_shape.grid(row=1, column=3,  padx=(0,10) ,pady=10)

data_Null_values = ttk.Button(window, text="Data Null Values", command=dataNullValues)
data_Null_values.grid(row=1, column=4,  padx=(0,10) ,pady=10)

data_Duplicated_values = ttk.Button(window, text="Data Duplicated Values", command=dataDuplicatedValues)
data_Duplicated_values.grid(row=1, column=5,  padx=(0,10) ,pady=10)

# Start GUI event loop
window.mainloop()