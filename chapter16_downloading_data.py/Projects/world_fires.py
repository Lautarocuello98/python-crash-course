from pathlib import Path
import csv
import plotly.express as px

path = Path(__file__).parent.parent / "eq_data" / "world_fires_1_day.csv"
lines = path.read_text(encoding='utf-8').splitlines()

reader = csv.reader(lines)
header_row = next(reader)

brights, lons, lats = [], [], []

bright_index = header_row.index("brightness")
lon_index = header_row.index("longitude")
lat_index = header_row.index("latitude")

for row in reader:
    try:
        brights.append(float(row[bright_index]))
        lons.append(float(row[lon_index]))
        lats.append(float(row[lat_index]))
    except ValueError:
        pass

fig = px.scatter_geo(
    lat=lats,
    lon=lons,
    title="Fires Last Day",
    color=brights,
    color_continuous_scale="Reds",
    labels={'color': 'Brightness'},
    projection="natural earth",
    
)

fig.show()