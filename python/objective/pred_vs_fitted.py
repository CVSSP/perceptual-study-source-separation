import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


def rmse(e):
    return np.sqrt(np.mean(e * e))


def absmax(e):
    return np.max(np.abs(e))


data = pd.read_csv('./data/subjective_objective_global.csv')

data['error'] = data['fitted_score'] - data['subjective_median']

r = data.groupby(['metric']).apply(
    lambda g: stats.pearsonr(g['fitted_score'], g['subjective_median'])
)

print(r)

#data = data.query("metric.isin(['SAR', 'APS'])")

error_stats = data.groupby(['metric']).agg(
    {'error': [rmse, absmax],
     })

fig, ax = plt.subplots(figsize=(3.3, 3.0))
colors = sb.color_palette("PuOr", 10)

sb.regplot(y='fitted_score', x='subjective_median',
           fit_reg=False,
           data=data.query("metric == 'APS'"),
           color=colors[2],
           ax=ax,
           label='APS',
          )

sb.regplot(y='fitted_score', x='subjective_median',
           fit_reg=False,
           data=data.query("metric == 'SAR'"),
           color=colors[6],
           marker='^',
           ax=ax,
           label='APS',
          )

r = data.groupby(['metric']).apply(
    lambda g: stats.pearsonr(g['fitted_score'], g['subjective_median'])[0]
)

handles, labels = ax.get_legend_handles_labels()
labels[0] = 'APS: $r$ = {number:.{digits}f}'.format(number=r.APS, digits=2)
labels[1] = 'SAR: $r$ = {number:.{digits}f}'.format(number=r.SAR, digits=2)
ax.legend(handles, labels, loc='upper left')

ax.plot([-20, 100], [-20, 100], '--', color='0.25', zorder=-3, linewidth=0.5)
plt.xlim(0, 90)
plt.ylim(0, 90)
plt.ylabel('Fitted objective rating')
plt.xlabel('Median subjective rating')

ticks = np.arange(0, 85, 10)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
sb.despine(offset=0)
plt.tight_layout(pad=0.2)

plt.savefig('./paper/images/subjective_vs_sar_aps.png', dpi=300)
plt.show()
