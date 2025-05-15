# analytics.py

import dash
from dash import html, dcc
from components.time_series import layout_time_series
# from components.graphs import chi_square_df, create_lollipop_chart, dash_table


dash.register_page(__name__, path="/analytics", name="Findings")

def create_findings_box(findings):
    """Helper function to create consistent findings boxes"""
    return html.Div([
        html.H4("Key Findings", style={'color': '#2C5282', 'marginBottom': '10px'}),
        html.Ul(findings, style={'paddingLeft': '20px', 'fontSize': '15px', 'color': '#4A5568'})
    ], className="findings-box")

# Create the chi-square analysis section with tabs and Random Forest chart
def layout_chi_square():
    return html.Div([
        html.H3("Feature Significance Analysis", style={"textAlign": "center"}),

        # Tabs for Chi-Square Table and Lollipop Chart
        dcc.Tabs([
            dcc.Tab(label="Chi-Square Table", children=[
                html.Div([
                    html.H4("Chi-Square Table", style={"textAlign": "center", "marginTop": "2rem"}),
                    html.Iframe(
                        src="/assets/chi_square_table.html",  # Path to the saved HTML file
                        style={"width": "100%", "height": "600px", "border": "none"}  # Adjust height as needed
                    )
                ], style={
                    "padding": "2rem",
                    "backgroundColor": "#f9f9f9",
                    "border": "1px solid #ddd",
                    "borderRadius": "8px",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
                    "margin": "2rem auto",
                    "maxWidth": "95%"
                })
            ]),
            dcc.Tab(label="Lollipop Chart", children=[
                html.Div([
                    html.H4("Lollipop Chart", style={"textAlign": "center", "marginTop": "2rem"}),
                    html.Iframe(
                        src="/assets/lollipop_chart.html",  # Path to the saved HTML file
                        style={"width": "100%", "height": "600px", "border": "none"}  # Adjust height as needed
                    )
                ], style={
                    "padding": "2rem",
                    "backgroundColor": "#f9f9f9",
                    "border": "1px solid #ddd",
                    "borderRadius": "8px",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
                    "margin": "2rem auto",
                    "maxWidth": "95%"
                })
            ])
        ], style={
            "margin": "1rem 0",
            "fontFamily": "'Helvetica Neue', Arial, sans-serif"
        }),

        # Random Forest Feature Importance Chart
        html.Div([
            html.H4("Random Forest Feature Importance", style={"textAlign": "center", "marginTop": "2rem"}),
            html.Img(
                src="/assets/RandomForest.png",  # Path to the saved image
                style={"width": "100%", "height": "600px", "objectFit": "contain", "border": "none"}  # Adjust size as needed
            )
        ], style={
            "padding": "2rem",
            "backgroundColor": "#f9f9f9",
            "border": "1px solid #ddd",
            "borderRadius": "8px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
            "margin": "2rem auto",
            "maxWidth": "95%"
        })
    ], className="chi-square-analysis-box")

# Add Chico-Yuba Comparison Visualization
def layout_chico_yuba_comparison():
    return html.Div([
        html.H3("Urban vs Rural", style={"textAlign": "center", "marginTop": "2rem"}),
        html.Div([
            html.Iframe(
                src="/assets/chico_yuba_comparison.html",  # Path to the HTML file in the assets folder
                style={"width": "100%", "height": "800px", "border": "none"}  # Increased height to 800px
            )
        ], style={
            "padding": "2rem",  # Increased padding for better spacing
            "backgroundColor": "#f9f9f9",
            "border": "1px solid #ddd",
            "borderRadius": "8px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",  # Slightly larger shadow for emphasis
            "margin": "2rem auto",  # Increased margin for better spacing
            "maxWidth": "95%"  # Increased maxWidth to make the box wider
        })
    ], className="chico-yuba-comparison-box")

# Update the main layout
layout = html.Div([
    # Dashboard Title
    html.Div([
        html.H1("Analytics Dashboard", 
                className="dashboard-title",
                style={
                    "backgroundColor": "#3A5311",
                    "color": "white",
                    "padding": "1rem",
                    "margin": "0"
                })
    ]),
    
    # Main Content Container
    html.Div([
        # Key Findings Overview Section (kept at top)
        html.Div([
            html.Div([
                create_findings_box([
                    html.Li([html.Strong("Fire Counts: "), 
                            "Exhibited the strongest association with PM₂.₅ levels in both chi-square and Random Forest analyses."]),
                    html.Li([html.Strong("Julian Date: "), 
                            "Showed a significant seasonal relationship with PM₂.₅ variability."]),
                    html.Li([html.Strong("Surface Pressure: "), 
                            "Demonstrated a robust correlation with PM₂.₅ concentrations."]),
                    html.Li([html.Strong("Boundary Layer Height: "), 
                            "Significantly influenced pollutant dispersion and PM₂.₅ readings."]),
                    html.Li([html.Strong("Fire Radiative Power: "), 
                            "Metrics (e.g., 500 km IDW) showed moderate significance but less impact than fire counts and seasonality."]),
                    html.Li([html.Strong("Wind Speed and Precipitation: "), 
                            "Had minimal statistical significance for PM₂.₅ prediction."])
                ])
            ], className="content-box")
        ], className="dashboard-section"),

        # Analysis Sections Container
        html.Div([
            # Chi-Square Analysis
            html.Div([
                html.Div([
                    layout_chi_square()
                ], className="content-box")
            ], className="dashboard-section"),

            # Chico-Yuba Comparison Visualization
            html.Div([
                layout_chico_yuba_comparison()
            ], className="dashboard-section"),

            # Time Series Analysis
            html.Div([
                html.H2("Time Series Analysis", className="section-title"),
                html.Div([
                    html.Div([
                        layout_time_series(),
                    ], className="content-box")
                ], className="analysis-box")
            ], className="dashboard-section"),

            # Research Conclusions
            html.Div([
                html.H2("Research Conclusions", className="section-title"),
                html.Div([
                    html.Div([
                        html.P("Based on our comprehensive analysis of PM2.5 levels during California wildfire seasons:", 
                               className="conclusion-text"),
                        html.Ul([
                            html.Li("Strong correlation between meteorological conditions and air quality"),
                            html.Li("Temporal patterns indicate predictable air quality deterioration"),
                            html.Li("Geographic location significantly influences PM2.5 exposure levels"),
                            html.Li("Statistical evidence supports the impact of multiple environmental factors"),
                            html.Li("Data suggests the need for region-specific air quality management strategies")
                        ], className="conclusion-list")
                    ], className="content-box")
                ], className="analysis-box")
            ], className="dashboard-section")
        ], className="dashboard-container")
    ], className="main-content")
])
