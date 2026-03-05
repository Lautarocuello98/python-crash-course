from pathlib import Path
import json
import plotly.express as px

# Load the GeoJSON earthquake dataset
path = Path(__file__).parent.parent / "eq_data" / "past_7_days.geojson"

contents = path.read_text(encoding='utf-8')
all_eq_data = json.loads(contents)

# Extract earthquake dictionaries
all_eq_dicts = all_eq_data['features']

# Lists to store earthquake data
mags, lons, lats, eq_titles = [], [], [], []

# Pull required data directly from each earthquake dictionary
for eq_dict in all_eq_dicts:
    mags.append(eq_dict['properties']['mag'])
    lons.append(eq_dict['geometry']['coordinates'][0])
    lats.append(eq_dict['geometry']['coordinates'][1])
    eq_titles.append(eq_dict['properties']['title'])

# Use the dataset metadata title automatically
title = all_eq_data['metadata']['title']

# Create geographic scatter plot
fig = px.scatter_geo(
    lat=lats,
    lon=lons,
    size=mags,
    title=title,
    color=mags,
    color_continuous_scale='Viridis',
    labels={'color': 'Magnitude'},
    projection='natural earth',
    hover_name=eq_titles,
)

fig.show()