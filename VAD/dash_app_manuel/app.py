import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Output, Input, State, callback,dash_table
from dash.exceptions import PreventUpdate
import base64
import datetime
import io

import pandas as pd

# Creación de la App

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG],
                 suppress_callback_exceptions=True)


# Menú principal

navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Explorar más",
    ),
    brand=[
        html.Div("Máster en Ciencia de Datos", style={"font-size": "1.5rem"}),
        html.Div("Aplicación de Detección de Arritmias", style={"font-size": "1rem"}),
    ],
    color="secondary",
    dark=True,
    className="mb-2",
    style={"background-color": "#007bff"}  # Cambia el color de fondo aquí
)

# Carga de datos

upload = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastrar y soltar o ',
            html.A('Seleccione Fichero')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    )


app.layout = dbc.Container(
    [dcc.Store(id='store', storage_type='session', data = {}), upload, navbar, dash.page_container],
    fluid=True,
)

### DEFINICIÓN DE LA LOGICA #####

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            cols = df.columns[1:-4]
            for i in range(len(cols)):
                df[cols[i]] = df[cols[i]].str.replace(",", ".").astype(float)
        else:
            return {}

    except Exception as e:
        print(e)
        return {}

    store = {
        "data": df.to_dict("records"),
        "datos":  df.to_dict(),
        "columns": [{"name": i, "id": i} for i in df.columns],
    }

    return store


## CALLBACK PARA LA CARGA DE UN DATAFRAME EN EL STORE DEFINIDO EN EL LAYOUT ##
@app.callback(
     Output("store", "data"),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')],
    suppress_callback_exceptions=True
)
def update_output(list_of_contents, list_of_names):

    if list_of_contents is not None:
        children = [parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
        print(children)
        if(len(children)>0):
            return children[0]
        else:
            return  {}


if __name__ == "__main__":
    app.run_server(debug=True)
