import calendar
from dash import Dash, dcc, html, Input, Output
from ML.MLPredict import MLPredict

ml  = MLPredict()
app = Dash(__name__)

app.layout = html.Div([
    html.H3('Predict Price',style=({'align-items': 'center'})),
    html.Div([
        
        html.Div([
            "Hour: ",
            dcc.Input(id='hour-in', value='0', type='number')
        ]),
        html.Br(),
        html.Div([
            "Month: ",
            dcc.Input(id='month-in', value='0', max = 12, type='number')
        ]),
        html.Br(),
        html.Div([
            "Wind: ",
            dcc.Input(id='wind-in', value='0', type='number')
        ]),
        html.Br(),
        html.Div([
            "Temperature: ",
            dcc.Input(id='temp-in', value='0', type='number')
        ]),
        ], id = 'augur-inner'),
        html.Br(),
        html.Div(id='hour-output'),
        html.Div(id='month-output'),
        html.Div(id='wind-output'),

        html.Div(id='temp-output'),
        # html.P('The predicted price is:'),

        html.Div(id='result-output',style=({'font-size': 22})),
        html.P(id='fake-in'),
    
],id= 'augur-outer',style=({'align-items': 'center'}))


@app.callback(
    Output(component_id='hour-output', component_property='children'),
    Output(component_id='month-output', component_property='children'),
    Output(component_id='wind-output', component_property='children'),
    Output(component_id='temp-output', component_property='children'),
    Output(component_id='result-output', component_property='children'),
    Input(component_id='hour-in', component_property='value'),
    Input(component_id='month-in', component_property='value'),
    Input(component_id='wind-in', component_property='value'),
    Input(component_id='temp-in', component_property='value'),
    Input(component_id='fake-in', component_property='value'),
)
def update_output_div(hour_val, month_val, wind_val, temp_val, result_str):
    if month_val == '0':
        print(f'{month_val}: no go', type(month_val))
        return (
            f'At {hour_val}:00,',
            f'in th month of 0',
            f'with wind average at {wind_val} m/s',
            f'and average temperatur of {temp_val}°C',
            f'Predicted price is: 0')

    elif month_val == None:
        print(f'{month_val}: no go', type(month_val))
        return (
            f'At {hour_val}:00,',
            f'in th month of 0',
            f'with wind average at {wind_val} m/s',
            f'and average temperatur of {temp_val}°C',
            f'Predicted price is: 0')
    else:
        print(f'{month_val}: yes go', type(month_val))
        result_str = ml.get_input_and_predict(wind_val, temp_val, month_val, hour_val)
        # print(a)

        return (
            f'At {hour_val}:00,',
            f'in th month of {calendar.month_name[int(month_val)]}',
            f'with wind average at {wind_val} m/s',
            f'and average temperatur of {temp_val}°C',
            f'Predicted price is: {result_str}, SEK / KWh')


if __name__ == '__main__':
    app.run_server(debug = True)