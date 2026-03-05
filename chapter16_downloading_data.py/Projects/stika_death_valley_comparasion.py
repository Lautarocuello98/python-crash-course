from pathlib import Path
import csv
from datetime import datetime
import matplotlib.pyplot as plt


def get_highs(csv_path):
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    reader = csv.reader(lines)
    header = next(reader)

    date_index = header.index("DATE")
    tmax_index = header.index("TMAX")

    dates, highs = [], []

    for row in reader:
        try:
            current_date = datetime.strptime(row[date_index], "%Y-%m-%d")
            high = int(row[tmax_index])
        except ValueError:
            continue
        else:
            dates.append(current_date)
            highs.append(high)

    return dates, highs


# ---- FILE PATHS ----
sitka_path = Path(r"C:\Users\lac_\programacion\python crash course\chapter16_downloading_data.py\weather_data\sitka_weather_2021_full.csv")
dv_path = Path(r"C:\Users\lac_\programacion\python crash course\chapter16_downloading_data.py\weather_data\death_valley_2021_full.csv")

# ---- LOAD DATA ----
sitka_dates, sitka_highs = get_highs(sitka_path)
dv_dates, dv_highs = get_highs(dv_path)

# ---- SAME Y SCALE ----
y_min = min(min(sitka_highs), min(dv_highs))
y_max = max(max(sitka_highs), max(dv_highs))

# ---- PLOTS ----
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

ax1.plot(sitka_dates, sitka_highs, color="blue")
ax1.set_title("Sitka - Daily Highs (2021)")
ax1.set_ylabel("Temperature (F)")
ax1.set_ylim(y_min, y_max)

ax2.plot(dv_dates, dv_highs, color="red")
ax2.set_title("Death Valley - Daily Highs (2021)")
ax2.set_ylabel("Temperature (F)")
ax2.set_ylim(y_min, y_max)

fig.autofmt_xdate()
plt.tight_layout()
plt.show()