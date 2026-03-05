from pathlib import Path
import csv
from datetime import datetime
import matplotlib.pyplot as plt


# ---- SITKA ----
path1 = Path(r"C:\Users\lac_\programacion\python crash course\chapter16_downloading_data.py\sitka_weather_2021_full.csv")
lines1 = path1.read_text(encoding="utf-8").splitlines()

reader1 = csv.reader(lines1)
header_row1 = next(reader1)

dates1, highs1 = [], []
for row in reader1:
    if len(row) < 8:
        continue
    try:
        current_date = datetime.strptime(row[2], "%Y-%m-%d")
        high = int(row[7])
    except ValueError:
        continue
    else:
        dates1.append(current_date)
        highs1.append(high)


# ---- DEATH VALLEY ----
path2 = Path(r"C:\Users\lac_\programacion\python crash course\chapter16_downloading_data.py\death_valley_2021_full.csv")
lines2 = path2.read_text(encoding="utf-8").splitlines()

reader2 = csv.reader(lines2)
header_row2 = next(reader2)

dates2, highs2 = [], []
for row in reader2:
    if len(row) < 8:
        continue
    try:
        current_date = datetime.strptime(row[2], "%Y-%m-%d")
        high = int(row[7])
    except ValueError:
        continue
    else:
        dates2.append(current_date)
        highs2.append(high)


# ---- DEBUG ----
print("Sitka len:", len(highs1), "min/max:", min(highs1), max(highs1))

if highs2:
    print("Death Valley len:", len(highs2), "min/max:", min(highs2), max(highs2))
else:
    print("Death Valley highs2 is EMPTY -> check indexes / CSV columns")


same = (highs1 == highs2) and (dates1 == dates2)
print("Are datasets identical:", same)


# ---- PLOT ----
fig, ax = plt.subplots()

ax.plot(dates1, highs1, label="Sitka", linewidth=2.2, marker=".", markersize=2)
ax.plot(dates2, highs2, label="Death Valley", linewidth=2.2, linestyle="--", marker=".", markersize=2)

ax.set_title("Daily High Temperatures - 2021", fontsize=20)
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (F)")
fig.autofmt_xdate()
ax.legend()

plt.show()