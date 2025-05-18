"""Module to convert NPY to CSV."""

from pathlib import Path

import numpy as np
import pandas as pd

PROJ_ROOT = Path(__file__).resolve().parent
DATA_DIR = Path("/data/smoke-signals")
RAWD_DIR = DATA_DIR / "raw"
PROCD_DIR = DATA_DIR / "processed"

DATASET_FILE = RAWD_DIR / "dataset_fire_wind_aligned.npy"
OUTPUT_NP_FILE = PROCD_DIR / 'dataset_file_wind_aligned_np.csv'
OUTPUT_PD_FILE = PROCD_DIR / 'dataset_file_wind_aligned_PD_timestamps.csv'
FEATURE_NAMES = [
    '100m_u_component_of_wind',
    '100m_v_component_of_wind',
    '2m_dewpoint_temperature',
    '2m_temperature',
    'boundary_layer_height',
    'total_precipitation',
    'surface_pressure',
    'u_component_of_wind+950',
    'v_component_of_wind+950',
    'frp_25km_idw',
    'frp_50km_idw',
    'frp_100km_idw',
    'frp_500km_idw',
    'fire_num',
    'interp_flag',
    'julian_date',
    'time_of_day',
    "pm25_known"
]

import numpy as np
import pandas as pd

# --- Assume you have loaded your .npy file ---
npy_file_path = DATASET_FILE
data_3d = np.load(npy_file_path) # Shape: (43816, 112, 18)
# ---------------------------------------------
# For demonstration, let's create a dummy data_3d with the correct shape
num_total_timesteps_3d = data_3d.shape[0]
num_monitors = data_3d.shape[1]
num_features = data_3d.shape[2]
# data_3d = np.random.rand(num_total_timesteps_3d, num_monitors, num_features)
# ---------------------------------------------

# Reshape
data_2d = data_3d.reshape(-1, num_features)

# Create identifier columns
original_timestep_indices = np.repeat(np.arange(num_total_timesteps_3d), num_monitors)
original_monitor_indices = np.tile(np.arange(num_monitors), num_total_timesteps_3d)

# Confirmed metadata
actual_start_datetime = pd.Timestamp(year=2017, month=1, day=1, hour=1, minute=0, tz='GMT')
hourly_interval = pd.Timedelta(hours=1)

# Calculate actual timestamps for each row
actual_timestamps_column = actual_start_datetime + original_timestep_indices * hourly_interval

# Create DataFrame
feature_names = FEATURE_NAMES
df = pd.DataFrame(data_2d, columns=feature_names)

# Insert the identifier and timestamp columns
df.insert(0, 'actual_timestamp_gmt', actual_timestamps_column)
df.insert(0, 'original_monitor_id', original_monitor_indices)
df.insert(0, 'original_timestep_index', original_timestep_indices) # Optional, as timestamp is more direct

# Display first few rows to check
print("\nDataFrame with Timestamps (first 5 rows):")
print(df.head())

# Display last few rows to check
print("\nDataFrame with Timestamps (last 5 rows):")
print(df.tail())

# Now you can save this DataFrame to CSV
csv_output_path = OUTPUT_PD_FILE
df.to_csv(csv_output_path, index=False, float_format='%.18g') # Using a specific float format
print(f"\nSaved DataFrame with timestamps to {csv_output_path}")