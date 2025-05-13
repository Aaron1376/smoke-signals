# analytics.py

import dash
from dash import html
from components.time_series import layout_time_series

dash.register_page(__name__, path="/analytics", name="Findings")

layout = html.Div([
    # Hero Section
    html.Section(
        html.Div([
            html.H1("Analytics Dashboard", className="hero-title"),
            html.P(
                "Explore PM2.5 levels across California during wildfire seasons",
                className="hero-text"
            ),
        ], className="container"),
        className="hero hero--secondary"
    ),

    # Time Series Section
    html.Section(
        html.Div([
            html.H2("Time Series Analysis", className="section-title"),
            html.Div(
                layout_time_series(),
                className="analytics-container"
            ),
        ], className="container"),
        className="section section--white"
    ),
])
