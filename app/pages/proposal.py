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
        className="hero hero--primary"
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
])
