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
nonull_file = 'nonull_elpriser_och_vader.csv'
df_nonull = pd.read_csv(nonull_file, delimiter = ';')
df_nonull.columns
#%%
dfe         = pd.read_csv('full_clean_energy.csv')
dfe_no_total = dfe.where(dfe['type'] != 'Total')
df_price = pd.read_csv('elpriser_och_vader.csv', delimiter=';')

fig_3d   = Scatter3D().get_plot(df_price)
# fig_nonull = LineGraph().get_plot(
fig_gwha = LineGraph().get_multi_energy_graph(dfe_no_total)
fig_gwht = LineGraph().get_line_energy_graph(dfe.where(dfe['type'] == 'Total'))

fig_price = px.line(df_nonull, x = 'Timestamp', y = 'SpotPriceEUR')

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Wind + Temperature = Price?'),
    html.P(children = 'An application to display correlations \
        between temperature, wind and price for electricity.'),
    dcc.Graph(
            id='s3d-graph',
            figure=fig_3d
        ),
    html.Div(children = [
        dcc.Graph(
            id='line-graph-price',
            figure=fig_price,
        ),
        dcc.Graph(
            id='line-graph-gwht',
            figure=fig_gwht,
        ),   
    ], id = 'graph-div'),
    dcc.Graph(
            id='multi-graph-gwh',
            figure=fig_gwha
        ),
], id = 'html-div')

if __name__ == '__main__':
    app.run_server(debug=True)
