import plotly.express as px

class Scatter3D:
    def __init__(self):
        pass

    def get_plot(self, df_price):
        fig_3d = px.scatter_3d(
            df_price,
            x = 'Temperature °C',
            y = 'Wind m/s',
            z = 'SEK/KWh',
            color = 'Wind m/s',
            hover_name = 'Timestamp'
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
        return fig_3d


