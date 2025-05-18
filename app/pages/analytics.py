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
            ),
            html.P(
                "These graphs show that fire activity and seasonality are the dominant drivers of PM₂.₅: in the lollipop chart, fire_num and julian_date have by far the highest chi-square values, indicating the strongest statistical association with PM₂.₅ categories, while in the Random Forest bar chart those same features top the permutation importances, confirming they also contribute most to predictive accuracy. Other meteorological factors—like surface pressure and boundary-layer height—appear significant but secondary, and variables such as wind components and precipitation add comparatively little unique information.",
                style={"textAlign": "center", "marginTop": "1rem", "fontSize": "16px", "color": "#4A5568"}
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

        # Embed the Chico-Yuba Comparison Graph and Comment
        html.Div([
            html.Iframe(
                src="/assets/chico_yuba_comparison.html",  # Path to the HTML file in the assets folder
                style={"width": "100%", "height": "800px", "border": "none"}  # Adjust height as needed
            ),
            html.P(
                "This side-by-side comparison suggests that Yuba City’s more urban environment experienced longer, higher PM₂.₅ elevations—likely because higher baseline pollution and building-induced airflow changes in urban areas trap wildfire smoke more effectively—whereas Chico’s more open, rural setting showed sharper but shorter spikes as smoke dispersed more quickly",
                style={"textAlign": "center", "marginTop": "1rem", "fontSize": "16px", "color": "#4A5568"}
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
    ], className="chico-yuba-comparison-box")

# Update the main layout
layout = html.Div([
    # Dashboard Title
    html.Div([
        html.H1("Analytics Dashboard", 
                className="dashboard-title",
                style={
                    "backgroundColor": "#2E7D32",  # Match the nav bar color
                    "color": "white",
                    "padding": "1rem",
                    "margin": "0",
                    "textAlign": "center"
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
                        layout_time_series()
                    ], className="content-box"),
                    html.P(
                        "Figure: Daily PM₂.₅ at Alpine for 2021—blue shows actual measurements, red the Spatio-Temporal GNN’s total-PM₂.₅ predictions (including fire effects), "
                        "green the ambient-only GNN baseline, and purple the isolated fire-specific PM₂.₅ component—demonstrating that the full model captures observed peaks during wildfire events "
                        "while the ambient forecast stays lower and the fire-specific trace highlights the wildfire contribution.",
                        style={"textAlign": "center", "marginTop": "1rem", "fontSize": "16px", "color": "#4A5568"}
                    )
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
                            html.Li("Fire counts are the strongest single predictor of PM₂.₅, showing the highest chi-square and permutation importance."),
                            html.Li("Day-of-year (julian_date) drives clear seasonal cycles in PM₂.₅ levels."),
                            html.Li("Surface pressure and boundary-layer height both exert significant control over pollutant accumulation."),
                            html.Li("Fire radiative power metrics and temperature variables contribute moderately but less than top features."),
                            html.Li("During the Dixie Fire, Chico saw sharp, short-lived PM₂.₅ spikes while Yuba City experienced more prolonged elevated levels."),
                            html.Li("The Random Forest’s predicted net PM₂.₅ closely follows observed trends but underestimates the most extreme peak events.")
                        ], className="conclusion-list")
                    ], className="content-box")
                ], className="analysis-box")
            ], className="dashboard-section")
        ], className="dashboard-container")
    ], className="main-content")
])
