import os
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
from google.cloud import bigquery


# BigQuery Config
PROJECT_ID = "smoke-signals-pmgnn-457202"  # Replace with your project ID
DATASET = "timeseries"        # Replace with your dataset
TABLE_TS = "time_series_data"
TABLE_LOCATIONS = "locations"
TABLE_MAP = "location_map"

# Initialize BigQuery client
bq_client = bigquery.Client()

# Cache
_data_cache = None

# Load locations and location map from BigQuery
def load_data():
    global _data_cache
    if _data_cache is not None:
        return _data_cache

    print("Loading data from BigQuery...")

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

    print("Loading timestamp bounds...")
    bounds_query = f"""
        SELECT MIN(timestamp) AS min_date, MAX(timestamp) AS max_date
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_TS}`
    """
    bounds_df = bq_client.query(bounds_query).to_dataframe()
    min_date, max_date = pd.to_datetime(bounds_df['min_date'][0]), pd.to_datetime(bounds_df['max_date'][0])

    _data_cache = (locations, location_map, min_date, max_date)
    return _data_cache


# Load cached data
locations, location_map, min_date, max_date = load_data()

# Layout function
def layout_time_series():
    return html.Section(
      html.Div([
        html.H2("PM2.5 Time Series Analysis", style={"textAlign": "center"}),
        html.Div([
          html.Div([
            html.Label("Site:", style={'marginRight':'10px'}),
            dcc.Dropdown(
              id='location-dropdown',
              options=locations,
              value=locations[0]['value'] if locations else None,
              clearable=False,
              style={'width':'250px'}
            )
          ], style={'display':'inline-block','marginRight':'20px'}),
          html.Div([
            html.Label("Date Range:"),
            dcc.DatePickerRange(
              id='date-picker-range',
              min_date_allowed=min_date,
              max_date_allowed=max_date,
              start_date=min_date,
              end_date=max_date,
              display_format='YYYY-MM-DD'
            )
          ], style={'display':'inline-block'})
        ], style={'textAlign':'center','marginBottom':'1rem'}),
        html.Div([
          html.Label("Show:", style={'marginRight':'10px'}),
          dcc.Checklist(
            id='data-checklist',
            options=[
              {'label':'Observed','value':'observed'},
              {'label':'Predicted Net','value':'predicted_net'},
              {'label':'Predicted Ambient','value':'predicted_ambient'},
              {'label':'Fire-specific','value':'fire_specific'},
            ],
            value=['observed','predicted_net'],
            inline=True,
            labelStyle={'marginRight':'15px'}
          )
        ], style={'textAlign':'center','marginBottom':'1rem'}),
        dcc.Loading(dcc.Graph(id='pm25-time-series-graph'))
      ], className="container"),
      className="container"
    )


# Callback for dynamic query
@callback(
    Output('pm25-time-series-graph', 'figure'),
    Input('location-dropdown', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('data-checklist', 'value'),
)
def update_ts(site, start, end, series):
    if not site:
        return go.Figure().update_layout(title="Select a site")

    query = f"""
        SELECT timestamp, observed, predicted_net, predicted_ambient, fire_specific
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_TS}`
        WHERE location_id = @site
          AND timestamp BETWEEN @start AND @end
        ORDER BY timestamp
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("site", "INT64", site),
            bigquery.ScalarQueryParameter("start", "TIMESTAMP", start),
            bigquery.ScalarQueryParameter("end", "TIMESTAMP", end),
        ]
    )

    df2 = bq_client.query(query, job_config=job_config).to_dataframe()
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])

    if df2.empty:
        return go.Figure().update_layout(title="No data")

    fig = go.Figure()
    label = location_map.get(site, site)

    if 'observed' in series:
        fig.add_trace(go.Scatter(x=df2.timestamp, y=df2.observed, mode='lines', name='Observed'))
    if 'predicted_net' in series:
        fig.add_trace(go.Scatter(x=df2.timestamp, y=df2.predicted_net, mode='lines', name='Predicted Net'))
    if 'predicted_ambient' in series:
        fig.add_trace(go.Scatter(x=df2.timestamp, y=df2.predicted_ambient, mode='lines', name='Pred Ambient'))
    if 'fire_specific' in series:
        fig.add_trace(go.Scatter(x=df2.timestamp, y=df2.fire_specific, mode='lines', name='Fire-specific'))

    fig.update_layout(title=f"PM2.5 @ {label}", xaxis_title="Time", yaxis_title="µg/m³", hovermode='x')
    return fig
    
    
  