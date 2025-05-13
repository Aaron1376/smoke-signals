# home.py
import dash
from dash import html

dash.register_page(__name__, path="/", name="Home")

layout = html.Div([
    # Hero Section
    html.Section(
        html.Div([
            html.H1("Smoke Signals", className="hero-title"),
            html.H2("Time Series Forecasting of PM2.5 Amid California Wildfires", className="hero-subtitle"),
            html.P(
                "Using Historical PM2.5 and Meteorological data to predict PM2.5 levels during California's wildfire seasons.",
                className="hero-text"
            ),
        ], className="container"),
        className="hero hero--primary"
    ),

    # Info Cards Section
    html.Section(
        html.Div([
            html.Div([
                # PM2.5 Card
                html.Div([
                    html.H3("What is PM2.5?"),
                    html.P(
                        "PM2.5 refers to fine particulate matter that is 2.5 micrometers or smaller in diameter. "
                        "These particles can pose serious health risks when inhaled."
                    ),
                ], className="info-card info-card--yellow"),
                
                # Wildfire Card
                html.Div([
                    html.H3("Wildfires & PM2.5"),
                    html.P(
                        "Wildfires release large amounts of PM2.5 into the atmosphere, significantly impacting air quality and public health. "
                        "Preparing for and managing wildfire smoke is crucial for minimizing these effects."
                    ),
                ], className="info-card info-card--green"),
            ], className="info-cards-grid"),
        ], className="container"),
        className="section section--light"
    ),

    # Health Effects Section
    html.Section(
        html.Div([
            html.H2("Health Effects of PM2.5", className="section-title"),
            html.Div(
                html.Img(
                    src="/assets/pm25healtheffects.webp",
                    alt="Health Effects of PM2.5",
                    className="full-width-image"
                ),
                className="image-container"
            ),
        ], className="container"),
        className="section section--white"
    ),

    # Emissions Data Section
    html.Section(
        html.Div([
            html.H2("Wildfire PM2.5 Emissions", className="section-title"),
            html.Div([
                html.Img(
                    src="/assets/wildfirepm2.5_emissions.jpg",
                    alt="Wildfire PM2.5 Emissions",
                    className="full-width-image"
                ),
                html.P(
                    "Graph provided by California Air Resources Board.",
                    className="image-caption"
                ),
            ], className="image-container"),
        ], className="container"),
        className="section section--light"
    ),

    # Map Section
    html.Section(
        html.Div([
            html.H2("PM2.5 Monitoring Sites in California", className="section-title"),
            html.Div(
                html.Iframe(
                    src="/assets/location_map.html",
                    className="map-frame"
                ),
                className="map-container"
            ),
        ], className="container"),
        className="section section--white"
    ),

    # CTA Section
    html.Section(
        html.Div([
            html.H2("Ready to Explore the Data?", className="cta-title"),
            html.Div([
                html.A("View Findings →", href="/analytics", className="btn btn--primary"),
                html.A("Research Objectives →", href="/proposal", className="btn btn--secondary"),
            ], className="cta-buttons"),
        ], className="container"),
        className="section section--cta"
    ),
])
