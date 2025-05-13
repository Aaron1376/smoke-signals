from utils import get_npy_from_gcs
from google.cloud import storage
from pathlib import Path
import pandas as pd
import numpy as np
import os
import psutil

# --- Configuration ---
PROJ_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJ_ROOT / "data"
PROC_DATA_DIR = DATA_DIR / "processed"
LOCATIONS_FILE = PROC_DATA_DIR / "locations-names.csv"
OUTPUT_CSV_FILE = PROC_DATA_DIR / "time_series_data.csv"  # Local CSV file path
BUCKET_NAME = "smoke-signal-bucket"
CSV_BLOB_NAME = "processed/time_series_data.csv"  # Path in the bucket

PREDICT_NET_FILE = get_npy_from_gcs(BUCKET_NAME, "pm25gnn/predict.npy")
PREDICT_AMBIENT_FILE = get_npy_from_gcs(BUCKET_NAME, "pm25gnn-ambient/predict.npy")
LABEL_FILE = get_npy_from_gcs(BUCKET_NAME, "pm25gnn-ambient/label.npy")
TIME_FILE = get_npy_from_gcs(BUCKET_NAME, "pm25gnn/time.npy")

PRED_LEN = 48  # Prediction length used in training

def log_memory_usage(stage):
    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
    print(f"[{stage}] Memory usage: {memory:.2f} MB")


def load_and_preprocess_data():
    """
    Load and preprocess data for time series analysis.
    Save the resulting DataFrame, locations, and location map to CSV files.
    """
    print("Starting data preprocessing...")
    log_memory_usage("Start of load_and_preprocess_data")

    # Ensure the processed data directory exists
    if not PROC_DATA_DIR.exists():
        PROC_DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {PROC_DATA_DIR}")

    # Load location data
    locations = []
    location_map = {}
    if os.path.exists(LOCATIONS_FILE):
        print(f"Locations file found: {LOCATIONS_FILE}")
        locations_df = pd.read_csv(LOCATIONS_FILE, index_col=0)
        log_memory_usage("After loading locations CSV")

        loc_id_col = 'location_id'
        city_name_col = 'city_name'

        for index, row in locations_df.iterrows():
            loc_index = index
            loc_name = row[city_name_col]
            label = f"{loc_name}"
            locations.append({'label': label, 'value': loc_index})
            location_map[loc_index] = loc_name  # Map location_id to city_name
    else:
        print(f"Locations file not found: {LOCATIONS_FILE}")
        return

    try:
        # Save locations to a CSV file
        locations_csv_file = PROC_DATA_DIR / "locations.csv"
        pd.DataFrame(locations).to_csv(locations_csv_file, index=False)
        print(f"Saved locations to {locations_csv_file}")
    except Exception as e:
        print(f"Error saving locations.csv: {e}")

    try:
        # Save location map to a CSV file
        location_map_csv_file = PROC_DATA_DIR / "location_map.csv"
        pd.DataFrame(list(location_map.items()), columns=['location_id', 'city_name']).to_csv(location_map_csv_file, index=False)
        print(f"Saved location map to {location_map_csv_file}")
    except Exception as e:
        print(f"Error saving location_map.csv: {e}")

    # Preprocess .npy data
    min_len = min(PREDICT_NET_FILE.shape[0], PREDICT_AMBIENT_FILE.shape[0], LABEL_FILE.shape[0], TIME_FILE.shape[0])
    predict_net_data_trunc = PREDICT_NET_FILE[:min_len]
    predict_ambient_data_trunc = PREDICT_AMBIENT_FILE[:min_len]
    label_data_trunc = LABEL_FILE[:min_len]
    time_data_trunc = TIME_FILE[:min_len]
    log_memory_usage("After truncating .npy files")

    predict_net_actual = predict_net_data_trunc[:, -PRED_LEN:, :, 0].reshape(-1, predict_net_data_trunc.shape[-2])
    predict_ambient_actual = predict_ambient_data_trunc[:, -PRED_LEN:, :, 0].reshape(-1, predict_ambient_data_trunc.shape[-2])
    label_actual = label_data_trunc[:, -PRED_LEN:, :, 0].reshape(-1, label_data_trunc.shape[-2])
    time_data_processed = np.repeat(time_data_trunc, PRED_LEN)
    log_memory_usage("After reshaping .npy data")

    time_data_dt = pd.to_datetime(time_data_processed, unit='s')

    # Combine into a DataFrame
    df_list = []
    for data_loc_idx in range(predict_net_actual.shape[1]):
        loc_df = pd.DataFrame({
            'timestamp': time_data_dt,
            'location_id': data_loc_idx,
            'city_name': location_map.get(data_loc_idx, "Unknown"),  # Add city_name
            'observed': label_actual[:, data_loc_idx],
            'predicted_net': predict_net_actual[:, data_loc_idx],
            'predicted_ambient': predict_ambient_actual[:, data_loc_idx]
        })
        df_list.append(loc_df)

    df = pd.concat(df_list, ignore_index=True)
    df['fire_specific'] = df['predicted_net'] - df['predicted_ambient']
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    log_memory_usage("After creating DataFrame")

    try:
        # Save DataFrame to CSV
        df.to_csv(OUTPUT_CSV_FILE, index=False)
        print(f"Saved DataFrame to {OUTPUT_CSV_FILE}")
    except Exception as e:
        print(f"Error saving time_series_data.csv: {e}")

    print("Data preprocessing complete.")
