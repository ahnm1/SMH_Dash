#%%
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio

from Scatter3D import Scatter3D
from LineGraph import LineGraph

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
# fig_nonull = LineGraph().get_plot(
fig_gwha = LineGraph().get_multi_energy_graph(dfe_no_total)
fig_gwht = LineGraph().get_line_energy_graph(dfe.where(dfe['type'] == 'Total'))

fig_temp_wind = px.line(df_price, x = 'Timestamp', y = ['Vindhastighet AVG', 'Lufttemperatur AVG'])

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='W i n d + T e m p e r a t u r e'),
    dcc.Graph(
            id='s3d-graph',
            figure=fig_3d
        ),
    html.H1(children = 'D o e s     i t     =   P r i c e ?'),
    html.Div(children = [
        dcc.Graph(
            id='line-graph-price',
            figure=fig_temp_wind,
        ),
        dcc.Graph(
            id='line-graph-gwht',
            figure=fig_gwht,
        ),   
    ], id = 'graph-div'),
    html.P(children = 'So is there a correlation \
        between temperature, wind and price for electricity.'),
    dcc.Graph(
            id='multi-graph-gwh',
            figure=fig_gwha
        ),
], id = 'html-div')

if __name__ == '__main__':
    app.run_server(debug=True)
