import plotly.express as px

from dice import Die

die_1 = Die()
die_2 = Die()

results = [die_1.roll()+ die_2.roll() for i in range(1000)]


max_result = die_1.num_sides + die_2.num_sides
poss_results = range(2, max_result+1)

frequencies = [results.count(value) for value in poss_results]

title = "Results of Rolling Two D6 1,000 Times"
labels = {'x': 'Result', 'y': 'Frequency of Result'}

fig = px.bar(x=poss_results, y=frequencies, title=title, labels=labels)
fig.update_layout(xaxis_dtick=1)

fig.show()