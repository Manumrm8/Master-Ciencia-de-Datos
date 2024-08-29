import dash
from dash import Dash, dcc, html, Input, Output, callback, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html

import pandas as pd


dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.Div([html.P("Por favor, realice la carga del fichero")],id= "contenedor1")
    ]
)

@callback(Output("contenedor1","children"),
          [Input("store", "data")],
          suppress_callback_exceptions=True)


def gen_datos(datos):
    if datos is not None and len(datos) > 0:
        df = pd.DataFrame(datos["datos"])
        if df.columns[0] == "PACIENTES" and df.columns[-1] == "AV":
            contenido = generaDivGraficas(df)
            return contenido
    elif datos is None:
        return html.Div([
            html.P("Inserte el archivo que contiene datos sobre Arritmias",
                   style={'font-size': '20px', 'font-weight': 'bold', 'color': 'blue', 'text-align': 'center'})
        ])

    return html.Div([
        html.P("El archivo proporcionado no es adecuado para el análisis de Proarritmidad.",
               style={'font-size': '20px', 'font-weight': 'bold', 'color': 'red', 'text-align': 'center'}),
        html.P("Por favor, verifique que el contenido es correcto. Debe comenzar con el ID del paciente y terminar con AV.",
               style={'font-size': '18px', 'font-weight': 'bold', 'color': 'red', 'text-align': 'center'})
    ])


def generaDivGraficas(df):
    columnas = df.columns[1:-1]
    hover = df.columns.to_list()[0]

    fig_scatter = px.scatter(df, x=columnas[0], y=columnas[1], hover_name=hover)
    fig_scatter.update_traces(marker=dict(size=10, opacity=0.8))
    fig_scatter.update_layout(
        title="Gráfico de dispersión",
        xaxis_title=columnas[0],
        yaxis_title=columnas[1],
        font=dict(family="Arial", size=14, color="black"),
        plot_bgcolor="paleturquoise",
        paper_bgcolor="paleturquoise",
    )

    fig_default_hover = px.scatter()
    fig_default_hover.update_layout(
        annotations=[
            dict(
                x=0.5, y=0.5,
                xref="paper", yref="paper", text="Coloca el ratón sobre los datos", showarrow=False,
                font=dict(family="Arial", size=14, color="black"))
        ],
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        plot_bgcolor="paleturquoise",
        paper_bgcolor="paleturquoise",
    )

    opciones_lin = [{"label": "Lineal", "value": "Linear"}, {"label": "Logarítmica", "value": "Log"}]

    res = [
        dbc.Row([
            dbc.Col([
                html.P("Seleccione la variable para el eje x", className="text-center"),
                dcc.Dropdown(id="columna1", options=[{"label": col, "value": col} for col in columnas],
                             value=columnas[0],
                             style={'padding-left': '20px'}),
                dcc.RadioItems(options=opciones_lin, value=opciones_lin[0]["value"], id="escala1", inline=True,
                               labelStyle={'padding-right': '20px', 'padding-top': '20px', 'padding-left': '20px'})
            ], width=6),
            dbc.Col([
                html.P("Seleccione la variable para el eje y", className="text-center"),
                dcc.Dropdown(id="columna2", options=[{"label": col, "value": col} for col in columnas],
                             value=columnas[1]),
                dcc.RadioItems(options=opciones_lin, value=opciones_lin[0]["value"], id="escala2", inline=True,
                               labelStyle={'padding-right': '20px', 'padding-top': '20px'})
            ], width=6),
        ]),

        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id="scatter_plt", figure=fig_scatter)
                ], style={'height': '600px', 'padding-top': '85px'}),
            ], width=6),
            dbc.Col([
                dcc.Graph(id="line_plot1", figure=fig_default_hover, style={'width': '90%', 'height': '400px'}),
                dcc.Graph(id="line_plot2", figure=fig_default_hover, style={'width': '90%', 'height': '400px'})
            ], width=6)
        ])
    ]
    return res

@callback(Output('columna1', 'options'),Input("store", "data"),suppress_callback_exceptions=True)
def actualizaColumnas(datos):
    if(len(datos)>0):
        df = pd.DataFrame(datos["datos"])
        col = df.columns.to_list()[1:-1]
        return col
    
