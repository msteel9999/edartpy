import pandas as pd
import numpy as np

class Indicators:
    
    @staticmethod
    def CalculateRSI(data, lookback):
        #For all rows and columns 0->3 take the difference with the previous row
        delta = data['Close'].diff()

        # Ignore the first row
        delta = delta[1:]
        up, down = delta.copy(), delta.copy()

        # Make the positive gains(up) and negative gains(down) series
        up[up < 0] = 0 
        down[down > 0] = 0

        # Calculate the SMA
        roll_up = up.rolling(lookback).mean()
        roll_down = down.abs().rolling(lookback).mean()

        # Remove empty values
        roll_up = roll_up[lookback:] 
        roll_down = roll_down[lookback:]

        # Calculate rsi using the SMA
        # rs = average gain/ average loss
        rs = roll_up / roll_down 
        rsi = (100.0 - (100.0 / (1.0 + rs))) 
        # rsi = np.array(rsi) 
        # rsi = np.reshape(rsi, (-1,1))
        
        #add zeros to start so that array is same length as data
        rsi = np.pad(rsi, (lookback+1, 0), 'constant')

        data['RSI']=rsi[:]

    @staticmethod
    def CalculateRSIOriginal(Data, lookback_rsi):    
        Data = pd.DataFrame(Data) 
        delta = Data.iloc[:, 3].diff()
        delta = delta[1:]

        up, down = delta.copy(), delta.copy()

        up[up < 0] = 0 
        down[down > 0] = 0

        # roll_up = pd.stats.moments.ewma (up, lookback_rsi)
        # roll_down = pd.stats.moments.ewma (down.abs(), lookback_rsi)
        roll_up = up.rolling(lookback_rsi).mean()
        roll_down = down.abs().rolling(lookback_rsi).mean()

        roll_up = roll_up[lookback_rsi:] 
        roll_down = roll_down [lookback_rsi:]
        
        Data = Data.iloc[lookback_rsi + 1:,].values 
        RS = roll_up / roll_down 
        RSI = (100.0 - (100.0 / (1.0 + RS))) 
        RSI = np.array (RSI) 
        RSI = np.reshape (RSI, (-1, 1))
        Data = np.concatenate ((Data, RSI), axis = 1)
        return Data

    @staticmethod
    # Formula for Stochastic Osc. 
    # %K=(C–L)(H–L)×100
    # C is closing price, L is lowest low and H is highest high
    def CalculateStochastic(data, lookback_stoch):
        z = np.zeros((len(data), 1), dtype = float)
        data['Stochastic'] = z[:,0] 

        for i in range (lookback_stoch, len (data)) :
            try:
                # range is i-lookback -> i+1
                # So if lookback is 14 and i is 20
                # range is 6->21
                minValue = min(data['Low'][i-lookback_stoch: i + 1])
                maxValue = max(data['High'][i-lookback_stoch: i + 1])
                data['Stochastic'][i] = (data['Close'][i] - minValue) * 100/(maxValue - minValue)
            except ValueError:
                pass  
    
    @staticmethod
    def CalculateStochasticOriginal(data, lookback_stoch):
        z = np.zeros((len(data), 1), dtype = float)
        data = np.append(data, z, axis = 1)

        for i in range (len (data)) :
            try:
                data[i, 5] = (data[i, 3] - min(data[i-lookback_stoch:i + 1, 2]))\
                    /(max (data[i-lookback_stoch:i + 1, 1]) - min(data[i-lookback_stoch:i + 1, 2]))
            except ValueError:
                pass
        data[:, 5] = data[:, 5] * 100
        return data

    @staticmethod
    def CombineIndicators(data, combinedColIndex, target1Index, target2Index):
        for i in range(len(data)):
            if data.iloc[i, target1Index] == 0 or data.iloc[i, target2Index] == 0: 
                data.iloc[i, combinedColIndex] = data.iloc[i, target1Index] + data.iloc[i, target2Index]
            else:
                data.iloc[i, combinedColIndex] = (int(data.iloc[i, target1Index]) + data.iloc[i, target2Index])/2
