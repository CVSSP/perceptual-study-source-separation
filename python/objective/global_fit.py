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
                               n=5000,
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

# Average the subjective values (take median)
medians = ln.mushra.average(ratings, 'median')

# Confidence intervals
ci95 = (
    ratings.groupby(['experiment', 'page', 'sound'])['normalised_rating'].apply(
        calculate_ci)
).reset_index()

# Sort the two dataframes
predictions = predictions.sort_values(
    by=['metric', 'experiment', 'page', 'sound'])

medians = medians.sort_values(
    by=['experiment', 'page', 'sound'])

# Copy medians and confidence intercals to prediction dataframe
for g in predictions.groupby('experiment'):
    num_metrics = len(pd.unique(g[1].metric))

    predictions.ix[g[1].index, 'subjective_median'] = np.tile(
        medians[medians.experiment == g[0]]['normalised_rating'], num_metrics)

    predictions.ix[g[1].index, 'ci95_lo'] = np.tile(
        ci95[ci95.experiment == g[0]]['normalised_rating'][1::2], num_metrics)

    predictions.ix[g[1].index, 'ci95_hi'] = np.tile(
        ci95[ci95.experiment == g[0]]['normalised_rating'][::2], num_metrics)

predictions['fitted_score'] = predictions.groupby(
    ['metric']).apply(
        lambda g: fit(g)
).values

predictions.to_csv('./data/subjective_objective_global.csv', index=None)