@callback(Output('columna2', 'options'),Input("store", "data"),suppress_callback_exceptions=True)
def actualizaColumnas2(datos):
    if(len(datos)>0):
        df = pd.DataFrame(datos["datos"])
        col = df.columns.to_list()[1:]
        return col
    
@callback(Output("scatter_plt", "figure"),
           [Input("store", "data"),
            Input('columna1', 'value'),
            Input('columna2', 'value'),
            Input("escala1", "value"),
            Input("escala2", "value")],
            suppress_callback_exceptions=True)
def createScatter(datos,col1,col2,scale1,scale2):

    df = pd.DataFrame(datos["datos"])
    fig = px.scatter(df, x=col1, y=col2, title='Diagrama de dispersión',
                      hover_name=df.columns.to_list()[0])
    fig.update_xaxes(title=col1)
    fig.update_yaxes(title=col2)
    fig.update_layout(
                            plot_bgcolor="paleturquoise",
                            paper_bgcolor="paleturquoise",
                        )
    if(scale1=="Log"):
        fig.update_xaxes(type='log',title=col1)
    if(scale2=="Log"):
        fig.update_yaxes(type='log',title=col2)
    return fig


@callback(Output("line_plot1", "figure"),
          [Input('scatter_plt', 'hoverData')],
          [State("store", "data"),
           State('columna1', 'value')],
           suppress_callback_exceptions=True)
def displayLine1(hoverData, datos, col):
    if hoverData is not None:
        data = pd.DataFrame(datos["datos"])
        data["highlight"] = False
        point_index = hoverData['points'][0]['pointIndex']
        print("El dato es tal que ",  hoverData['points'][0])

        data.iloc[[point_index],[-1]] = True

        fig = px.histogram(data, x=col, color='highlight', 
                       color_discrete_map={False: 'blue', True: 'red'}, 
                       title='Histograma de la variable '+col)
        fig.update_traces(showlegend=False)
        fig.update_layout(
                            plot_bgcolor="paleturquoise",
                            paper_bgcolor="paleturquoise",
                        )


        return fig

    else:
        fig_default_hover = px.scatter()
        fig_default_hover.update_layout(
            annotations=[
                dict(x=0.5,y=0.5,xref="paper",yref="paper",
                    text="Selecciona un dato",showarrow=False,
                    font=dict(family="Arial",size=18,color="black"))])
        fig_default_hover.update_xaxes(showgrid=False, zeroline=False, visible=False)
        fig_default_hover.update_yaxes(showgrid=False, zeroline=False, visible=False)
        fig_default_hover.update_layout(
                            plot_bgcolor="paleturquoise",
                            paper_bgcolor="paleturquoise",
                        )
        return fig_default_hover
    
@callback(Output("line_plot2", "figure"),
          [Input('scatter_plt', 'hoverData')],
          [State("store", "data"),
           State('columna2', 'value')],
           suppress_callback_exceptions=True)
def displayLine2(hoverData, datos, col):
    if hoverData is not None:
        data = pd.DataFrame(datos["datos"])
        data["highlight"] = False
        point_index = hoverData['points'][0]['pointIndex']
        print("El dato es tal que ",  hoverData['points'][0])
        data.iloc[[point_index],[-1]] = True

        fig = px.histogram(data, x=col, color='highlight', 
                       color_discrete_map={False: 'blue', True: 'red'}, 
                       title='Histograma de la variable '+col)
        fig.update_traces(showlegend=False)
        fig.update_layout(
                            plot_bgcolor="paleturquoise",
                            paper_bgcolor="paleturquoise",
                        )

        return fig

    else:
        fig_default_hover = px.scatter()
        fig_default_hover.update_layout(
            annotations=[
                dict(x=0.5,y=0.5,xref="paper",yref="paper",
                    text="Selecciona un dato",showarrow=False,
                    font=dict(family="Arial",size=18,color="black"))])
        fig_default_hover.update_xaxes(showgrid=False, zeroline=False, visible=False)
        fig_default_hover.update_yaxes(showgrid=False, zeroline=False, visible=False)
        fig_default_hover.update_layout(
                            plot_bgcolor="paleturquoise",
                            paper_bgcolor="paleturquoise",
                        )
        return fig_default_hover


