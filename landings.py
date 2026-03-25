import matplotlib.pyplot as plt
from data_prep import df

''' Landing over the years (excluding NA values) '''

# count frequecy of each meteorite
meteorite_counts = df['year'].value_counts().sort_index()

# Smoothing the data for representation
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
plt.xlim(1800, 2026) 

plt.tight_layout()
plt.savefig('images/landings', bbox_inches='tight', dpi=300)
plt.show()
