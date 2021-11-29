# Importamos las librerias mínimas necesarias
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import logging
from plotly.subplots import make_subplots


df = pd.read_csv("./trabajo4.csv")


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
                        html.H4(
                            children = [
                                "The clients are mostly europeans. And this pie chart shows more than a third are portuguese. So we could say that the hotels involved here are located in Portugal."
                            ],
                            id = "txt_clients_origins",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        )
                    ],
                    style = {
                        "width": "700px",
                        "height": "600px",
                        "display": "inline-block",
                        "border-style": "ridge",
                        "border-color": "black"
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
                        html.H4(
                            children = [
                                "The clients are mostly europeans. And this pie chart shows more than a third are portuguese. So we could say that the hotels involved here are located in Portugal."
                            ],
                            id = "txt_clients_per_reservation",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        )
                    ],
                    style = {
                        "width": "700px",
                        "height": "600px",
                        "display": "inline-block",
                        "border-style": "ridge",
                        "border-color": "black"
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
                                "Clients per Reservation"
                            ],
                            id = "clients_per_reservation",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown3',
                            value="hotel",
                            options=[{'value': x, 'label': x}
                                     for x in ['hotel']],
                            clearable=False
                        ),
                        dcc.Graph(id="pie_chart3"),
                        html.H4(
                            children = [
                                "x1"
                            ],
                            id = "x1",
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
                                "Price"
                            ],
                            id = "price_revevenues",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Dropdown(
                            id='dropdown4',
                            value="adr",
                            options=[{'value': x, 'label': x}
                                     for x in ['adr']],
                            clearable=False
                        ),
                        dcc.Graph(id="pie_chart4"),
                        html.H4(
                            children = [
                                "x2"
                            ],
                            id = "x2",
                            style ={
                                "text-align": "center",
                                "display": "block"
                            }

                        )
                    ],
                ),
            ],
        ),
    ],
    style = {
        "font-family": "Arial"
    }
)

@app.callback(

    [Output("pie_chart1", "figure"),
     Output("pie_chart2", "figure"),
     Output("pie_chart3", "figure"),
     Output("pie_chart4", "figure")],

    [Input("dropdown1", "value"),
     Input("dropdown2", "value"),
     Input("dropdown1", "value"),
     Input("dropdown2", "value")]
)

def pie_chart(dropdown1,dropdown2,dropdown3,dropdown4):
    dff=df
    df_per = df.groupby(['hotel', ])["adults", "children", "babies"].count()
    fig1 = px.pie(data_frame=dff, names=dropdown1, hole=.3,)
    fig2 = px.pie(data_frame=dff, names=dropdown2, hole=.3,)
    fig3 = px.pie(data_frame=df_per, names=dropdown3, hole=.3,)
    fig4 = px.pie(data_frame=dff, names=dropdown4, hole=.3,)

    return fig1, fig2, fig3, fig4


app.run_server()