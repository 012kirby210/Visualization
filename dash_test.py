import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output

import plotly.express as px

df = px.data.tips()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("My dash app"),
    dcc.Graph(id="graph"),
    html.Label([
        "colorscale",
        dcc.Dropdown(
            id="colorscale-dropdown",
            clearable=False,
            value="plasma",
            options=[
                {"label":color, "value":color}
                for color in px.colors.named_colorscales()
                    ]
        )
    ])
])

@app.callback(
        Output("graph", "figure"),
        [Input("colorscale-dropdown", "value")]
)

# From the test data from px.data
def update_figure(colorscale):
    return px.scatter(
        df,
        x="total_bill",
        y="tip",
        color="size",
        color_continuous_scale=colorscale,
        render_mode="webgl",
        title="Y/X"
    )


app.run()