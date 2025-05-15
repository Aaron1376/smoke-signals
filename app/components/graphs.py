import pandas as pd
from dash import Dash, html, dash_table, dcc
from scipy.stats import chi2_contingency
from google.cloud import bigquery
import plotly.graph_objects as go
import plotly.io as pio  # For saving Plotly figures to HTML

# BigQuery Config
PROJECT_ID = "smoke-signals-pmgnn-457202"  # Replace with your project ID
DATASET = "timeseries"        # Replace with your dataset
TABLE_METEOROLOGICAL = "meteorlogical_data"  # Replace with your table name

# Initialize BigQuery client
bq_client = bigquery.Client()

# Cache
_data_cache = None

# Load the updated dataset from BigQuery
def load_updated_data():
    global _data_cache
    if _data_cache is not None:
        print("Using cached data.")
        return _data_cache

    print("Loading updated data from BigQuery...")

    # Query to fetch data
    query = f"""
        SELECT 
            `100m_u_component_of_wind` AS u_wind_100m,
            `100m_v_component_of_wind` AS v_wind_100m,
            `2m_dewpoint_temperature` AS dewpoint_temp_2m,
            `2m_temperature` AS temp_2m,
            boundary_layer_height,
            total_precipitation,
            surface_pressure,
            `u_component_of_wind+950` AS u_wind_950,
            `v_component_of_wind+950` AS v_wind_950,
            frp_25km_idw,
            frp_50km_idw,
            frp_100km_idw,
            frp_500km_idw,
            fire_num,
            interp_flag,
            julian_date,
            time_of_day,
            AQI_Category
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_METEOROLOGICAL}`
        WHERE AQI_Category IS NOT NULL
    """
    # Execute the query and fetch the data
    df = bq_client.query(query).to_dataframe()
    print(f"Loaded {len(df)} rows of data.")

    # Cache the data
    _data_cache = df
    return df


# Load the data
df = load_updated_data()

# Discretize continuous features into bins
def discretize_feature(feature, bins=5):
    return pd.cut(feature, bins=bins, labels=[f"Bin_{i}" for i in range(1, bins + 1)])

# List of features to analyze
features = [
    "u_wind_100m", "v_wind_100m", "dewpoint_temp_2m", "temp_2m",
    "boundary_layer_height", "total_precipitation", "surface_pressure",
    "u_wind_950", "v_wind_950", "frp_25km_idw", "frp_50km_idw",
    "frp_100km_idw", "frp_500km_idw", "fire_num", "interp_flag",
    "julian_date", "time_of_day"
]

# Perform chi-square analysis
chi_square_results = []

for feature in features:
    # Discretize the feature
    df[f"{feature}_binned"] = discretize_feature(df[feature], bins=5)
    
    # Create a contingency table
    contingency_table = pd.crosstab(df[f"{feature}_binned"], df["AQI_Category"])
    
    # Perform chi-square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    
    # Store the results
    chi_square_results.append({
        "Feature": feature,
        "Chi-Square Value": round(chi2, 2),
        "P-Value": round(p, 5),
        "Statistically Significant?": "Yes" if p < 0.05 else "No"
    })

# Convert results to a DataFrame
chi_square_df = pd.DataFrame(chi_square_results)

