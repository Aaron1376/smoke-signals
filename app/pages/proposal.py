# proposal.py
import dash
from dash import html

dash.register_page(__name__, path="/proposal", name="Proposal")

layout = html.Div([
    # Hero Section
    html.Section(
        html.Div([
            html.H1("Project Proposal", className="hero-title"),
            html.P(
                "This project aims to create reliable time series forecasting models to accurately predict hourly PM2.5 levels during California's wildfire seasons. "
                "By analyzing historical air quality data, meteorological conditions, and wildfire events, we aim to provide actionable insights and improve early warning systems.",
                className="hero-text"
            ),
        ], className="container"),
        className="hero hero--tertiary"
    ),

    # Objectives Section
    html.Section(
        html.Div([
            html.H2("Research Objectives", className="section-title"),
            html.Div([
                html.Div([
                    html.H3("Primary Goals", className="card-title"),
                    html.Ul([
                        html.Li("Analyze seasonal and temporal trends in PM2.5 concentrations"),
                        html.Li("Identify key meteorological and wildfire-related drivers of PM2.5 levels"),
                        html.Li("Develop advanced forecasting models for early warning systems"),
                    ], className="card-list")
                ], className="info-card")
            ], className="cards-grid"),
        ], className="container"),
        className="section section--light"
    ),

    # Broader Impacts Section
    html.Section(
        html.Div([
            html.H2("Broader Impacts", className="section-title"),
            html.Div([
                html.Div([
                    html.H3("Community Benefits", className="card-title"),
                    html.Ul([
                        html.Li("Provide accurate PM2.5 forecasts for sensitive communities"),
                        html.Li("Influence policies on land management and fire prevention strategies"),
                        html.Li("Highlight the impact of wildfires on air quality"),
                        html.Li("Support public health initiatives by identifying high-risk areas"),
                    ], className="card-list")
                ], className="info-card")
            ], className="cards-grid"),
        ], className="container"),
        className="section section--white"
    ),

    # Data Sources Section
    html.Section(
        html.Div([
            html.H2("Data Sources", className="section-title"),
            html.Div([
                html.Div([
                    html.H3("Primary Sources", className="card-title"),
                    html.Ul([
                        html.Li("United States Environmental Protection Agency (EPA)"),
                        html.Li("California Air Resources Board (AQMIS)"),
                        html.Li("ERA5 Reanalysis (ECMWF)"),
                        html.Li("National Interagency Fire Center (NIFC)"),
                    ], className="card-list")
                ], className="info-card")
            ], className="cards-grid"),
        ], className="container"),
        className="section section--light"
    ),

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
