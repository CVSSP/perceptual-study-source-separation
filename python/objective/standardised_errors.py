'''
The idea:

    sample = 1 sound that has been rated / measured

    Error(sample) =
    |model_prediction(sample) - subective_median(sample)| / IQR(sample)

    where IQR is the interquartile range of the the subjective ratings.
    Can do without normalisation, but then interpretation is a little
    difficult?

model_prediction needs mapping to subjective scale:
    - Linear fit to medians on a page-by-page basis
    - Linear fit to pooled medians
    - Can consider nonlinear mappings...

My current preference:
    - Keep it in line with the experiment, subjects rated on a page by page
    basis.

    - Compute an average error for each page, giving you 16 average errors.

    - Summarise performance from this distribution.
'''
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


# some functions needed:
def iqr(g):
    '''
    The interquarile range
    '''
    return g.quantile(0.75) - g.quantile(0.25)


def fit(g):
    '''
    Uses linear regression to fits the objective predictions to the subjective
    medians using linear regression.
    '''
    out = stats.linregress(g['score'], g['subjective'])
    fitted = out.slope * g['score'] + out.intercept
    return fitted

# Pull out within-trial means or not (ignore for now)
remove_song_effect = False

# Objective predictions
predictions = pd.read_csv('./data/bss_eval_and_peass_corrected.csv')

# Subjective medians and IQR
ratings = pd.read_csv('./data/ratings.csv')
ratings = ratings.query("~sound.isin(['ref', 'Interferer', 'Quality'])")
medians = (
    ratings.groupby(['experiment', 'page', 'sound']).median()
                                                    .reset_index()
)

iqr = (
    ratings.groupby(['experiment', 'page', 'sound']).agg(iqr)
                                                    .reset_index()
)

# Sort the two dataframes
predictions = predictions.sort_values(
    by=['metric', 'experiment', 'page', 'sound'])
medians = medians.sort_values(
    by=['experiment', 'page', 'sound'])

if remove_song_effect:

    predictions['score'] = predictions.groupby(
        ['experiment', 'page', 'metric'])['score'].transform(
        lambda g: g - np.mean(g)
    )

    medians['normalised_rating'] = medians.groupby(
        ['experiment', 'page'])['normalised_rating'].transform(
        lambda g: g - np.mean(g)
    )


# Copy medians to prediction dataframe
predictions['subjective'] = predictions.groupby(
    ['metric']).apply(
        lambda g: medians['normalised_rating']
).values.flatten()

predictions['iqr'] = predictions.groupby(
    ['metric']).apply(
        lambda g: iqr['normalised_rating']
).values.flatten()

# Only care about these
predictions = predictions.query(
    ("metric == 'SAR' and experiment == 'quality' or "
     "metric == 'APS' and experiment == 'quality' or "
     "metric == 'SIR' and experiment == 'interferer' or "
     "metric == 'IPS' and experiment == 'interferer'"
     )
)


# Fit prediction to subjective medians
predictions['fitted_score'] = predictions.groupby(
    ['metric', 'experiment', 'page']).apply(
        lambda g: fit(g)
).values

predictions['error'] = np.abs(predictions['fitted_score'] -
                              predictions['subjective'])
predictions['normalised_error'] = predictions['error'] / predictions['iqr']

# What do we have?
print(predictions.head())

# Average error for each trial
error = (
    predictions.groupby(
        ['metric', 'experiment', 'page']
    )['normalised_error'].agg(np.mean).reset_index()
)
error['Statistic'] = 'Mean'

# Max error for each trial
error2 = (
    predictions.groupby(
        ['metric', 'experiment', 'page']
    )['normalised_error'].agg(np.max).reset_index()
)
error2['Statistic'] = 'Max'
error3 = error.append(error2)

'''
The plot
'''

'''
fig, axes = plt.subplots(1, 2)

for i, (experiment, order) in enumerate(
    zip(['quality', 'interferer'], [['APS', 'SAR'], ['SIR', 'IPS']])
):

    data = error3[error3.experiment == experiment]

    sb.boxplot(x='metric', y='normalised_error', hue='Statistic',
               order=order,
               palette='Set1',
               fliersize=0,
               notch=True,
               data=data,
               ax=axes[i],
               )

    sb.swarmplot(x='metric', y='normalised_error', hue='Statistic',
                 order=order,
                 color='k',
                 dodge=True,
                 data=data,
                 ax=axes[i],
                )

handles, labels = axes[0].get_legend_handles_labels()
axes[0].legend(handles[:2], labels[:2], loc='upper left')
axes[1].legend_.remove()

axes[0].set_ylim(0, 5)
axes[1].set_ylim(0, 2.5)
axes[0].set_title('Quality')
axes[1].set_title('Interference')
axes[0].set_ylabel('Standardised error')
axes[1].set_ylabel('')
axes[0].set_xlabel('')
axes[1].set_xlabel('')
[sb.despine(ax=axes[i], offset=10) for i in range(2)]
plt.tight_layout()
plt.savefig('metric_boxplot.png', dpi=300)
plt.show()
'''

'''
Another plot
'''
fig, ax = plt.subplots(figsize=(3.39, 2.5))
error.loc[error.metric == 'SAR', 'metric'] = 'BSS Eval'
error.loc[error.metric == 'SIR', 'metric'] = 'BSS Eval'
error.loc[error.metric == 'APS', 'metric'] = 'PEASS'
error.loc[error.metric == 'IPS', 'metric'] = 'PEASS'

sb.boxplot(x='experiment', y='normalised_error', hue='metric',
           hue_order=['BSS Eval', 'PEASS'],
           palette='Set1',
           fliersize=0,
           notch=True,
           data=error,
           ax=ax,
           )

# iterate over boxes
colors = sb.color_palette("PRGn")
colors = [colors[1], colors[2]]
for i,box in enumerate(ax.artists):
    box.set_facecolor(colors[i%2])

sb.swarmplot(x='experiment', y='normalised_error', hue='metric',
             hue_order=['BSS Eval', 'PEASS'],
             color='k',
             dodge=True,
             data=error,
             ax=ax,
             )

x = [-0.25, 0.25, 0.75, 1.25]
y = error.groupby(['experiment', 'metric'])['normalised_error'].quantile(0.8).values
y = [y[2], y[3], y[0], y[1]]
text = ['SAR', 'APS', 'SIR', 'IPS']
[plt.text(_ + 0.2, _2, _3, ha='center', va='bottom') for _, _2, _3 in zip(x, y, text)]

ax.legend_.remove()
ax.set_ylabel('Mean standardised error')
ax.set_xticklabels(['Quality', 'Interference'])
ax.set_xlabel('')
plt.tight_layout()
sb.despine(ax=ax, offset=10)
plt.savefig('./paper/images/metric_boxplot.png', dpi=300)
plt.show()
