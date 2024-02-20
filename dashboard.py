import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input,Output
# from dash.exceptions import PreventUpdate
# import seaborn as sns

df1 = pd.read_csv('data/raw/costs_2022.csv')
df2 = pd.read_csv('data/raw/revenue_2022.csv')

## EDA Process
# print(df1.shape) = (336, 16)
# print(df2.shape) = (109, 16)
### Finding and treating nulls
# (
#     df1
#     .isnull()
#     .melt()
#     .pipe(
#         lambda df: (
#             sns.displot(
#                 data=df,
#                 y='variable',
#                 hue='value',
#                 multiple='fill',
#                 aspect=2
#             ).savefig("data/procesed/costs_isnull.png")  # Guardar el gráfico como un archivo PNG
#         )
#     )
# )
# (
#     df2
#     .isnull()
#     .melt()
#     .pipe(
#         lambda df: (
#             sns.displot(
#                 data=df,
#                 y='variable',
#                 hue='value',
#                 multiple='fill',
#                 aspect=2
#             ).savefig("data/procesed/revenue_isnull.png")  # Guardar el gráfico como un archivo PNG
#         )
#     )
# )
# df1.dtypes
# df2.dtypes

## ETL Process
df1['Expense Item'] = df1['Expense Item'].astype(str)
df1['Line Of Business'] = df1['Line Of Business'].astype('category')
cols_to_clean = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Total']
df2[cols_to_clean] = df2[cols_to_clean].replace('[\$,]', '', regex=True).astype(float).round(2)
dtype_dict = {
    'Client Name': str,
    'Line Of Business': 'category',
    'Jan': float, 'Feb': float, 'Mar': float, 'Apr': float,
    'May': float, 'Jun': float, 'Jul': float, 'Aug': float,
    'Sep': float, 'Oct': float, 'Nov': float, 'Dec': float,
    'Total': float
}
df2 = df2.astype(dtype_dict)

# pd.merge(df1, df2, left_on='Expense Item', right_on='Client Name', how='inner')['Expense Item'].value_counts() ->Expense Item /n Blank    216 /n Name: count, dtype: int64

# Derretir los DataFrames con la columna 'Line of Business' incluida
df_melted1 = df1.melt(id_vars=['Line Of Business'], value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Total'], 
                      var_name='Month', value_name='Value')
df_melted2 = df2.melt(id_vars=['Line Of Business'], value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Total'], 
                      var_name='Month', value_name='Value')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('Costos vs Ingresos'),
    ], className='banner'),

        html.Div([
        html.Div([
            html.P('Seleccione qué gráfica desea ver', className = 'fix_label', style={'color':'black', 'margin-top': '2px'}),
            dcc.RadioItems(id = 'CostoVsIngresos', 
                            labelStyle = {'display': 'inline-block'},
                            options = [
                                {'label' : 'Costos', 'value' : 'costos'},
                                {'label' : 'Ingresos', 'value' : 'ingresos'}
                            ], value = 'costos',
                            style = {'text-aling':'center', 'color':'black'}, className = 'dcc_compon'),
        ], className = 'create_container2 five columns', style = {'margin-bottom': '20px'}),
        html.Div([
            dcc.Dropdown(id="line-of-business-dropdown",
                            placeholder='Seleccione una línea de negocio',
                            multi=True),
                ], className = 'create_container2 five columns', style = {'margin-bottom': '20px'}),    
    
    ], className = 'row flex-display'),

    html.Div([
        html.Div([
            dcc.Graph(id = 'my_graph', figure = {})
        ], className = 'create_container2 eight columns')
    ], className = 'row flex-display'),

])

# Función para actualizar la gráfica
def update_graph(selected_option_radio, selected_option_dropdown):
    if selected_option_radio == 'costos':
        # Código para actualizar la gráfica para costos
        df = df_melted1
    elif selected_option_radio == 'ingresos':
        # Código para actualizar la gráfica para ingresos
        df = df_melted2

    if selected_option_dropdown:
        # Asegurarnos de que selected_option_dropdown sea una lista plana
        selected_option_dropdown = np.ravel(selected_option_dropdown)

        # Filtrar el DataFrame según la opción seleccionada en el dropdown
        df = df[df['Line Of Business'].isin(selected_option_dropdown)]

    fig = px.bar(
        df,
        x='Month',
        y='Value',
        color='Line Of Business',
        barmode='overlay'
    )

    return fig

# Función para actualizar las opciones del dropdown
def update_dropdown(selected_option_radio):
    if selected_option_radio == 'costos':
        # Obtener las opciones del dropdown para costos
        dropdown_options = [{'label': label, 'value': label} for label in df_melted1['Line Of Business'].unique()]
    elif selected_option_radio == 'ingresos':
        # Obtener las opciones del dropdown para ingresos
        dropdown_options = [{'label': label, 'value': label} for label in df_melted2['Line Of Business'].unique()]

    return dropdown_options

# Callbacks
@app.callback(
    [Output('my_graph', 'figure'),
     Output('line-of-business-dropdown', 'options')],
    [Input('CostoVsIngresos', 'value'),
     Input('line-of-business-dropdown', 'value')]
)
def update_graph_and_dropdown(selected_option_radio, selected_option_dropdown):
    dropdown_options = update_dropdown(selected_option_radio)
    
    # Determinar el disparador actual
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Actualizar la gráfica si el cambio fue en 'CostoVsIngresos' o 'line-of-business-dropdown'
    if triggered_input == 'CostoVsIngresos' or triggered_input == 'line-of-business-dropdown':
        fig = update_graph(selected_option_radio, selected_option_dropdown)
        return fig, dropdown_options
    else:
        # Si no hubo cambios en 'CostoVsIngresos' o 'line-of-business-dropdown', devolver los valores actuales
        return dash.no_update, dropdown_options

if __name__ == '__main__':
    app.run_server(debug=True)