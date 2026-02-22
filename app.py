import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Load Dataset
df1 = pd.read_csv('./datasets/Fireball_And_Bolide_Reports_rows.csv')
df2 = pd.read_csv('./datasets/Meteorite_Landings.csv')

# Add 'Type' Columns for easier filtering
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
        try: # Handle cases where it might already be a pure number
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

# Apply conversion functions FIRST
df1['Latitude'] = df1['Latitude (Deg)'].apply(convert_latitude) 
df1['Longitude'] = df1['Longitude (Deg)'].apply(convert_longitude)

# Create GeoLocation matching df2's format
df1['GeoLocation'] = '(' + df1['Latitude'].astype(str) + ', ' + df1['Longitude'].astype(str) + ')'

# Convert other columns to float safely
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
    errors='coerce' # Removing the strict format constraint
)

# Data Cleaning for df2 (Meteorite Landings)
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


''' visulization of data '''

'''Frequency of Bolide over the years'''

yearly_counts = df1['Date/Time - Peak Brightness (UT)'].dt.year.value_counts().sort_index()

if yearly_counts.empty:
    print("Warning: The yearly_counts series is empty. Check your CSV date column!")
else:
    # Plot the data
    plt.figure(figsize=(10, 6))
    yearly_counts.plot(kind='bar', color='skyblue', edgecolor='black')

    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Frequency of Bolide Appearance Over Time', fontsize=14)

    plt.xticks(rotation=45)
    plt.tight_layout() 
    plt.show()

''' Landing over the years (excluding NA values) '''

# isolate the column and count frequencies
meteorite_counts = df['year'].value_counts().sort_index()

# Smooth the data using a rolling window (3 years)
smoothed_counts = meteorite_counts.rolling(window=3).mean() 

plt.figure(figsize=(10,6))

# Plot the smoothed data with a thicker line
plt.plot(meteorite_counts.index, smoothed_counts.values, 
         marker='o', linestyle='-', color='orange', linewidth=2, label='Smoothed Data')

# Scatter the raw data
plt.scatter(meteorite_counts.index, meteorite_counts.values, 
            color='blue', label='Raw Data', alpha=0.5)

plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Meteorite Landings', fontsize=12)
plt.title('Meteorite Landings Over the Years', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.xlim(1800, 2026) # Perfect limits to capture historical and recent data

plt.tight_layout()
plt.show()

''' Count of meteorite in each class '''
value_counts = df2['recclass'].value_counts()
total_count = value_counts.sum()

threshold_percentage = 1

filtered_value_counts = value_counts[value_counts / total_count * 100 > threshold_percentage]

filtered_value_counts['Other'] = total_count - filtered_value_counts.sum()

plt.figure(figsize=(8, 8))
filtered_value_counts.plot(kind='pie', autopct = '%1.1f%%', startangle = 90, legend = False)

plt.title('Distribution of recclass (Above 1%)')
plt.ylabel('')

print("\nCount of Meteorites in each class")
for class_name, count in filtered_value_counts.items():
    print(f"{class_name}: {count}")

plt.show()

# Cleaning the data: Drop rows where we don't have coordinates, and filter out (0, 0) coordinates means Missing Data called Null Island
map_data = df2.dropna(subset=['Latitude', 'Longitude'])
map_data = map_data[(map_data['Latitude'] != 0) & (map_data['Longitude'] != 0)]

# interactive map
fig = px.scatter_geo(
    map_data,
    lat='Latitude',
    lon='Longitude',
    hover_name='name',       # Shows the meteorite name when hovered
    hover_data=['mass (g)', 'year', 'recclass'], # Extra details on hover
    color_discrete_sequence=['red'], # Color the dots red
    opacity=0.5,             # Make dots slightly transparent to see clusters
    title='Global Meteorite Landings'
)

# Customizing the map style
fig.update_geos(
    projection_type="natural earth",
    showcoastlines=True, coastlinecolor="Black",
    showland=True, landcolor="lightgreen",
    showocean=True, oceancolor="lightblue"
)

fig.show()