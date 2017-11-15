import scipy
import listen as ln
import pandas as pd

predictions = pd.read_csv(
    './data/bss_eval_and_peass_non_norm_corrected.csv')

# Subjective ratings, remove hidden stimuli
ratings = pd.read_csv('./data/ratings.csv')
ratings = ratings.query("~sound.isin(['ref', 'Interferer', 'Quality'])")

# Sort the two dataframes
predictions = predictions.sort_values(
    by=['metric', 'experiment', 'page', 'sound'])

ratings = ratings.sort_values(
    by=['subject', 'experiment', 'page', 'sound'])

medians = ln.mushra.average(ratings, 'median')

def fit(g):

    one = medians[medians.experiment.isin(g.experiment)]
    return scipy.stats.pearsonr(one['normalised_rating'], g['score'])[0]

out = predictions.groupby('metric').apply(fit)
print(out)
