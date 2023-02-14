#%%
import calendar
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

from Scatter3D import Scatter3D
from LineGraph import LineGraph
from ML.MLPredict import MLPredict

pio.templates.default = 'plotly_dark' # 'ggplot2' 
#%%

EXCHANGE_RATE = 0.08918

nonull_file = 'nonull_elpriser_och_vader.csv'
df_price = pd.read_csv(nonull_file, delimiter = ';')

#%%
dfe         = pd.read_csv('full_clean_energy.csv')
dfe_no_total = dfe.where(dfe['type'] != 'Total')
# df_price = pd.read_csv('elpriser_och_vader.csv', delimiter=';')
# df_price['SEK'] = df_price['SpotPriceEUR'] * EXCHANGE_RATE
df_price['SEK/KWh'] = df_price['SpotPriceEUR'] * (EXCHANGE_RATE / 10)
new_p_columns = ['Timestamp', 'PriceArea', 'Spot Price EUR', 'Wind m/s',
       'Temperature °C', 'SEK/KWh']
dfc_price = df_price.round(1).copy()
dfc_price.columns = new_p_columns

fig_3d   = Scatter3D().get_plot(dfc_price)

fig_gwha = LineGraph().get_multi_energy_graph(dfe_no_total)
fig_gwht = LineGraph().get_line_energy_graph(dfe.where(dfe['type'] == 'Total'))
fig_gwht.update_traces(line_color='#c03bf5')
# with open('px_single.txt', 'w') as outp:
#             outp.write(str(fig_gwht))

fig_temp_wind = px.line(df_price, x = 'Timestamp', y = ['Vindhastighet AVG', 'Lufttemperatur AVG'], color_discrete_map={
    "Vindhastighet AVG": '#3BCDF5',#"#2362ec",
    "Lufttemperatur AVG": '#F5633B' #"#f5db1c"
    }).update_layout({'legend': {'title': 'Parameter'},
    'xaxis': {'title': {'text': 'Date'}},
    'yaxis': {'title': {'text': 'Value'}}})

ml  = MLPredict()
app = Dash(__name__)
app.title = 'PowerPredictors'
app.layout = html.Div(children=[
    # html.H1(children='Wind + Temperature ?'),
    dcc.Graph(
            id='s3d-graph',
            figure = fig_3d
        ),
    html.Div(children = [
        dcc.Graph(
            id='line-graph-qwht',
            figure = fig_temp_wind,
        ),
        html.Div([
            html.H3('Predict Price', style=({'align-items': 'center'})),
            html.Div([
                
                html.Div([
                    'Hour ',
                    dcc.Input(id='hour-in', value='0', type='number')
                ]),
                html.Br(),
                html.Div([
                    'Day ',
                    dcc.Input(id='day-in', value='1', max = 7,min = 1, type='number')
                ]),
                html.Br(),
                html.Div([
                    'Month ',
                    dcc.Input(id='month-in', value='1', max = 12, min = 1, type='number')
                ]),
                html.Br(),
                html.Div([
                    'Wind ',
                    dcc.Input(id='wind-in', value='0', min = 0, type='number')
                ]),
                html.Br(),
                html.Div([
                    'Temp ',
                    dcc.Input(id='temp-in', value='0', type='number', style = ({'align-items': 'end'}))
                ]),
                ], id = 'augur-inner'),
                html.Br(),
                html.Div(id='hour-output'),
                html.Div(id='day-output'),
                
                html.Div(id='month-output'),
                html.Div(id='wind-output'),

                html.Div(id='temp-output'),

                html.Div(id='result-output',style=({'font-size': 16, 'border-top': '2px solid purple', 'margin-top': '4px', 'padding-top': '4px'})),
                html.P(id='fake-in'),
            
        ],id= 'augur-outer',style=({
            'align-items': 'center',
            'margin-left': 32,
            'padding-left': 16,
            'margin-right': 32,
            'padding-right': 16,
            }
            ))
    ], id = 'graph-div'),
        dcc.Graph(
            id = 'line-graph-gwh',
            figure = fig_gwht,
        ),  
    dcc.Graph(
            id = 'multi-graph-price',
            figure = fig_gwha
        ),
    
], id = 'html-div')

@app.callback(
    Output(component_id='hour-output', component_property='children'),
    Output(component_id='day-output', component_property='children'),
    Output(component_id='month-output', component_property='children'),
    Output(component_id='wind-output', component_property='children'),
    Output(component_id='temp-output', component_property='children'),
    Output(component_id='result-output', component_property='children'),
    Input(component_id='hour-in', component_property='value'),
    Input(component_id='day-in', component_property='value'),
    Input(component_id='month-in', component_property='value'),
    Input(component_id='wind-in', component_property='value'),
    Input(component_id='temp-in', component_property='value'),
    Input(component_id='fake-in', component_property='value'),
)
def update_output_div(hour_val, day_val, month_val, wind_val, temp_val, result_str):
    if month_val == '0':
        # print(f'{month_val}: no go', type(month_val))
        return (
            f'A {day_val}', f'at {hour_val}:00,',
            f'in the month of 0',
            f'with wind average at {wind_val} m/s',
            f'and average temperatur of {temp_val}°C',
            f'Predicted Price: 0 SEK / KWh')

    elif month_val == None:
        # print(f'{month_val}: no go', type(month_val))
        return (
            f'A {day_val}', f'at {hour_val}:00,',
            f'in the month of 0',
            f'with wind average at {wind_val} m/s',
            f'and average temperatur of {temp_val}°C',
            f'Predicted Price: 0 SEK / KWh')
    else:
        # print(f'{month_val}: yes go', type(month_val))
        result_str = ml.get_input_and_predict(wind_val, temp_val, month_val, hour_val, day_val)

        return (
            f'A {calendar.day_name[int(day_val)-1]}', f'at {hour_val}:00,',
            f'in the month of {calendar.month_name[int(month_val)]}',
            f'with wind average at {wind_val} m/s',
            f'and average temperatur of {temp_val}°C',
            f'Predicted Price: {result_str} SEK / KWh')

if __name__ == '__main__':
    app.run_server(debug = True)
