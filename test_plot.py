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

def z_scale(df):
    # copy the data
    df_z_scaled = df.copy()
    
    for column in df.columns[2:]:
        print(column)
    # apply normalization technique to Column
        column = f'{column}'
        df_z_scaled[column] = (df_z_scaled[column] - df_z_scaled[column].mean()) / df_z_scaled[column].std()    
     
    return df_z_scaled

#%%
# print(df_price)
def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())

# for col in df_price.columns[2:]:
#         df_price[col] = min_max_scale(df_price[col])
# df_price

#%%
## normalized df definitions 

df_norm   = z_scale(df_price)

timestamp = df_norm['Timestamp']
temp      = df_norm['Lufttemperatur AVG']
wind      = df_norm['Vindhastighet AVG']
price     = df_norm['SpotPriceEUR']

#%%
## go.Figure scatter-line function

def make_scatter(x, y, name):#, color):
    return go.Scatter(
        x = x,
        y = y,
        # mode = 'markers',
        # marker_color = color,
        name = name,
        )

def make_bar(x, y, name):
     return go.Bar(
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

# fig.add_trace(make_scatter(timestamp, wind, 'wind', 'steelblue'))
# fig.add_trace(make_scatter(timestamp, temp, 'temp', 'gold'))
# # fig.add_trace(make_scatter(timestamp, price, 'price', 'green'))
# fig.add_trace()

#%%
## 3D plot

fig = px.scatter_3d(df_price, x = 'Lufttemperatur AVG', y = 'Vindhastighet AVG', z = 'SpotPriceEUR', color = 'Vindhastighet AVG')
fig.update_scenes(xaxis_autorange="reversed")
# %%
fig.show()

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

# with open('px_dump_scatter_3d.txt', 'w') as out:
#     out.writelines(f'{fig}')



# %%
nonull_file = 'nonull_elpriser_och_vader.csv'
df_nonull = pd.read_csv(nonull_file, delimiter = ';')
#%%
# fig_price = 
px.line(df_nonull, x = 'Timestamp', y = ['Vindhastighet AVG', 'Lufttemperatur AVG'])
px.line(df_nonull, x = 'Timestamp', y = 'SpotPriceEUR')
# px.line


#%%
## NONULL normalize
for col in df_nonull.columns[2:]:
        df_nonull[col] = min_max_scale(df_nonull[col])
df_nonull
#%%
dfe['amount'] = min_max_scale(dfe['amount'])
dfe_total = dfe.where(dfe['type'] == 'Total')
#%%
px.line(df_nonull, x = 'Timestamp', y = ['Lufttemperatur AVG', 'SpotPriceEUR', 'Vindhastighet AVG'])
#%%
px.line(df_nonull, x = 'Timestamp', y = 'SpotPriceEUR')

#%%
fig = go.Figure()
fig.add_trace(make_bar(dfe_total['month'], dfe_total['amount'], 'Total GWh'))
fig.add_trace(make_scatter(df_nonull['Timestamp'], df_nonull['SpotPriceEUR'], 'Spot Price ???'))

fig.add_trace(make_scatter(df_nonull['Timestamp'], df_nonull['Vindhastighet AVG'], 'Wind Average'))