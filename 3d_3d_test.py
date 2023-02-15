#%%
import plotly.express as px
import pandas as pd
import plotly.io as pio
pio.templates.default = 'plotly_dark' # 'ggplot2' 

EXCHANGE_RATE = 0.08918

df_price = pd.read_csv('nonull_elpriser_och_vader.csv', delimiter=';')
df_price['SEK/KWh'] = df_price['SpotPriceEUR'] * (EXCHANGE_RATE / 10)

new_p_columns = ['Timestamp', 'PriceArea', 'Spot Price EUR', 'Wind m/s',
       'Temperature °C', 'SEK/KWh']
dfc_price = df_price.round(1).copy()
dfc_price.columns = new_p_columns

fig_3d = px.scatter_3d(
            dfc_price,
            x = 'Temperature °C',
            y = 'Wind m/s',
            z = 'SEK/KWh',
            color = 'Wind m/s',
            hover_name = 'Timestamp',
            # title = 'Scatter'
        )

fig_3d.update_layout(
    {'coloraxis': {'colorbar': {'title': {'text': 'Avg. Wind'}}}}
)

fig_3d.update_scenes( 
    {
        'xaxis': {'title': {'text': 'Avg. Temperature °C'}},
        'yaxis': {'title': {'text': 'Avg. Wind m/s'}},
        'zaxis': {'title': {'text': 'SEK / KWh'}}#'Spot Price €'}}
    },
    xaxis_autorange="reversed"
)

# %%
