from sklearn.neural_network import MLPRegressor
import numpy as np
import pandas as pd

class Splitter:

    @staticmethod
    def Predictor(data, projection):
        data = pd.DataFrame(data)
        Determinant = len(data.columns) 		
        
        #Translate projection, 30% 0.3, to a value eg. 200 data points => projection = 60
        projection = int(len(data.index) * projection)
        
        X = data.iloc[:, 1: Determinant-1].values
        Y = data.iloc[:, -1].values
        Y = np.reshape(Y, (-1, 1))

        #splitting the dataset into the Training set and Test set
        X_train = X[:-projection, ]

        Y_train = Y[:-projection, ]

        X_test = X[-projection:,]

        Y_test = Y[-projection:,]

        # Fitting the model
        regressor = MLPRegressor(hidden_layer_sizes = (1,), activation = 'relu', \
             solver = 'adam', batch_size = 'auto', verbose = False, max_iter = 10000, \
                  early_stopping = False, random_state = 0)

        regressor.fit(X_train, Y_train.ravel())

        # Predicting the Test set results
        prediction = regressor.predict(X_test)

        data['Prediction'] = \
            np.pad(prediction, (0, len(data) - len(prediction)), 'constant').tolist()
        return data