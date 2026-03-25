import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

df1 = pd.read_csv('./datasets/Fireball_And_Bolide_Reports_rows.csv')
df2 = pd.read_csv('./datasets/Meteorite_Landings.csv')

# Type column for easy filtering
df1['Type'] = 'Fireball/Bolide'
df2['Type'] = 'Meteorite'

# Data Cleaning for df1 (Fireballs & Bolides)
def convert_latitude(lat_str):
    if pd.isna(lat_str): return np.nan
    lat_str = str(lat_str).strip().upper()
    
    if lat_str.endswith("N"):
        return float(lat_str[:-1])
    elif lat_str.endswith("S"):
        return -float(lat_str[:-1])
    else:
        try: # Trying if pure number cases are founnd
            return float(lat_str)
        except ValueError:
            return np.nan

def convert_longitude(lon_str):
    if pd.isna(lon_str): return np.nan
    lon_str = str(lon_str).strip().upper()
    
    if lon_str.endswith("E"):
        return float(lon_str[:-1])
    elif lon_str.endswith("W"):
        return -float(lon_str[:-1])
    else: 
        try:
            return float(lon_str)
        except ValueError:
            return np.nan

# conversion of latitudes in format of data in CSV
df1['Latitude'] = df1['Latitude (Deg)'].apply(convert_latitude) 
df1['Longitude'] = df1['Longitude (Deg)'].apply(convert_longitude)

df1['GeoLocation'] = '(' + df1['Latitude'].astype(str) + ', ' + df1['Longitude'].astype(str) + ')'

# Convert columns to floating numbers for easy calculation
cols_to_numeric_df1 = [
    'Altitude (km)', 'Velocity (km/s)', 
    'Velocity Components (km/s): vx',
    'Velocity Components (km/s): vy', 
    'Velocity Components (km/s): vz'
]

for column in cols_to_numeric_df1:
    if column in df1.columns:
        df1[column] = pd.to_numeric(df1[column], errors='coerce')

# Convert Date/Time
df1['Date/Time - Peak Brightness (UT)'] = pd.to_datetime(
    df1['Date/Time - Peak Brightness (UT)'], 
    format='mixed',
    errors='coerce' 
)

# Data Cleaning for df2 containing Meteorite Landings
df2['Latitude'] = pd.to_numeric(df2['reclat'], errors='coerce')
df2['Longitude'] = pd.to_numeric(df2['reclong'], errors='coerce')

cols_to_numeric_df2 = ['id', 'mass (g)', 'year']
for column in cols_to_numeric_df2:
    if column in df2.columns:
        df2[column] = pd.to_numeric(df2[column], errors='coerce')

# Merging the Datasets df1 and df2
df = pd.concat([df1, df2], ignore_index=True)

# Preview the result
# print(df[['Type', 'Latitude', 'Longitude', 'GeoLocation']].sample(5))
