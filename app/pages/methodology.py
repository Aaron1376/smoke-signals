# methodology.py
import dash
from dash import html

dash.register_page(__name__, path="/methodology", name="Methodology")

layout = html.Div([
    # Methodology Section
    html.Section(
        html.Div([
            html.H2("Methodology", className="section-title"),
            html.Div([
                html.Div([
                    html.H3("Research Approach", className="card-title"),
                    html.P(
                        "Our methodology involves collecting and preprocessing historical PM2.5 data, integrating meteorological and wildfire datasets, "
                        "and applying advanced machine learning models such as LSTMs and GNNs for time series forecasting.",
                        className="card-text"
                    ),
                    html.Ul([
                        html.Li("Data Collection: Gather PM2.5, meteorological, and wildfire data from reliable sources"),
                        html.Li("Data Preprocessing: Clean and normalize data for analysis"),
                        html.Li("Model Development: Train and evaluate forecasting models"),
                        html.Li("Validation: Compare model predictions with actual observations"),
                    ], className="card-list")
                ], className="info-card info-card--wide")
            ], className="cards-grid"),
        ], className="container"),
        className="section section--white"
    ),
])