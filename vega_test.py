# We can have altair work directly into vscode with the python extension.
# (altair.renderer by default is html)
# Run it in interactive window
# 

# Use dash to display graph and control callbacks.
# Some reading
# The Grammar of Graphics, Leland Wilkinson

import altair
import io

from vega_datasets import data

from dash.dependencies import Input,Output

import dash
from dash import html, dcc

cars = data.cars()

app = dash.Dash(__name__)
COLUMNS = [
    "Miles_per_Gallon",
    "Acceleration",
    "Displacement",
    "Cylinders",
    "Weight_in_lbs"
]

# Make two dimensions show their correlation
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label("x-axis", style={"color": "silver"}),
            dcc.Dropdown(
                id="x_axis",
                options=[{
                    "label": feature,
                    "value": feature}
                    for feature in COLUMNS
                ],
                value="Miles_per_Gallon"
            )
        ]),
        html.Div([
            html.Label("y-axis", style={"color":"silver"}), 
            dcc.Dropdown(
                id="y_axis",
                options=[{
                    "label": feature,
                    "value": feature
                } for feature in COLUMNS
                ],
                value="Acceleration"
            )
        ])
    ]),
    html.Iframe(
        id="plot",
        height= "700",
        width="1200",
        sandbox="allow-scripts"
    )
])


@app.callback(
        Output("plot","srcDoc"),
        [
            Input("x_axis", "value"),
            Input("y_axis","value")
        ]
)
def make_figure(x_axis,y_axis):
    brush = altair.selection_interval()
    base = altair.Chart(cars)

    scatter = (
        base.mark_point()
        .encode( 
            x = x_axis,
            y = y_axis,
            color = "Origin:N")
        .properties( 
            width = 400,
            height = 600)
    )

    histogram = (
        base.mark_bar()
        .encode(
            x = altair.X("Horsepower:Q", bin=True),
            y = "count()",
            color = "Origin:N")
        # .transform_filter(brush.ref())
    ).properties( height = 600 )

    chart = altair.hconcat(scatter, histogram)

    cars_html = io.StringIO()
    chart.save(cars_html, "html")

    return cars_html.getvalue()


app.run()
