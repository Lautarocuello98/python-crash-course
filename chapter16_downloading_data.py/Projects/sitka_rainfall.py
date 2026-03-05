from pathlib import Path
import csv
from datetime import datetime

import matplotlib.pyplot as plt

path = Path('C:/Users/lac_/programacion/python crash course/chapter16_downloading_data.py/sitka_weather_2021_full.csv')
lines = path.read_text(encoding='utf-8').splitlines()

reader = csv.reader(lines)
header_row = next(reader)

# Extract dates, and high and low temperatures.
dates, prcps = [], []

for row in reader:
    current_date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        prcp = float(row[5])
    except ValueError:
        print(f"Missing data for {current_date}")
    else:
        dates.append(current_date)
        prcps.append(prcp)

# Plot the high and low temperatures.
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots()
ax.plot(dates, prcps, color='green', alpha=0.5)

# Format plot.
title = "Daily Quantity rainfall, 2021\nDeath Valley, CA"
ax.set_title(title, fontsize=20)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("PRCP", fontsize=16)
ax.tick_params(labelsize=16)


plt.show()