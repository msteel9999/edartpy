import numpy as np
import pandas as pd
from indicators.indicators import Indicators
from splitter import Splitter
from dataoperations import DataOperations

projection = 0.3
indicator1 = "RSI"
indicator2 = "Stochastic"

#import data from csv - note we need OHLC structure ie
#column 1 - open, column 2 - high, column 3 - low, column 4 - close
data = pd.Cov = pd.read_csv("C:/Uploader/GBP_USD_No_Header.csv", sep=',', header=None, names=["Open", "High", "Low", "Close"], usecols=[1,2,3,4])
# data = DataOperations.PrepareData(data, [indicator1, indicator2, "Predicted"])

# Indicators.CalculateRSI(data, 14)
# Indicators.CalculateStochastic(data, 14) 
data = Indicators.CalculateRSIOriginal(data, 14)
data = Indicators.CalculateStochasticOriginal(data, 14) 
# Indicators.CombineIndicators(data, 7, 5, 6)
# data = DataOperations.Lagger(data, 14)
data = DataOperations.Lagger(data, 14)
# data.to_excel("C:/Output/MLP_AutoLag.xlsx")

data = Splitter.Predictor(data, projection)
# pd.DataFrame(data).to_excel("C:/Output/MLP_Prediction.xlsx")
np.savetxt("C:/Output/MLP_Prediction.csv", data, delimiter=",")