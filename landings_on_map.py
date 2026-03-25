## Note : This will open in browser

import plotly.express as px
from data_prep import df2

# Cleaning the data, deleting where latitude or longitude is zero
map_data = df2.dropna(subset=['Latitude', 'Longitude'])
map_data = map_data[(map_data['Latitude'] != 0) & (map_data['Longitude'] != 0)]

# interactive map
fig = px.scatter_geo(
    map_data,
    lat='Latitude',
    lon='Longitude',
    hover_name='name',       
    hover_data=['mass (g)', 'year', 'recclass'], 
    color_discrete_sequence=['red'], 
    opacity=0.5,            
    title='Global Meteorite Landings'
)

# map style
fig.update_geos(
    projection_type="natural earth",
    showcoastlines=True, coastlinecolor="Black",
    showland=True, landcolor="lightgreen",
    showocean=True, oceancolor="lightblue"
)

fig.show()
