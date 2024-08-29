import dash
from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from sklearn.manifold import TSNE, Isomap, MDS
from sklearn.decomposition import PCA
from umap import UMAP

from sklearn.preprocessing import StandardScaler

dash.register_page(__name__,path= "/embedding")


layout = html.Div([
    dbc.Row([
        dbc.Col([html.P()],width=1),
        dbc.Col([html.P("Seleccione el método para generar el embedding (UMAP puede que tarde un rato)", className="text-center"),
            dcc.RadioItems(
                options=[
                    {"label": "PCA   ", "value": "pca"},
                    {"label": "ISOMap   ", "value": "isomap"},
                    {"label": "tsNE   ", "value": "tsne"},
                    {"label": "UMAP   ", "value": "umap"},
                    {"label": "MDS  ", "value": "mds"}
                ],
                value="pca",
                id="method_embedding",
                className="text-center",
                inline=True,
                labelStyle={'padding-right': '20px'}
            )],width=11)]),
            
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="plot_pca")
                ], width=6),
        dbc.Col([
            dcc.Graph(id="plot_pca_aux")
        ], width=6)])
    ])


@callback(Output("plot_pca", "figure"),
          [Input("store", "data"),
           Input("method_embedding", "value")],
           suppress_callback_exceptions=True
          )
def createPCA(datos, metodo):
    df = pd.DataFrame(datos["data"])
    X = df.iloc[:,1:-1]
    Y = df["AV"]
    pacientes = df["PACIENTES"]
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(X)
    if(metodo=="tsne"):
        embedding = TSNE(n_components=2, random_state=1)
    elif(metodo =="isomap"):
        embedding = Isomap(n_components=2)
    elif(metodo =="umap"):
        embedding = UMAP(n_components=2)
    elif(metodo =="mds"):
        embedding = MDS(n_components=2)
    else:
        embedding =  PCA(n_components=2)

    embedded_data = embedding.fit_transform(df_scaled)


    xval = embedded_data[:,0]
    yval = embedded_data[:,1]
    
    df_plot = pd.DataFrame({"paciente":pacientes,
                            "variable_1":xval,
                            "variable_2":yval,
                            "color":Y.astype(str)})

    fig = px.scatter(df_plot, x="variable_1", y="variable_2", 
                     title='Scatter plot tras aplicar '+metodo, 
                     hover_name=df_plot.columns.to_list()[0],
                     color = "color",
                     custom_data=['paciente'],
                     color_discrete_sequence =['blue', 'red'])
    
    fig.update_traces(marker=dict(size=10)) 
    fig.update_layout( 
                            plot_bgcolor="lightpink",
                            paper_bgcolor="lightpink",
                     )


    return fig

@callback(Output("plot_pca_aux","figure"),
           [Input("plot_pca","hoverData")],
           [State("store","data")],
           suppress_callback_exceptions=True)
def createHoverPlot(hoverData, datos):
    if hoverData is not None:
        data = pd.DataFrame(datos["data"])
        seleccionado = hoverData['points'][0]['customdata'][0]
        point_index = data.index[data['PACIENTES'] == seleccionado].tolist()[0]

        df = data.iloc[:,1:-1]
        columnas = data.columns[1:-1]

        valores = df.iloc[point_index,:] 


        df = pd.DataFrame({"Valor":valores,
                           "Variable":columnas})
        
        fig = px.bar(df, x='Variable', y='Valor',
                      title='Valores para cada uno de los atributos del dato seleccionado')
        fig.update_layout(
                            plot_bgcolor="lightpink",
                            paper_bgcolor="lightpink",
                         )

        return fig
    else:
        return {}





