import os
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
from google.cloud import bigquery
from plotly.subplots import make_subplots
import plotly.io as pio


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


def plot_chico_yuba_comparison_side_by_side():
    # Define the location IDs for Chico and Yuba City
    chico_id = 3  # Replace with the actual location_id for Chico
    yuba_city_id = 4  # Replace with the actual location_id for Yuba City

    # Define the date range
    start_date = "2021-07-13"
    end_date = "2021-10-25"

    # Query for Chico
    chico_query = f"""
        SELECT timestamp, observed
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_TS}`
        WHERE location_id = @chico_id
          AND timestamp BETWEEN @start_date AND @end_date
        ORDER BY timestamp
    """
    chico_job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("chico_id", "INT64", chico_id),
            bigquery.ScalarQueryParameter("start_date", "TIMESTAMP", start_date),
            bigquery.ScalarQueryParameter("end_date", "TIMESTAMP", end_date),
        ]
    )
    chico_df = bq_client.query(chico_query, job_config=chico_job_config).to_dataframe()
    chico_df['timestamp'] = pd.to_datetime(chico_df['timestamp'])

    # Query for Yuba City
    yuba_city_query = f"""
        SELECT timestamp, observed
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_TS}`
        WHERE location_id = @yuba_city_id
          AND timestamp BETWEEN @start_date AND @end_date
        ORDER BY timestamp
    """
    yuba_city_job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("yuba_city_id", "INT64", yuba_city_id),
            bigquery.ScalarQueryParameter("start_date", "TIMESTAMP", start_date),
            bigquery.ScalarQueryParameter("end_date", "TIMESTAMP", end_date),
        ]
    )
    yuba_city_df = bq_client.query(yuba_city_query, job_config=yuba_city_job_config).to_dataframe()
    yuba_city_df['timestamp'] = pd.to_datetime(yuba_city_df['timestamp'])

    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,  # One row, two columns
        subplot_titles=(
            "<b>Chico (Observed PM2.5 During Dixie Fire)</b>", 
            "<b>Yuba City (Observed PM2.5 During Dixie Fire)</b>"
        ),
        horizontal_spacing=0.1  # Adjust spacing between the subplots
    )

    # Add Chico data to the first subplot
    if not chico_df.empty:
        fig.add_trace(
            go.Scatter(
                x=chico_df['timestamp'],
                y=chico_df['observed'],
                mode='lines',
                name='Chico (Observed)',
                line=dict(color='blue', width=2),
                fill='none'  # Ensure no fill under the line
            ),
            row=1, col=1
        )

    # Add Yuba City data to the second subplot
    if not yuba_city_df.empty:
        fig.add_trace(
            go.Scatter(
                x=yuba_city_df['timestamp'],
                y=yuba_city_df['observed'],
                mode='lines',
                name='Yuba City (Observed)',
                line=dict(color='green', width=2),
                fill='none'  # Ensure no fill under the line
            ),
            row=1, col=2
        )

    # Update layout
    fig.update_layout(
        title=dict(
            text="<b>Observed PM2.5 Levels: Chico vs Yuba City During Dixie Fire (07/13/2021 - 10/25/2021)</b>",
            x=0.5,  # Center the title
            xanchor="center"
        ),
        template="plotly_white",
        height=600,
        width=1400  # Increased width for a wider graph
    )

    # Customize individual subplot axes
    fig.update_xaxes(
        title_text="Time",
        range=["2021-07-13", "2021-10-25"],  # Explicitly set x-axis range
        row=1, col=1
    )
    fig.update_yaxes(title_text="PM2.5 (µg/m³)", row=1, col=1)
    fig.update_xaxes(
        title_text="Time",
        range=["2021-07-13", "2021-10-25"],  # Explicitly set x-axis range
        row=1, col=2
    )
    fig.update_yaxes(title_text="PM2.5 (µg/m³)", row=1, col=2)

    # # Save the plot to an HTML file
    # output_file = "chico_yuba_comparison.html"
    # pio.write_html(fig, file=output_file, auto_open=True)  # auto_open=True will open the file in a browser

    return fig


# Example usage: Uncomment the following line to save and display the plot
#plot_chico_yuba_comparison_side_by_side()




