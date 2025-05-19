from dash import Dash, html, dcc, dash_table
from business.graph_manager import GraphManager

app = Dash()

graph_manager = GraphManager()
deaths_by_department_map_graph = graph_manager.generate_deaths_by_department_map_graph()
deaths_by_month_line_graph = graph_manager.generate_deaths_by_month_line_graph()
most_violent_cities_bar_graph = graph_manager.generate_most_violent_cities_bar_graph()
least_mortality_cities_circle_graph = graph_manager.generate_least_mortality_cities_circle_graph()
principal_death_reasons_table = graph_manager.generate_principal_death_reasons_table()
age_histogram_graph = graph_manager.generate_age_histogram_graph()
gender_stacked_bar_graph = graph_manager.generate_gender_stacked_bar_graph()

app.layout = html.Div([
    html.H1("Estudiante: Miguel Ángel Manrique Téllez"),
    html.H2("Mapa de muertes por departamento en Colombia (2019)"),
    dcc.Graph(id='grafica-mapa-muertes-por-departamento', figure=deaths_by_department_map_graph),
    html.H2("Muertes por Departamento en Colombia (2019)"),
    dcc.Graph(id='grafica-muertes', figure=deaths_by_month_line_graph),
    html.H2("Ciudades más violentas en Colombia (2019)"),
    dcc.Graph(id='grafica-ciudades-mas-violentas', figure=most_violent_cities_bar_graph),
    html.H2("Ciudades con menor índice de mortalidad en Colombia (2019)"),
    dcc.Graph(id='grafica-ciudades-menor-indice-mortalidad', figure=least_mortality_cities_circle_graph),
    html.H2("Principales causas de muerte en Colombia (2019)"),
    dash_table.DataTable(
        id='tabla-causas',
        columns=[
            {"name": "Código CIE-10", "id": "COD_MUERTE"},
            {"name": "Descripción", "id": "DESCRIPCION"},
            {"name": "Total de Casos", "id": "TOTAL_CASOS", "type": "numeric"}
        ],
        data=principal_death_reasons_table.to_dict('records'),
        sort_action="native",
        style_cell={
            'padding': '8px',
            'textAlign': 'left',
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold'
        },
        page_size=10
    ),
    html.H2("Distribución de muertes según grupos de edad en Colombia (2019)"),
    dcc.Graph(id='grafica-distribucion-muertes-por-edad', figure=age_histogram_graph),
    html.H2("Muertes por sexo en Colombia (2019)"),
    dcc.Graph(id='grafica-muertes-por-sexo', figure=gender_stacked_bar_graph),
])

if __name__ == '__main__':
    app.run(debug=True)