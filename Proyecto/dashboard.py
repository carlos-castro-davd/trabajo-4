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

        html.H6(
            children = [
                "TUna empresa hotelera gestiona dos hoteles diferentes y ha almacenado información de las reservas realizadas en ambos hoteles durante varios años. Su idea es realizar nuevas campañas publicitarias que puedan atraer a clientes en temporadas bajas y altas entre otras posibles medidas estratégicas."
            ],
            id = "txt1",
            style ={
                "text-align": "left",
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
                            value=df['hotel'].unique()[0],
                            options=[{'value': x, 'label': x}
                                     for x in df['hotel'].unique()],
                            clearable=False
                        )
                    ],
                ),

                html.Div( #
                    children = [
                        html.H3(
                            children = [
                                "Arrival Date (Month)"
                            ],
                            id = "arrival_date_month",
                            style = {
                                "display": "block",
                                "text-align": "center"
                            }
                        ),
                        dcc.Graph(id="plot_arrival_date_month")
                    ]
                )
            ]
        ),
    ],
    style = {
        "font-family": "Arial"
    }
)

@app.callback(
    Output("pie_chart", "figure"),
    Input("dropdown1", "value"))

def pie_chart(dropdown1):

    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels = df[df["country"]==dropdown1].unique(), values = df[df["country"]==dropdown1].value_counts(normalize=True)
        )
    )
    return fig


app.run_server()