# Save the table to HTML using Pandas
def save_table_to_html(df, filename="chi_square_table.html"):
    print(f"Saving chi-square table to {filename}...")
    try:
        # Convert the DataFrame to an HTML table
        html_table = df.to_html(
            index=False,  # Do not include the index
            classes="table table-striped",  # Add Bootstrap classes for styling
            border=0  # No border
        )
        # Write the HTML table to a file
        with open(filename, "w") as f:
            f.write(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
                <title>Chi-Square Table</title>
            </head>
            <body>
                <div class="container mt-4">
                    <h1 class="text-center">Chi-Square Analysis Results</h1>
                    {html_table}
                </div>
            </body>
            </html>
            """)
        print(f"Table saved to {filename}.")
    except Exception as e:
        print(f"Error saving table to HTML: {e}")

# Save the lollipop chart to HTML
def save_lollipop_chart_to_html(fig, filename="lollipop_chart.html"):
    print(f"Saving lollipop chart to {filename}...")
    pio.write_html(fig, file=filename, auto_open=False)
    print(f"Lollipop chart saved to {filename}.")

# Create the lollipop chart
def create_lollipop_chart(chi_square_df):
    print("Creating lollipop chart for chi-square analysis...")
    
    # Sort the DataFrame by Chi-Square Value in descending order
    chi_square_df = chi_square_df.sort_values(by="Chi-Square Value", ascending=False)
    
    # Create the lollipop chart
    fig = go.Figure()

    # Add the "stick" part of the lollipop
    fig.add_trace(go.Scatter(
        x=chi_square_df["Chi-Square Value"],
        y=chi_square_df["Feature"],
        mode="lines+markers",
        line=dict(color="gray", width=1),
        marker=dict(size=10, color="blue"),
        name="Chi-Square Value"
    ))

    # Add the "circle" part of the lollipop
    fig.add_trace(go.Scatter(
        x=chi_square_df["Chi-Square Value"],
        y=chi_square_df["Feature"],
        mode="markers",
        marker=dict(size=15, color="blue", symbol="circle"),
        name="Feature"
    ))

    # Update layout for better visualization
    fig.update_layout(
        title="Lollipop Chart for Chi-Square Analysis",
        xaxis_title="Chi-Square Value",
        yaxis_title="Feature",
        yaxis=dict(autorange="reversed"),  # Reverse the y-axis for better readability
        template="plotly_white",
        height=600,
        width=800
    )

    return fig

# # Save the results
# save_table_to_html(chi_square_df, filename="chi_square_table.html")
# lollipop_chart = create_lollipop_chart(chi_square_df)
# save_lollipop_chart_to_html(lollipop_chart, filename="lollipop_chart.html")

# Uncomment the following code to include Random Forest functionality
# # Prepare the data for Random Forest
# def prepare_data(df):
#     # Drop rows with missing values
#     df = df.dropna()

#     # Define features (X) and target (y)
#     X = df.drop(columns=["AQI_Category"])
#     y = df["AQI_Category"]

#     return train_test_split(X, y, test_size=0.2, random_state=42)

# X_train, X_test, y_train, y_test = prepare_data(df)

# # Train a GPU-accelerated Random Forest model
# def train_random_forest_gpu(X_train, y_train):
#     print("Training GPU-accelerated Random Forest model...")
#     rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
#     rf.fit(X_train, y_train)
#     return rf

# rf_model = train_random_forest_gpu(X_train, y_train)

# # Evaluate the model
# def evaluate_model(rf_model, X_test, y_test):
#     print("Evaluating the model...")
#     y_pred = rf_model.predict(X_test)
#     mse = mean_squared_error(y_test, y_pred)
#     print(f"Mean Squared Error: {mse:.2f}")
#     return mse

# mse = evaluate_model(rf_model, X_test, y_test)

# # Display feature importance
# Display feature importance
# def plot_feature_importance(rf_model, feature_names):
#     print("Plotting feature importance...")
#     # Correct attribute name for feature importance
#     importance = rf_model.feature_importances_
#     importance_df = pd.DataFrame({
#         "Feature": feature_names,
#         "Importance": importance
#     }).sort_values(by="Importance", ascending=False)

#     fig = px.bar(
#         importance_df,
#         x="Importance",
#         y="Feature",
#         orientation="h",
#         title="Feature Importance",
#         labels={"Importance": "Importance Score", "Feature": "Features"}
#     )
#     fig.update_layout(yaxis=dict(autorange="reversed"))
#     fig.show()

# # Call the function with the correct feature names
# fig = plot_feature_importance(rf_model, X_train.columns)



