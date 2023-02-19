from dash import html, dcc

widget = html.Div([  # Div for Widget
            html.H3('Augur', style=({'align-items': 'center', 'border-bottom': '2px solid #6a178b', 'margin-bottom': '8px', 'padding-bottom': '4px'})),
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
                html.Div(id='result-output',style=({'font-size': 16, 'border-top': '2px solid #6a178b', 'margin-top': '4px', 'padding-top': '4px'})),
                html.P(id='fake-in'),
            
        ],id= 'augur-outer',style=({
            'align-items': 'center',
            'margin-left': 32,
            'padding-left': 16,
            'margin-right': 32,
            'padding-right': 16,
            }
            ))
