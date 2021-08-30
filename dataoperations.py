# Importing libraries
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.neural_network import MLPRegressor 

class DataOperations:
    @staticmethod
    def Lagger (data, lookback, dropnan = True): # Autolag Function
        # del data['Open Time']
        data = pd.DataFrame(data)
        cols = list()
        cols.append(data.shift(-(lookback + 1)))

        All = pd.concat(cols, axis=1)

        if dropnan:
            All.dropna(inplace = True)
        return All

    @staticmethod
    def LaggerOriginal (data, n_in = 1, n_out = 1, dropnan = True): # Autolag Function
        n_vars=1 if type (data) is list else data.shape[1] 
        df = pd.DataFrame (data) 
        cols, names = list(), list() 
        for i in range (n_in, 0, -1):
            cols.append(df.shift(i))
            # names += [('X%d(t-%d)' % (j+1, i)) for j in range(n_vars)]

        for i in range (0, n_out):
            cols.append(df.shift(-i))
            # if i == 0:
            #     names += [('X%d(t)' % (j+1)) for j in range (n_vars)]
            # else:
            #     names += [('X%d (t+%d)' % (j+1, i)) for j in range(n_vars)]

        All = pd.concat(cols, axis=1)
        # All.columns = names
        
        # Drop rows with NaN values
        if dropnan:
            All.dropna(inplace = True)

        return All.to_numpy()

 
    @staticmethod
    def PrepareData(data, headers):
        data = DataOperations.AddRows(data, headers)
        data['Open Time'] = pd.to_datetime(data['Open Time'], unit='ms')
        return data

    @staticmethod
    def AddRows(data, headers):
        for i in range(0, len(headers)):
            df = pd.DataFrame(data)
            df[headers[i]]=0
        return data