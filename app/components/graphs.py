import pandas as pd
from google.cloud import bigquery
from cuml.ensemble import RandomForestRegressor  # GPU-accelerated Random Forest
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import plotly.express as px
from tqdm import tqdm  # Import tqdm for progress tracking

# BigQuery Config
PROJECT_ID = "smoke-signals-pmgnn-457202"  # Replace with your project ID
DATASET = "timeseries"        # Replace with your dataset
TABLE_METEOROLOGICAL = "meteorological_data"  # Replace with your table name

# Initialize BigQuery client
bq_client = bigquery.Client()

# Load meteorological data
def load_meteorological_data():
    print("Loading meteorological data from BigQuery...")
    query = f"""
        SELECT 
            actual_timestamp_gmt,
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
            pm25_known
        FROM `{PROJECT_ID}.{DATASET}.{TABLE_METEOROLOGICAL}`
        WHERE pm25_known IS NOT NULL
    """
    df = bq_client.query(query).to_dataframe()
    print(f"Loaded {len(df)} rows of meteorological data.")
    return df

# Load the data
df = load_meteorological_data()

# Prepare the data for Random Forest
def prepare_data(df):
    # Drop rows with missing values
    df = df.dropna()

    # Define features (X) and target (y)
    X = df.drop(columns=["actual_timestamp_gmt", "pm25_known"])
    y = df["pm25_known"]

    return train_test_split(X, y, test_size=0.2, random_state=42)

X_train, X_test, y_train, y_test = prepare_data(df)

# Train a GPU-accelerated Random Forest model
def train_random_forest_gpu(X_train, y_train):
    print("Training GPU-accelerated Random Forest model...")
    rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    return rf

rf_model = train_random_forest_gpu(X_train, y_train)

# Evaluate the model
def evaluate_model(rf_model, X_test, y_test):
    print("Evaluating the model...")
    y_pred = rf_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")
    return mse

mse = evaluate_model(rf_model, X_test, y_test)

# Display feature importance
def plot_feature_importance(rf_model, feature_names):
    print("Plotting feature importance...")
    importance = rf_model.feature_importances_
    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importance
    }).sort_values(by="Importance", ascending=False)

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Feature Importance",
        labels={"Importance": "Importance Score", "Feature": "Features"}
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.show()

fig = plot_feature_importance(rf_model, X_train.columns)

# Save the plot to an HTML file
def save_plot_to_html(fig, filename="feature_importance.html"):
    print(f"Saving plot to {filename}...")
    fig.write_html(filename)
    print(f"Plot saved successfully to {filename}.")

# Save the feature importance plot
save_plot_to_html(fig)