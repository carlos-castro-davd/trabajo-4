# Importamos las librerias mínimas necesarias
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from trab import ts_resort_fin, ts_city_fin
from trab2 import test_r, test_c, pred_r, pred_c, pred_forc_r, pred_forc_c


data = pd.read_csv("./trabajo4.csv")
df=data

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
                "Una empresa hotelera gestiona dos hoteles diferentes y ha almacenado información de las reservas realizadas en ambos hoteles durante varios años. Su idea es realizar nuevas campañas publicitarias que puedan atraer a clientes en temporadas bajas y altas entre otras posibles medidas estratégicas."
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
                                "Clients per reservations"
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
                            options=[{'value': x, 'label': x}
                                     for x in ['adults']],
                            clearable=False
                        ),
                        dcc.Graph(id="pie_chart2"),
                        html.Br(),
                        html.H4(
                            children = [
                                "The clients are mostly europeans. And this pie chart shows more than a third are portuguese. So we could say that the hotels involved here are located in Portugal."
                            ],
                            id = "txt_clients_per_reservation",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        ),
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
                                "x1ffkldfnlnl dfnf fdnldn fgldfgnld fdngldn dfnlnd ngdlnfg"
                            ],
                            id = "line_chart_conclu",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        )
                    ],
                ),

                html.Div( #
                    children = [
                        html.H3(
                            children = [
                                "Cancellation impact on ohters variables"
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
                                "Hotel revenues as time serie"
                            ],
                            id = "txt_time_serie",
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
                        dcc.Graph(id="graph_time_serie"),
                    ],
                ),
                html.Div( #
                    children = [
                        html.H3(
                            children = [
                                "Prediction"
                            ],
                            id = "txt_pred",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown6',
                            value="Resort Hotel",
                            options=[{'label': x, 'value': x} for x in ["Resort Hotel","City Hotel"]],
                            clearable=False
                        ),
                        dcc.Graph(id="graph_pred"),
                    ],
                ),
                html.Div( #
                    children = [
                        html.H3(
                            children = [
                                "Forcasting"
                            ],
                            id = "txt_forcast",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown7',
                            value="Resort Hotel",
                            options=[{'label': x, 'value': x} for x in ["Resort Hotel","City Hotel"]],
                            clearable=False
                        ),
                        dcc.Graph(id="graph_forcast")
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
    Output("graph_time_serie", "figure"),
    Input("dropdown5", "value"))

def generate_ts_chart(dropdown5):
    data = [
        go.Scatter(
            x = ts_resort_fin.index,
            y = ts_resort_fin,
            mode = "lines",
            line = dict(color = "steelblue"),
            name = "Total revenue")]
    layout = go.Layout(title = "Total revenue for the Resort Hotel", xaxis_title = "Timestamp", yaxis_title = "Total revenue")

    if dropdown5 == "City Hotel":
        data = [
            go.Scatter(
                x = ts_city_fin.index,
                y = ts_city_fin,
                mode = "lines",
                line = dict(color = "steelblue"),
                name = "Total revenue")]
        layout = go.Layout(title = "Total revenue for the City Hotel", xaxis_title = "Timestamp", yaxis_title = "Total revenue")

    fig5 = go.Figure(data = data, layout = layout)
    return fig5


@app.callback(
    Output("graph_pred", "figure"),
    Input("dropdown6", "value"))

def generate_pred_chart(dropdown6):
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
            name = "Forecast")]
    layout = go.Layout(title = "Total revenue for the Resort Hotel", xaxis_title = "Timestamp", yaxis_title = "Total revenue")

    if dropdown6 == "City Hotel":
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
                name = "Forecast")]
        layout = go.Layout(title = "Total revenue for the City Hotel", xaxis_title = "Timestamp", yaxis_title = "Total revenue")

    fig6 = go.Figure(data = data, layout = layout)

    return fig6

@app.callback(
    Output("graph_forcast", "figure"),
    Input("dropdown7", "value"))

def generate_forcast_chart(dropdown7):
    data = [
        go.Scatter(
            x = ts_resort_fin.index,
            y = ts_resort_fin,
            mode = "lines",
            line = dict(color = "steelblue"),
            name = "Total revenue"),
        go.Scatter(
            x = pred_forc_r.index,
            y = pred_forc_r,
            mode = "lines",
            line = dict(color = "firebrick", dash = "dash"),
            name = "Forecast")]
    layout = go.Layout(title = "Total revenue forecasted for the Resort Hotel", xaxis_title = "Timestamp", yaxis_title = "Total revenue")

    if dropdown7 == "City Hotel":
        data = [
            go.Scatter(
                x = ts_city_fin.index,
                y = ts_city_fin,
                mode = "lines",
                line = dict(color = "steelblue"),
                name = "Total revenue"),
            go.Scatter(
                x = pred_forc_c.index,
                y = pred_forc_c,
                mode = "lines",
                line = dict(color = "firebrick", dash = "dash"),
                name = "Forecast")]
        layout = go.Layout(title = "Total revenue forecasted for the City Hotel", xaxis_title = "Timestamp", yaxis_title = "Total revenue")

    fig7 = go.Figure(data = data, layout = layout)

    return fig7

app.run_server()