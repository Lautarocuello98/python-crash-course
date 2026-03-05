from pathlib import Path
import json

# Read data as a string and convert to a python object.
path = Path(__file__).parent.parent / "eq_data" / "past_7_days.geojson"
contents = path.read_text(encoding='utf-8')
all_eq_data = json.loads(contents)

# Create a more readable version of the data file.
path = Path(__file__).parent.parent / "eq_data" / "readable_past_7_days.geojson"
readable_contents = json.dumps(all_eq_data, indent=4)
path.write_text(readable_contents)