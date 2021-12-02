import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly.subplots import make_subplots
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

def descomposicion_ts(ts,modelo,period):
    '''
    Parametros:
        Serie temporal asociada
        modelo: Si la serie es aditiva o multiplicativa
        period: frecuencia estimada del modelo
    Resultado:
        Representación gráfica de la descomposición de la serie temporal
    '''

    descomposicion = seasonal_decompose(ts, model = modelo, period = period)
    aux = pd.DataFrame({"tendencia" : descomposicion.trend, "estacionalidad" : descomposicion.seasonal, "residuo" : descomposicion.resid})

    fig = make_subplots(rows = 3, cols = 1, )

    fig.add_trace(
        go.Scatter(
            x = aux.index,
            y = aux["tendencia"],
            name = "Trend",
            mode = "lines",
            line = dict(color = "mediumseagreen")
        ),
        row = 1,
        col = 1
    )

    fig.add_trace(
        go.Scatter(
            x = aux.index,
            y = aux["estacionalidad"],
            name = "Seasonality",
            mode = "lines",
            line = dict(color = "darkorange")
        ),
        row = 2,
        col = 1
    )

    fig.add_trace(
        go.Scatter(
            x = aux.index,
            y = aux["residuo"],
            name = "Residuals",
            mode = "lines",
            line = dict(color = "grey")
        ),
        row = 3,
        col = 1
    )

    # Update xaxis properties
    fig.update_xaxes(title_text="Fecha", row=1, col=1)
    fig.update_xaxes(title_text="Fecha", row=2, col=1)
    fig.update_xaxes(title_text="Fecha", row=3, col=1)


    # Update yaxis properties
    fig.update_yaxes(title_text="Trend", row=1, col=1)
    fig.update_yaxes(title_text="Seasonality", row=2, col=1)
    fig.update_yaxes(title_text="Residuals", row=3, col=1)

    fig.update_layout(height=1200, title_text="Descomposicion de la serie temporal")
    fig.show()

model_r = ARIMA(endog = train_r,freq = "D",order = (0,1,1), seasonal_order = (0,1,0,365))
model_r = model_r.fit()
pred_r = model_r.predict(start = test_r.index[0], end =test_r.index[-1])

model_c = ARIMA(endog = train_c,freq = "D",order = (0,1,1), seasonal_order = (0,1,0,365))
model_c = model_c.fit()
pred_c = model_c.predict(start = test_c.index[0], end =test_c.index[-1])

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
model_forc_r = model_forc_r.fit()
pred_forc_r = model_forc_r.predict(start = start, end =end)

model_forc_c = ARIMA(endog = ts_city_fin,freq = "D",order = (0,1,1), seasonal_order = (0,1,0,365))
model_forc_c = model_forc_c.fit()
pred_forc_c = model_forc_c.predict(start = start, end =end)