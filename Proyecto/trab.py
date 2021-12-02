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


path = "trabajo4.csv"
df = pd.read_csv(path)

df = df.drop(df[df['adr'] == 5400.0].index)

df['arrival_date_month'].loc[(df['arrival_date_month'] == "January")] = 1
df['arrival_date_month'].loc[(df['arrival_date_month'] == "February")] = 2
df['arrival_date_month'].loc[(df['arrival_date_month'] == "March")] = 3
df['arrival_date_month'].loc[(df['arrival_date_month'] == "April")] = 4
df['arrival_date_month'].loc[(df['arrival_date_month'] == "May")] = 5
df['arrival_date_month'].loc[(df['arrival_date_month'] == "June")] = 6
df['arrival_date_month'].loc[(df['arrival_date_month'] == "July")] = 7
df['arrival_date_month'].loc[(df['arrival_date_month'] == "August")] = 8
df['arrival_date_month'].loc[(df['arrival_date_month'] == "September")] = 9
df['arrival_date_month'].loc[(df['arrival_date_month'] == "October")] = 10
df['arrival_date_month'].loc[(df['arrival_date_month'] == "November")] = 11
df['arrival_date_month'].loc[(df['arrival_date_month'] == "December")] = 12
arrival_date = pd.to_datetime(df.arrival_date_year*10000+df.arrival_date_month*100+df.arrival_date_day_of_month,format='%Y%m%d')
df["arrival_date"] = arrival_date

df = df.drop(["arrival_date_year","arrival_date_month","arrival_date_week_number","arrival_date_day_of_month","is_repeated_guest","previous_cancellations","previous_bookings_not_canceled","booking_changes","agent","company","days_in_waiting_list","required_car_parking_spaces","total_of_special_requests","lead_time","meal","country","market_segment","distribution_channel","reserved_room_type","assigned_room_type","deposit_type","customer_type","reservation_status_date"],1)

df["room_occupied"] = 1

