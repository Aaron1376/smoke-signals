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
                        html.Li("Develop advanced forecasting models to accurately predict hourly PM2.5 levels"),
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
                        html.Li("California Department of Forestry and Fire Protection (CAL FIRE)"),
                    ], className="card-list")
                ], className="info-card")
            ], className="cards-grid"),
        ], className="container"),
        className="section section--light"
    ),

    # Expected Major Findings Section
    html.Section(
        html.Div([
            html.H2("Expected Major Findings", className="section-title"),
            html.Div([
                html.Div([
                    html.H3("Improved Predictive Precision using Spatio-Temporal Model Advancements", className="card-title"),
                    html.P(
                        "With the use of graph neural networks (GNNs), our method should provide better hourly PM2.5 forecasts during wildfire seasons. "
                        "Similar to the gains seen in research linked below, we expect that the GNN's capacity to capture intricate spatial and temporal connections will enhance performance measures like MAE and RMSE, especially for sharp increases in PM2.5 during major wildfire occurrences.",
                        className="card-text"
                    )
                ], className="info-card"),
                html.Div([
                    html.H3("Urban versus Rural Impacts", className="card-title"),
                    html.P(
                        "Due to variations in baseline pollution levels and local topography influencing dispersion, wildfire-induced increases in PM2.5 are more noticeable in urban areas than in rural ones. "
                        "Urban settings may make wildfire smoke buildup worse due to their greater baseline pollution levels and structural effects on airflow.",
                        className="card-text"
                    )
                ], className="info-card"),
                html.Div([
                    html.H3("Weather-Related Factors", className="card-title"),
                    html.P(
                        "Detailed meteorological data (e.g., wind speed and direction, temperature inversions, humidity) will reveal which climatic factors most strongly exacerbate PM2.5 buildup during wildfire events. "
                        "The goal is to demonstrate that certain weather conditions not only correlate but also amplify the impact of wildfire emissions on air quality, thereby refining forecast lead times and accuracy.",
                        className="card-text"
                    )
                ], className="info-card")
            ], className="cards-grid"),
        ], className="container"),
        className="section section--light"
    )
])
