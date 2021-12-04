# Importamos las librerias mínimas necesarias
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error, mean_absolute_error


data = pd.read_csv("./trabajo4.csv")
df=data

ts_resort_fin = pd.read_csv("data_from_notebook/ts_resort_fin.csv",header = None, index_col = 0, squeeze = True)
test_r = pd.read_csv("data_from_notebook/test_r.csv",header = None, index_col = 0, squeeze = True)
pred_r = pd.read_csv("data_from_notebook/pred_r.csv",header = None, index_col = 0, squeeze = True)
pred_forc_r = pd.read_csv("data_from_notebook/pred_forc_r.csv",header = None, index_col = 0, squeeze = True)

ts_city_fin = pd.read_csv("data_from_notebook/ts_city_fin.csv",header = None, index_col = 0, squeeze = True)
test_c = pd.read_csv("data_from_notebook/test_c.csv",header = None, index_col = 0, squeeze = True)
pred_c = pd.read_csv("data_from_notebook/pred_c.csv",header = None, index_col = 0, squeeze = True)
pred_forc_c = pd.read_csv("data_from_notebook/pred_forc_c.csv",header = None, index_col = 0, squeeze = True)


def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
rmse_r = np.sqrt(mean_squared_error(test_r, pred_r))
mae_r = mean_absolute_error(test_r,pred_r)
mape_r = mean_absolute_percentage_error(test_r,pred_r)
rmse_c = np.sqrt(mean_squared_error(test_c, pred_c))
mae_c = mean_absolute_error(test_c,pred_c)
mape_c = mean_absolute_percentage_error(test_c,pred_c)

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

app = dash.Dash(__name__)


