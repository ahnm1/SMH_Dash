import plotly.express as px

class LineGraph:
    def __init__(self):
        pass
    
    def get_prices_graph(self):
        pass

    def get_multi_energy_graph(self, dfe_no_total):
        fig_gwha = px.line(dfe_no_total, x='month', y='amount', color='type', title = 'Production by Type')
        fig_gwha.update_layout(
            {'legend': {'title': 'Type'},
            'xaxis': {'title': {'text': 'Date'}},
            'yaxis': {'title': {'text': 'GWh'}}}
        )
        return fig_gwha
    
    def get_line_energy_graph(self, df_total):
        fig_gwht = px.line(df_total.where(
            df_total['type'] == 'Total'), x = 'month', y = 'amount', title = 'Total Energy Production')
        fig_gwht.update_layout(
            {'legend': {'title': 'Type'},
            'xaxis': {'title': {'text': 'Date'}},
            'yaxis': {'title': {'text': 'GWh'}}}
        )
        
        return fig_gwht

