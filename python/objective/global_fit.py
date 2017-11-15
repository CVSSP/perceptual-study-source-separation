'''
The idea:

    sample = 1 sound that has been rated / measured

    Error(sample) = model_prediction(sample) - subective_median(sample)

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
import listen as ln


def fit(g):
    '''
    Uses linear regression to fits the objective predictions to the subjective
    medians using linear regression.
    '''
    out = stats.linregress(g['score'], g['subjective_median'])
    fitted = out.slope * g['score'] + out.intercept
    print(out.rvalue)
    return fitted

def calculate_ci(data):

    ci = ln.utils.bootstrap_ci(data,
                               np.median,
                               n=1000,
                               conf_level=95,
                               plot=False)

    return pd.Series({'lo': ci[0], 'hi': ci[1]})



# Pull out within-trial means or not
remove_song_effect = False
per_page_fit = False
boxplots = False

# Objective predictions
predictions = pd.read_csv('./data/bss_eval_and_peass_corrected.csv')

# Subjective ratings, remove hidden stimuli
ratings = pd.read_csv('./data/ratings.csv')
ratings = ratings.query("~sound.isin(['ref', 'Interferer', 'Quality'])")

# Sort the two dataframes
predictions = predictions.sort_values(
    by=['metric', 'experiment', 'page', 'sound'])

ratings = ratings.sort_values(
    by=['subject', 'experiment', 'page', 'sound'])

# Remove means or not?
if remove_song_effect:

    predictions['score'] = predictions.groupby(
        ['metric', 'experiment', 'page'])['score'].transform(
        lambda g: g - np.mean(g)
    )

    ratings['normalised_rating'] = ratings.groupby(
        ['subject', 'experiment', 'page'])['normalised_rating'].transform(
        lambda g: g - np.mean(g)
    )

if boxplots:
    for g in ratings.groupby(['experiment', 'page']):
        g[1].boxplot(by='sound', column='normalised_rating')
        plt.title(g[0])
        plt.show()

medians = ln.mushra.average(ratings, 'median')
print(medians.head())
print(predictions.query("experiment == 'interferer'").head())

# Copy medians to prediction dataframe
for g in predictions.groupby('experiment'):
    num_metrics = len(pd.unique(g[1].metric))
    predictions.ix[g[1].index, 'subjective_median'] = np.tile(
        medians[medians.experiment == g[0]]['normalised_rating'], num_metrics)

# Fit prediction to subjective medians
if per_page_fit:
    predictions['fitted_score'] = predictions.groupby(
        ['metric', 'page']).apply(
            lambda g: fit(g)
    ).values

    predictions.to_csv('./data/subjective_objective_per_page.csv', index=None)
else:
    predictions['fitted_score'] = predictions.groupby(
        ['metric']).apply(
            lambda g: fit(g)
    ).values

    if remove_song_effect:
        predictions.to_csv('./data/subjective_objective_global_centred.csv', index=None)
    else:
        predictions.to_csv('./data/subjective_objective_global.csv', index=None)