app.layout = html.Div(
    children= [
        html.H1(
            children = [
                "Resort and City Hotel data analysis"
            ],
            id = "title",
            style = {
                "text-align": "center",
                "text-decoration": "underline",
                "backgroundColor": "lightblue",
                "margin-bottom": "20px",
                "border-style": "outset",
                "border-color": "lightblue",
                "height": "50px"
            }
        ),

        html.H4(
            children = [
                "Desarrollo un cuadro de mando con Dash que resuma los aspectos más relevantes que hayáis extraido en el análisis exploratorio y muestre cual es la previsión de ingresos de los hoteles."
                ],
            id = "txt1",
            style ={
                "text-align": "center",
                "display": "block"
            }
        ),

        html.H2(
            children = [
                "1) Visualization part 1"
            ],
            id = "subtitle1",
            style ={
                "text-align": "left",
                "display": "block"
            }
        ),

        html.Div(
            children = [
                html.Div(
                    children = [
                        html.H3(
                            children = [
                                "Clients Origins"
                            ],
                            id = "clients_origins",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),

                        dcc.Dropdown(
                            id='dropdown1',
                            value="country",
                            options=[{'value': x, 'label': x}
                                     for x in ['country']],
                            clearable=False
                        ),
                        dcc.Graph(id="pie_chart1"),
                        html.Br(),
                        html.H4(
                            children = [
                                "The clients are mostly europeans. And this pie chart shows more than a third are portuguese. So we could say that the hotels involved here are located in Portugal."
                            ],
                            id = "txt_clients_origins",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        ),
                        html.Br(),
                        html.Br(),
                    ],
                    style = {
                        "width": "700px",
                        "height": "600px",
                        "display": "inline-block",
                    },
                ),

                html.Div( #
                    children = [
                        html.H3(
                            children = [
                                "Number of clients/reservation"
                            ],
                            id = "arrival_date_month",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown2',
                            value="adults",
                            options=[{'value': 'Clients', 'label': 'adults'}],
                            clearable=False
                        ),
                        dcc.Graph(id="pie_chart2"),
                        html.Br(),
                        html.H4(
                            children = [
                                "The hotels could mostly expect 2 clients per reservation "
                            ],
                            id = "txt_clients_per_reservation",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ],
                    style = {
                        "width": "700px",
                        "height": "600px",
                        "display": "inline-block",
                    },
                ),
            ],
        ),
        html.Div(
            children = [
                html.Div(
                    children = [
                        html.H3(
                            children = [
                                "Price Variation during the year "
                            ],
                            id = "price_variation_one_year",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown3',
                            value="arrival_date_month",
                            options=[{'label': "Arrival Month", 'value': 'arrival_date_month'}],
                            clearable=False
                        ),
                        dcc.Graph(id="line_chart"),
                        html.H4(
                            children = [
                                "For City Hotel, the income per room almost constant during the year with a slight decrease between november and march. For Resort we have a high income per room from June to August and during the others months it's very less."
                            ],
                            id = "line_chart_conclu",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        ),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                    ],
                ),

                html.Div( #
                    children = [
                        html.H3(
                            children = [
                                "Cancelation vs Other features"
                            ],
                            id = "txt_sub_bars",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown4',
                            value="hotel",
                            options=[{'label': x, 'value': x} for x in df.nunique()[df.nunique()<10].drop(["is_canceled","arrival_date_year"]).index],
                            clearable=False
                        ),
                        dcc.Graph(id="id_sub_bars"),
                        html.H4(
                            id = "sub_bars_conclu",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        )
                    ],
                ),
            ],
        ),
        html.H2(
            children = [
                "1) Visualization part 2"
            ],
            id = "subtitle2",
            style ={
                "text-align": "left",
                "display": "block"
            }
        ),
        html.Div(
            children = [
                html.Div( #
                    children = [
                        html.H3(
                            children = [
                                "Forcasting"
                            ],
                            id = "txt_forc",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown5',
                            value="Resort Hotel",
                            options=[{'label': x, 'value': x} for x in ["Resort Hotel","City Hotel"]],
                            clearable=False
                        ),
                        dcc.Graph(id="graph_forc"),
                        html.H4(
                            id="metrics",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                    ],
                ),
    ],
    style = {
        "font-family": "Arial"
    }
)])

@app.callback(
    [Output("pie_chart1", "figure"),
     Output("pie_chart2", "figure")
     ],
    [Input("dropdown1", "value"),
     Input("dropdown2", "value")])

def pie_chart(dropdown1,dropdown2):
    dff=df
    fig1 = px.pie(data_frame=dff, names=dropdown1, hole=.3,)
    fig2 = px.pie(data_frame=dff, names=dropdown2, hole=.3,)
    return fig1, fig2


@app.callback(
    Output("line_chart", "figure"),
    Input("dropdown3", "value"))

def line_chart(price_month):
    df['arr_month'] = df['arrival_date'].dt.strftime('%B')
    fig3 = go.Figure()
    if price_month == "arrival_date_month":
        dff2_r = df[df["hotel"]=="Resort Hotel"].groupby(['arrival_date_month','arr_month'])["adr","hotel"].mean()
        dff2_c = df[df["hotel"]=="City Hotel"].groupby(['arrival_date_month','arr_month'])["adr","hotel"].mean()
        dff2_r=dff2_r.reset_index(level=[0,1])
        dff2_c=dff2_c.reset_index(level=[0,1])
        fig3.add_trace(go.Scatter(x=dff2_r['arr_month'],
                                  y=dff2_r["adr"],
                                  name='Resort Hotel', marker_color='red'))
        fig3.add_trace(go.Scatter(x=dff2_c['arr_month'],
                              y=dff2_c["adr"],
                              name='City Hotel', marker_color='green'))
    return fig3


@app.callback(
    Output("id_sub_bars", "figure"),
    Input("dropdown4", "value"))

def generate_bar_chart(dropdown4):
    dff3=df
    dff3 = dff3.groupby([dropdown4,'is_canceled'])[dropdown4,"arrival_date_year"].count()
    dff3 = dff3.drop([dropdown4], axis=1)
    dff3 = dff3.reset_index([0,1])
    fig4 = px.bar(data_frame=dff3,
                  x=dff3[dropdown4],
                  y=dff3["arrival_date_year"],
                  color=dff3['is_canceled'],
                  barmode='group')
    return fig4


@app.callback(
    [Output("graph_forc", "figure"),
     Output("metrics", "children")],
    [Input("dropdown5", "value")]
)
def generate_pred_chart(dropdown5):
    data = [
        go.Scatter(
            x = ts_resort_fin.index,
            y = ts_resort_fin,
            mode = "lines",
            line = dict(color = "steelblue"),
            name = "Total revenue"),
        go.Scatter(
            x = test_r.index,
            y = pred_r,
            mode = "lines",
            line = dict(color = "firebrick", dash = "dash"),
            name = "Forecast 1"),
        go.Scatter(
            x = pred_forc_r.index,
            y = pred_forc_r,
            mode = "lines",
            line = dict(color = "darkgreen", dash = "dash"),
            name = "Forecast 2")]
    layout = go.Layout(title = "Total revenue for the Resort Hotel", xaxis_title = "Timestamp", yaxis_title = "Total revenue")
    metrics = "RMSE (Root Mean Square Error) : "+str(rmse_r)+"\n"+"MAE (Mean Absolute Error) : "+str(mae_r)+"\n"+"MAPE (Mean Percentage Error) : "+str(mape_r)

    if dropdown5 == "City Hotel":
        data = [
            go.Scatter(
                x = ts_city_fin.index,
                y = ts_city_fin,
                mode = "lines",
                line = dict(color = "steelblue"),
                name = "Total revenue"),
            go.Scatter(
                x = test_c.index,
                y = pred_c,
                mode = "lines",
                line = dict(color = "firebrick", dash = "dash"),
                name = "Forecast 1"),
            go.Scatter(
                x = pred_forc_c.index,
                y = pred_forc_c,
                mode = "lines",
                line = dict(color = "darkgreen", dash = "dash"),
                name = "Forecast 2")]
        layout = go.Layout(title = "Total revenue for the City Hotel", xaxis_title = "Timestamp", yaxis_title = "Total revenue")
        metrics = "RMSE(Root Mean Square Error):"+str(rmse_c)+" MAE(Mean Absolute Error):"+str(mae_c)+" MAPE (Mean Percentage Error):"+str(mape_c)

    fig5 = go.Figure(data = data, layout = layout)

    return fig5,metrics


app.run_server()