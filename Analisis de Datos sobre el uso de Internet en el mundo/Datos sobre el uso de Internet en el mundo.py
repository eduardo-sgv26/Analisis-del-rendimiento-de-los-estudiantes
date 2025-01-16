from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

# Inicializa la aplicación Dash con un tema de Bootstrap
app = Dash(external_stylesheets=[dbc.themes.CERULEAN])

# Carga de datos desde un archivo CSV
db = pd.read_csv("internet_users.csv")

# Procesamiento de datos (si es necesario)
# Ejemplo: Renombrar columnas para mejor legibilidad
db.rename(columns={
    "Location": "País",
    "Rate (WB)": "Tasa_WB",
    "Year": "Año_WB",
    "Rate (ITU)": "Tasa_ITU",
    "Year.1": "Año_ITU",
    "Users (CIA)": "Usuarios_CIA",
    "Year.2": "Año_CIA",
    "Notes": "Notas"
}, inplace=True)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Análisis de Usuarios de Internet", style={"textAlign": "center"}),

    # Dropdown para seleccionar una categoría de análisis
    dcc.Dropdown(
        id="categoria-dropdown",
        options=[
            {"label": "Tasa (WB)", "value": "Tasa_WB"},
            {"label": "Tasa (ITU)", "value": "Tasa_ITU"},
            {"label": "Usuarios (CIA)", "value": "Usuarios_CIA"},
        ],
        value="Tasa_WB",
        placeholder="Selecciona una categoría",
        style={"marginBottom": "20px"}
    ),

    # Tabla dinámica
    dash_table.DataTable(
        id="tabla-dinamica",
        columns=[
            {"name": "País", "id": "País"},
            {"name": "Tasa (WB)", "id": "Tasa_WB"},
            {"name": "Año (WB)", "id": "Año_WB"},
            {"name": "Tasa (ITU)", "id": "Tasa_ITU"},
            {"name": "Año (ITU)", "id": "Año_ITU"},
            {"name": "Usuarios (CIA)", "id": "Usuarios_CIA"},
            {"name": "Año (CIA)", "id": "Año_CIA"},
            {"name": "Notas", "id": "Notas"},
        ],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "#f8f9fa", "fontWeight": "bold"},
    ),

    # Gráfico interactivo
    dcc.Graph(id="grafico-usuarios"),
])

# Callbacks para actualizar componentes
@app.callback(
    [
        Output("tabla-dinamica", "data"),
        Output("grafico-usuarios", "figure")
    ],
    [
        Input("categoria-dropdown", "value")
    ]
)
def actualizar_componentes(categoria):
    # Filtra y prepara los datos para la tabla
    tabla_data = db[["País", "Tasa_WB", "Año_WB", "Tasa_ITU", "Año_ITU", "Usuarios_CIA", "Año_CIA", "Notas"]].to_dict("records")

    # Crea un gráfico de barras con la categoría seleccionada
    figura = px.bar(
        db,
        x="País",
        y=categoria,
        title=f"Distribución de {categoria.replace('_', ' ')} por País",
        labels={"País": "País", categoria: categoria.replace('_', ' ')}
    )

    return tabla_data, figura

# Ejecución de la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
