import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pickle

duration = 4000
total = 501

infection_times = pickle.load(open("infection_times.p", "rb"))

fig, ax = plt.subplots()
for key in sorted(infection_times):
    x = infection_times[key] + [duration]
    counts = range(len(infection_times[key])) + [len(infection_times[key])]
    y = [float(c) / total * 100 for c in counts]
    ax.plot(x, y, label = str(key) + "%", linewidth=1.5)

plt.xlabel('Time')

plt.ylabel('Infection prevalence (%)')

plt.title('Impact of digital contact tracing depending on adoption rate')
plt.legend(title='Adoption rate', loc='upper left')
plt.savefig('chart.png')