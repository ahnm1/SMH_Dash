#%%
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

pio.templates.default = "plotly_dark"

#%%
## define energy df without 'total'

dfe  = pd.read_csv('full_clean_energy.csv')

dfex = dfe['month'].where(dfe['type'] != 'Total')
dfey = dfe['amount'].where(dfe['type'] != 'Total')
ecolor = dfe['type'].where(dfe['type'] != 'Total')

df_price = pd.read_csv('elpriser_och_vader.csv', delimiter=';')

#%%
## Normalize values in column for better visualization

def normalize_values(df):
    # copy the data
    df_z_scaled = df.copy()
    
    for column in df.columns[2:]:
        print(column)
    # apply normalization technique to Column
        column = f'{column}'
        df_z_scaled[column] = (df_z_scaled[column] - df_z_scaled[column].mean()) / df_z_scaled[column].std()    
    
    # view normalized data  
    return df_z_scaled

#%%
## normalized df definitions 

df_norm   = normalize_values(df_price)

timestamp = df_norm['Timestamp']
temp      = df_norm['Lufttemperatur AVG']
wind      = df_norm['Vindhastighet AVG']
price     = df_norm['SpotPriceEUR']

#%%
## go.Figure scatter-line function

def make_scatter(x, y, name, color):
    return go.Scatter(
        x = x,
        y = y,
        # mode = 'markers',
        # marker_color = color,
        name = name,
        )
    
# %%

fig = go.Figure()
#%%
## Add Trace method

fig.add_trace(make_scatter(timestamp, wind, 'wind', 'steelblue'))
fig.add_trace(make_scatter(timestamp, temp, 'temp', 'gold'))
# fig.add_trace(make_scatter(timestamp, price, 'price', 'green'))
fig.add_trace()

#%%
## 3D plot

# fig = 
px.scatter_3d(df_norm, x = 'Lufttemperatur AVG', y = 'Vindhastighet AVG', z = 'SpotPriceEUR', color = 'Vindhastighet AVG')

# %%
# fig.show()

#%%
## All other power (px)

## All + total
# fig.add_trace(make_scatter(dfe['month'], dfe['amount'], 'Energy Production', dfe['type']))

figg = px.line(dfe, x = dfex, y = dfey, color = ecolor)

figg.update_layout(
    {'legend': {'title': 'Type'},
    'xaxis': {'title': {'text': 'Date'}},
    'yaxis': {'title': {'text': 'Amount'}}}
)

# %%
## save px.line dump

with open('px_dump.json', 'w') as out:
    out.writelines(f'{figg}')