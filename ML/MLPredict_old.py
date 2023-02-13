import calendar
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
import currency_converter as cc
#load the model from a file

class MLPredict_old:
    def __init__(self):
        pass

    def get_input_and_predict(self, wind, temp, month, hour):#, predict_var = 0):
        filename = 'ML/finalized_model.sav'

        vindhastighet = float(wind)
        lufttemperatur = float(temp)
        month_in  = int(month)
        timeofday = int(hour)
        
        print(vindhastighet)
        print(lufttemperatur)
        print(month_in)
        print(timeofday)

        loaded_model = pickle.load(open(filename, 'rb'))

        #put the input into a dataframe
        df = pd.DataFrame(
            {'Vindhastighet AVG': [vindhastighet],
            'Lufttemperatur AVG': [lufttemperatur],
            'Month':      [month_in],
            'TimeOfDay': [timeofday]}
        )

        #scale the data
        X = df[['Vindhastighet AVG', 'Lufttemperatur AVG', 'Month', 'TimeOfDay']]
        scaler = StandardScaler()
        scaler.fit(X).transform(X)

        #make a prediction
        y_pred = loaded_model.predict(X)

        #convert from EUR per Mwh to SEK per Kwh
        c = cc.CurrencyConverter()
        y_pred = y_pred / 1000
        y_pred = y_pred * c.convert(1, 'EUR', 'SEK')

        return str(y_pred.round(2)[0])