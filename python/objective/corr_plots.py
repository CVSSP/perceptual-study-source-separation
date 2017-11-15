import listen as ln
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['text.usetex'] = True


corrs = pd.read_csv('./data/correlations.csv')

corrs = corrs.query("corr_type == 'spearman'")

medians = corrs.groupby(['experiment', 'metric'])['corr'].median()

means = corrs.groupby(['experiment', 'metric'])['corr'].mean()

ci95 = corrs.groupby(['experiment', 'metric'])['corr'].apply(
    ln.correlation.confidence_interval
)

print(medians)
print(means)
print(ci95)

fig, ax = plt.subplots(figsize=(3.3, 3.0))

colors = sb.color_palette("PRGn")

order = ['APS', 'TPS', 'SAR', 'ISR', 'SIR', 'IPS']
sb.boxplot(y='metric', x='corr',
           order=order,
           dodge=False,
           data=corrs,
           whis=0,
           fliersize=0,
           ax=ax,
           )

# iterate over boxes
for i, box in enumerate(ax.artists):
    box.set_edgecolor('black')
    box.set_facecolor('white')


# Add some small jitter
corrs['corr'] += np.random.uniform(-0.01, 0.01, size=len(corrs))

sb.swarmplot(y='metric', x='corr',
             data=corrs.query("experiment == 'quality'"),
             order=order,
             size=4,
             dodge=True,
             marker='o',
             ax=ax,
             color=colors[1],
             label='Quality',
             )

sb.swarmplot(y='metric', x='corr',
             data=corrs.query("experiment == 'interferer'"),
             order=order,
             size=4,
             dodge=True,
             marker='X',
             ax=ax,
             color=colors[4],
             label='Interference',
             )


handles, labels = ax.get_legend_handles_labels()
handles = [handles[0], handles[-1]]
labels = [labels[0], labels[-1]]
ax.legend(handles, labels, loc='lower left')

labels = ['APS\n' + r'\scriptsize{PEASS}', 'TPS\n' + r'{\scriptsize PEASS}',
          'SAR\n' + r'{\scriptsize BSS Eval}', 'ISR\n' + r'{\scriptsize BSS Eval}',
          'SIR\n' + r'{\scriptsize BSS Eval}', 'IPS\n' + r'{\scriptsize PEASS}']

ax.set_yticklabels(labels, ha='right')

plt.ylabel('')
plt.xlabel('Spearman correlation')
sb.despine(offset=10)
plt.tight_layout(pad=0.2)
plt.savefig('./paper/images/spearman_boxplot.png', dpi=300)
plt.show()