def agrupacion_diaria(df,col,hotel):
    """
    Esta funcion la utilizaremos para crear la serie temporal que toma el beneficio diario basado en ADR

    Parametros:
        df: pd.DataFrame
            Dataframe que contiene los datos de los hoteles
        col: str
            Nombre de la columna que va a ser agrupada
        hotel:
            Nombre del hotel que se decide hacer la agrupación para estudiar sus beneficios

    Resultado:
        grouped: pd.DataFrame
            Serie temporal que agrupa la columna anterior

    """
    # Paso 0: Estructura general a la que iremos añadiendo los valores
    df_hotel = df[df["hotel"] == hotel]


    # Si estamos midiendo el ADR quitamos los que no reportan beneficio
    if col == "adr":
        df_hotel = df_hotel[df_hotel["adr"] != 0]

    # Numero de noches que han reservado e intervalo entre inicio y final de estancia

    df_hotel["total_nights"] = df_hotel["stays_in_weekend_nights"] + df_hotel["stays_in_week_nights"]

    print("Estableciendo el intervalo de las noches que han pasado los clientes del hotel {}".format(hotel))
    df_hotel["check_out_day"] = df_hotel.apply(lambda row: row["arrival_date"] + timedelta(days = row["total_nights"]), axis = 1)

    # Seleccionamos la primera fecha de entrada y la última fecha de salida
    min_date = df_hotel["arrival_date"].min()
    max_date = df_hotel["check_out_day"].max() - timedelta(days = 1)
    full_range = pd.date_range(min_date, max_date, freq = "D")

    # Creamos una estructura a detalle diario que vaya desde la fecha mínima a la fecha máxima
    grouped = pd.DataFrame()

    grouped["date"] = full_range

    # Creamos una columna auxiliar llena de ceros a la que iremos sumando la agrupacion por columna
    grouped[col] = 0

    # Paso 1: caso general, los clientes se hospedan con normalidad (reservation_status == "Check-Out")

    check_out = df_hotel[df_hotel["reservation_status"] == "Check-Out"]
    check_out = check_out[["arrival_date","total_nights",col, "check_out_day"]]


    # Calculamos el beneficio en cada una de las noches del hotel basandonos en el ADR
    print("Agrupando los resultados por noche de la variable {} para los clientes que realizaron Check-Out en el {}".format(col,hotel))
    for date in full_range:
        date_df = check_out[(check_out["arrival_date"] <= date) & (check_out["check_out_day"] > date)]
        suma = date_df[col].sum()
        grouped.loc[grouped["date"] == date, col] = suma
        del date_df
    print("Agrupacion completada de la variable {} para clientes que realizaron Check-Out en el {}".format(col,hotel))
    print(" ")

    del check_out

    # En caso de que estuvieramos estudiando el adr podemos añadir los beneficios por cancelaciones o no apariciones

    if col == "adr":
        # Paso 2: cancelaciones, el beneficio que generen los clientes que cancelan su reserva se aplicarán
        # a los teóricos días de estancia, como en el caso anterior
        grouped[col + "_canceled"] = 0
        print("Agrupando los resultados por noche de la variable {} para aquellos clientes que cancelaron su reserva en el {}".format(col,hotel))
        cancel = df_hotel[df_hotel["reservation_status"] == "Canceled"]
        cancel = cancel[["arrival_date","total_nights",col, "check_out_day"]]

        for date in full_range:
            date_df = cancel[(cancel["arrival_date"] <= date) & (cancel["check_out_day"] > date)]
            suma = date_df[col].sum()
            grouped.loc[grouped["date"] == date, col + "_canceled"] += suma
            del date_df
        print("Agrupacion completada de la variable {} para clientes que cancelaron su reserva en el {}".format(col, hotel))
        print(" ")

        # Paso 3: el cliente no aparece el dia reservado, el beneficio generado por estos clientes se aplica al dia de entrada
        grouped[col + "_noshow"] = 0
        print("Agrupando los resultados por noche de la variable {} para aquellos clientes que no acudieron a su reserva en el {}".format(col, hotel))
        no_show = df_hotel[df_hotel["reservation_status"] == "No-Show"]
        no_show = no_show[["arrival_date","total_nights",col, "check_out_day"]]

        for date in full_range:
            date_df = no_show[(no_show["arrival_date"] <= date) & (no_show["check_out_day"] > date)]
            suma = date_df[col].sum()
            grouped.loc[grouped["date"] == date, col + "_noshow"] += suma
            del date_df
        print("Agrupacion completada de la variable {} para clientes que no acudieron a su reserva en el {}".format(col, hotel))
        print(" ")

    grouped.set_index("date",inplace = True)
    return grouped

df_city = agrupacion_diaria(df, "adr", "City Hotel")

df_resort = agrupacion_diaria(df, "adr", "Resort Hotel")


ts_resort = pd.DataFrame()
cols = ["adr", "rooms_occupied", "adults","children","babies"]
df["rooms_occupied"] = 1
for col in cols:
    aux = agrupacion_diaria(df,col,"Resort Hotel")
    if ts_resort.empty:
        ts_resort = aux
    else:
        ts_resort = pd.merge(ts_resort, aux, how = "left", left_index = True, right_index = True)
df.drop("rooms_occupied", axis = 1, inplace = True)


ts_city = pd.DataFrame()
cols = ["adr", "rooms_occupied", "adults","children","babies"]
df["rooms_occupied"] = 1
for col in cols:
    aux = agrupacion_diaria(df,col,"City Hotel")
    if ts_city.empty:
        ts_city = aux
    else:
        ts_city = pd.merge(ts_city, aux, how = "left", left_index = True, right_index = True)
df.drop("rooms_occupied", axis = 1, inplace = True)

ts_resort_fin = ts_resort["adr"].copy() + ts_resort["adr_canceled"].copy() + ts_resort["adr_noshow"].copy()
ts_city_fin = ts_city["adr"].copy() + ts_city["adr_canceled"].copy() + ts_city["adr_noshow"].copy()

ts_resort_fin = ts_resort_fin[(ts_resort_fin.index >= datetime(2015,7,15)) & (ts_resort_fin.index <= datetime(2017,8,31))]
ts_city_fin = ts_city_fin[(ts_city_fin.index >= datetime(2015,7,15)) & (ts_city_fin.index <= datetime(2017,8,31))]
