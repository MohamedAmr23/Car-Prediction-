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
window.title("Visualization")


# reading data
data=pd.read_csv("data.csv")

#cleaning data =editing in dataset
data.columns=data.columns.str.lower().str.replace(' ','_')

stringColumns=list(data.dtypes[data.dtypes=='object'].index)

for col in stringColumns:
  data[col]=data[col].str.lower().str.replace(' ','_')


#change column name msrp to price
data.rename(columns = {'msrp': 'price'}, inplace = True)  
#analysis of data
def his():
    plt.figure(figsize=(7, 4))
    sns.histplot(data.price[data.price < 80000], bins=40)
    plt.ylabel('Frequency')
    plt.xlabel('Price')
    plt.title('Distribution of prices')
    plt.show()

def line():
   # Example line plot
    plt.figure(figsize=(8, 6))
    sns.lineplot(data.price[data.price < 80000])
    plt.title('Line Plot')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.show()

def scatter():
  # Example scatter plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data.price[data.price > 80000])
    plt.title('Scatter Plot')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.show()

def bar():
    plt.figure(figsize=(8, 6))
    sns.barplot(data.engine_hp[data.engine_hp > 800])
    plt.title('Bar Plot')
    plt.xlabel('engine_hp')
    plt.ylabel('Frequency')
    plt.show()

def pie():
    plt.figure(figsize=(8, 6))
    plt.pie(data['make'].value_counts(), labels=data['make'].unique(), autopct='%1.1f%%', startangle=140)
    plt.title('Pie Chart')
    plt.show()

histplot = ttk.Button(window, text="Histplot", command=his)
histplot.grid(row=1, column=0,padx=(10)  ,pady=10)

lineplot = ttk.Button(window, text="Lineplot", command=line)
lineplot.grid(row=1, column=1,padx=(0,10) , pady=10)

scatterplot = ttk.Button(window, text="Scatterplot", command=scatter)
scatterplot.grid(row=1, column=2, padx=(0,10) , pady=10)

barplot = ttk.Button(window, text="Barplot", command=bar)
barplot.grid(row=1, column=3,  padx=(0,10) ,pady=10)

piee = ttk.Button(window, text="Pie", command=pie)
piee.grid(row=1, column=4,  padx=(0,10) ,pady=10)


# Start GUI event loop
window.mainloop()