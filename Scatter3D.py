import plotly.express as px

class Scatter3D:
    def __init__(self):
        pass

    def get_plot(self, df_price):
        fig_3d = px.scatter_3d(
            df_price,
            x = 'Lufttemperatur AVG',
            y = 'Vindhastighet AVG',
            z = 'SpotPriceEUR',
            color = 'Vindhastighet AVG',
            hover_name = 'Timestamp'
        )
        fig_3d.update_layout(
            {'coloraxis': {'colorbar': {'title': {'text': 'Wind Average'}}}}
        )
        fig_3d.update_scenes( 
            {
                'xaxis': {'title': {'text': 'Air Temperature'}},
                'yaxis': {'title': {'text': 'Wind Average'}},
                'zaxis': {'title': {'text': 'Spot Price €'}}
            },
            xaxis_autorange="reversed"
        )
        return fig_3d


