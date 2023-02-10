from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import plotly.io as pio

pio.templates.default = "plotly_dark"

app = Dash(__name__)
# app.css.append_css({'external_url': '/static/style.css'})
# app.server.static_folder = 'static'

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")#.update_layout({'paper_bgcolor': 'black'})

app.layout = html.Tbody(children = [
    html.Div(children=[
    # html.Tbody(),
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
])], style = {'backgroundColor': 'wheat', 'margin': 0}
)
# print(app.layout)
if __name__ == '__main__':
    app.run_server(debug=True)