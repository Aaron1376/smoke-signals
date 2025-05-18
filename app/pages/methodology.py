# methodology.py
import dash
from dash import html

dash.register_page(__name__, path="/methodology", name="Methodology")

layout = html.Div([
    # Hero Section
    html.Section(
        html.Div([
            html.H1("Methodology", className="hero-title"),
            html.P(
                "A detailed breakdown of the data collection, cleaning, testing, and modeling processes used to predict PM2.5 levels.",
                className="hero-text"
            ),
        ], className="container"),
        className="hero hero--primary"
    ),

    # Data Collection Section
    html.Section(
        html.Div([
            html.H2("Data Collection", className="section-title"),
            html.Div([
                html.P(
                    [
                        "Source: ",
                        html.A(
                            "PM2.5_Forecasting_GNN",
                            href="https://github.com/kyleenliao/PM2.5_Forecasting_GNN",
                            target="_blank",
                            style={"color": "#2E7D32", "fontWeight": "bold"}
                        )
                    ],
                    className="card-text"
                ),
                html.P(
                    "The dataset contains meteorological data and PM2.5 data from 2017-2021. ",
                    
                    className="card-text"
                ),
            ], className="info-card"),
        ], className="container"),
        className="section section--light"
    ),

    # Data Cleaning & Feature Engineering Section
    html.Section(
        html.Div([
            html.H2("Data Cleaning & Feature Engineering", className="section-title"),
            html.Div([
                html.P(
                    "Structured Features: Meteorological (temperature, surface pressure, precipitation, frp), PM2.5, cities, and timestamp.",
                    className="card-text"
                ),
                html.Ul([
                    html.Li("Converted the numpy files of the models into a csv."),
                    html.Li("Converted the numpy files of the meteorological data into a csv."),
                    html.Li("Using the latitude and longtitude of the sensors, created a city name column for the sensors."),
                    html.Li("Created an AQI categorical column. Categorized PM2.5 levels into 6 categories: Good, Moderate, Unhealthy for Sensitive Groups, Unhealthy, Very Unhealthy, Hazardous."),

                ], className="card-list")
            ], className="info-card"),
        ], className="container"),
        className="section section--light"
    ),

    # Statistical Testing Section
    html.Section(
        html.Div([
            html.H2("Statistical Testing", className="section-title"),
            html.Div([
                html.P(
                    "Applied a chi-square test on each meteorological variable against the AQI categories to determine which features showed statistically significant associations.",
                    className="card-text"
                ),
                html.P(
                    "Framed the AQI column as a categorical target, ensuring the chi-square test was appropriate for feature selection in a classification context.",
                    className="card-text"
                ),
                html.P(
                    "Trained a Random Forest Classifier on the same dataset and extracted the feature importance scores to quantify each variable’s predictive power.",
                    className="card-text"
                ),
                html.P(
                    "Ranked and compared results from both the chi-square analysis and the Random Forest importances to identify the most influential meteorological predictors of air quality.",
                    className="card-text"
                ),
            ], className="info-card"),
        ], className="container"),
        className="section section--light"
    ),

    # Model Training Section
    html.Section(
        html.Div([
            html.H2("Model Training", className="section-title"),
            html.Div([
                html.P(
                    "Models:",
                    className="card-text"
                ),
                html.Ul([
                    html.Li(
                        "Total PM₂.₅ GNN: A spatio-temporal graph neural network that fuses meteorological inputs (wind components, temperature, pressure, etc.) with fire‐activity features (FRP, fire counts) to predict combined ambient + wildfire PM₂.₅."
                    ),
                    html.Li(
                        "Ambient-Only GNN: The same GNN architecture trained exclusively on meteorological variables—no fire inputs—to estimate background PM₂.₅ driven purely by weather patterns."
                    ),
                ], className="card-list"),
                html.P(
                    "Graph Construction & Temporal Encoding: Stations are treated as graph nodes connected by spatial proximity edges; each model ingests fixed‐length temporal windows (e.g., past 6 hours) to capture persistence and trends.",
                    className="card-text"
                ),
                html.P(
                    "Optimization & Evaluation: Both networks minimize mean squared error with Adam (LR = 1e-3, batch = 32) over 100 epochs; performance is compared via RMSE and R², with the Total model notably outperforming during major wildfire events.",
                    className="card-text"
                ),
            ], className="info-card"),
        ], className="container"),
        className="section section--light"
    ),
])