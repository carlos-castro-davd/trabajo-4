import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from trab import ts_resort_fin, ts_city_fin


def split_ts(ts,test_size):
    '''
    Parametros:
        ts: Serie temporal
        test_size: tamaño del test
    Resultado:
        Division en train y test
    '''

    train_size = len(ts) - test_size
    train,test = ts[:train_size], ts[train_size:]
    return train,test

train_r, test_r = split_ts(ts_resort_fin,30)
train_c, test_c = split_ts(ts_city_fin,30)

model_r = ARIMA(endog = train_r,freq = "D",order = (0,1,1), seasonal_order = (0,1,0,365))
model_rr = model_r.fit()
pred_r = model_rr.predict(start = test_r.index[0], end =test_r.index[-1])

model_c = ARIMA(endog = train_c,freq = "D",order = (0,1,1), seasonal_order = (0,1,0,365))
model_cc = model_c.fit()
pred_c = model_cc.predict(start = test_c.index[0], end =test_c.index[-1])

def mean_absolute_percentage_error(y_true, y_pred):
    '''
    Parametros:
        y_true: valores reales
        y_pred: valores predichos

    Resultado:
        Valor del MAPE del modelo
    '''
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# This is RMSE
rmse_r = np.sqrt(mean_squared_error(test_r, pred_r))
# This is MAE
mae_r = mean_absolute_error(test_r,pred_r)
# This is MAPE
mape_r = mean_absolute_percentage_error(test_r,pred_r)

# This is RMSE
rmse_c = np.sqrt(mean_squared_error(test_c, pred_c))
# This is MAE
mae_c = mean_absolute_error(test_c,pred_c)
# This is MAPE
mape_c = mean_absolute_percentage_error(test_c,pred_c)

start = datetime.strptime('01Sep2017', '%d%b%Y')
end = datetime.strptime('30Sep2017', '%d%b%Y')

model_forc_r = ARIMA(endog = ts_resort_fin,freq = "D",order = (0,1,1), seasonal_order = (0,1,0,365))
model_forc_rr = model_forc_r.fit()
pred_forc_r = model_forc_rr.predict(start = start, end =end)

model_forc_c = ARIMA(endog = ts_city_fin,freq = "D",order = (0,1,1), seasonal_order = (0,1,0,365))
model_forc_cc = model_forc_c.fit()
pred_forc_c = model_forc_cc.predict(start = start, end =end)