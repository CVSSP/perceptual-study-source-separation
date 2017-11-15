import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import numpy as np


frame = pd.read_csv('./data/ratings.csv')

# Probably best to average reps
frame = ln.

sub = frame.query("sound.isin(['Quality', 'Interferer', 'ref'])")

ref = sub.query("sound == 'ref'")

out = ref.groupby('experiment')['normalised_rating'].agg(
    lambda g: 100 * np.sum(g == 100) / g.size
)

print('Percentage of ratings for the reference equal to 100:', out)


#red, blue = sb.xkcd_rgb["pale red"], sb.xkcd_rgb["denim blue"]
colors = sb.color_palette("PRGn")

fig, ax = plt.subplots(figsize=(3.39, 2.5))

sb.swarmplot(x="sound", y="normalised_rating",
             ax=ax,
             data=sub.query("experiment == 'quality'"),
             color=colors[1],
             marker='o',
             size=4,
             label='Quality',
             )

sb.swarmplot(x="sound", y="normalised_rating",
             ax=ax,
             data=sub.query("experiment == 'interferer'"),
             color=colors[4],
             marker='X',
             size=4,
             label='Interference',
             )



ax.set_ylabel('Rating')
ax.set_xlabel('')
ax.set_xticklabels(['$A_{Q}$', '$A_{I}$', 'Ref'])

handles, labels = ax.get_legend_handles_labels()
handles = [handles[0], handles[3]]
labels = [labels[0], labels[3]]
ax.legend(handles, labels,
          loc=(0.6, 0.22),
          )

ax.set_ylim(-5, 105)

sb.despine(offset=10)
plt.tight_layout(pad=0.2)
plt.savefig('./paper/images/swarmplot_hidden_sounds.png', dpi=300)
plt.show()
