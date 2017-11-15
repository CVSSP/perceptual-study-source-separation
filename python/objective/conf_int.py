from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import listen as ln


def calculate_ci(data):

    ci = ln.utils.bootstrap_ci(data,
                               np.median,
                               n=5000,
                               conf_level=95,
                               plot=False)

    return (ci[1] - ci[0]) / 2


# Subjective ratings, remove hidden stimuli
ratings = pd.read_csv('./data/ratings.csv')
ratings = ratings.query("~sound.isin(['ref', 'Interferer', 'Quality'])")
ratings = ratings.query("experiment == 'quality'")
ratings = ln.mushra.average_replicates(ratings)

ci95 = (
    ratings.groupby(['page', 'sound'])
    ['normalised_rating'].agg(
        lambda g: calculate_ci(g)
    )
).reset_index()

print(np.percentile(ci95['normalised_rating'], 95))
print(np.percentile(ci95['normalised_rating'], 50))
