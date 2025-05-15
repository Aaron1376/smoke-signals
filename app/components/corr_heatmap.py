from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
from google.cloud import bigquery
from dash import Dash

# BigQuery Config
PROJECT_ID = "smoke-signals-pmgnn-457202"  # Replace with your project ID
DATASET = "timeseries"  # Replace with your dataset
TABLE_METEOROLOGICAL = "meteorlogical_data"
TABLE_LOCATIONS = "locations"
TABLE_MAP = "location_map"

# Initialize BigQuery client
bq_client = bigquery.Client()

# Cache
_corr_data_cache = None

# Load data from BigQuery
def load_corr_data():
    global _corr_data_cache
    if _corr_data_cache is not None:
        return _corr_data_cache

    print("Loading correlation data from BigQuery...")

    # Load locations dropdown
    locations_query = f"""
        SELECT label, value
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_LOCATIONS}`
        ORDER BY label
    """
    locations_df = bq_client.query(locations_query).to_dataframe()
    locations = locations_df.to_dict(orient="records")

    # Load location_id → city_name map
    map_query = f"""
        SELECT location_id, city_name
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_MAP}`
    """
    map_df = bq_client.query(map_query).to_dataframe()
    location_map = dict(zip(map_df['location_id'], map_df['city_name']))

    # Load meteorological data
    meteo_query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_METEOROLOGICAL}`
    """
    meteo_df = bq_client.query(meteo_query).to_dataframe()

    _corr_data_cache = (locations, location_map, meteo_df)
    return _corr_data_cache

# Layout function for correlation heatmap
def layout_corr_heatmap():
    locations, _, _ = load_corr_data()
    return html.Div([
        html.H2("PM2.5 vs. Meteorology Correlation Heatmap", style={"textAlign": "center"}),

        html.Div([
            html.Label("Select Monitoring Site:", style={'marginRight': '10px'}),
            dcc.Dropdown(
                id='corr-heatmap-location-dropdown',
                options=locations,
                value=locations[0]['value'] if locations else None,
                clearable=False,
                style={'width': '300px', 'display': 'inline-block', 'marginRight': '20px'}
            ),
        ], style={'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),

        dcc.Loading(
            id="loading-corr-heatmap-graph",
            type="circle",
            children=dcc.Graph(id='corr-heatmap-graph', style={'height': '80vh'})
        )
    ])

# Callback for updating the correlation heatmap
@callback(
    Output('corr-heatmap-graph', 'figure'),
    Input('corr-heatmap-location-dropdown', 'value'),
)
def update_corr_heatmap(selected_location_idx):
    if not selected_location_idx:
        return go.Figure().update_layout(title="Please select a location")

    locations, location_map, meteo_df = load_corr_data()

    # Fixed date range
    start_date = "2021-01-13"
    end_date = "2021-12-30"

    # Filter data for the selected location and fixed date range
    location_label = location_map.get(selected_location_idx, f"Location_Index_{selected_location_idx}")
    filtered_df = meteo_df[
        (meteo_df['location_id'] == selected_location_idx) &
        (meteo_df['timestamp'] >= start_date) &
        (meteo_df['timestamp'] <= end_date)
    ]
    print(f"Filtered data: {filtered_df.shape[0]} rows")

    if filtered_df.empty:
        return go.Figure().update_layout(title="No data available for the selected location")

    # Calculate correlation matrix
    feature_columns = [col for col in filtered_df.columns if col not in ['timestamp', 'location_id', 'city_name']]
    corr_matrix = filtered_df[feature_columns].corr()

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=feature_columns,
        y=feature_columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        colorbar=dict(title='Pearson Corr.')
    ))

    fig.update_layout(
        title=f"PM2.5 vs. Meteorology Correlation - {location_label} ({start_date} to {end_date})",
        xaxis_title="Variable",
        yaxis_title="Variable",
        xaxis_tickangle=-45,
        margin=dict(l=150, r=50, b=150, t=100),
        yaxis_autorange='reversed'
    )

    return fig

    # This script is intended to be used as a Dash app component.
    # To run this file, you need to integrate it into a Dash app.

if __name__ == "__main__":

        app = Dash(__name__)
        app.layout = layout_corr_heatmap()

        app.run(debug=True)