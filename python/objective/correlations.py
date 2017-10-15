import numpy as np
import scipy
import listen
import pandas as pd


def get_values(subjective, objective, col='normalised_rating'):
    '''
    This functions sorts subjective ratings and model predictions by sound
    and returns the values.
    '''

    objective = objective.sort_values(by='sound')
    subjective = (
        subjective[subjective.experiment.isin(objective.experiment) &
                   subjective.page.isin(objective.page)]
        .sort_values(by='sound')
    )

    return subjective['normalised_rating'].values, objective['score'].values


def pearson(x, y):
    return scipy.stats.pearsonr(*get_values(x, y))[0]


def spearman(x, y):
    return scipy.stats.spearmanr(*get_values(x, y))[0]


def correlation_stats(data):

    stats = listen.correlation.confidence_interval(data)
    stats.set_value('median', listen.correlation.average(data))
    stats.set_value('min', np.min(data))
    stats.set_value('max', np.max(data))
    stats.set_value('iqr',
                    np.percentile(data, 0.75) - np.percentile(data, 0.25))

    return stats


def main(filename, shuffle_ratings=False):

    # Load subjective data
    ratings = pd.read_csv("./data/ratings.csv")

    # Drop hidden stimuli from ratings
    ratings = ratings.query("~sound.isin(['ref', 'Quality', 'Interferer'])")

    if shuffle_ratings:

        ratings['normalised_rating'] = (

            ratings.groupby(
                ['subject', 'experiment', 'page']

            )['normalised_rating'].transform(np.random.permutation)
        )

    # Compute median rating
    median_rating = listen.mushra.average(ratings, 'median')

    # Model predictions
    predictions = pd.read_csv("./data/predictions.csv")

    # Compute correlation statistics
    corrs = predictions.groupby(['experiment', 'metric', 'page']).agg(
        lambda g: pearson(median_rating, g)
    ).reset_index(name='corr')
    corrs['corr_type'] = 'pearson'

    corrs2 = predictions.groupby(['experiment', 'metric', 'page']).agg(
            lambda g: spearman(median_rating, g)
    ).reset_index(name='corr')
    corrs2['corr_type'] = 'spearman'

    corrs = pd.concat([corrs, corrs2])

    stats = corrs.groupby(['experiment', 'metric', 'corr_type'])['corr'].apply(
        correlation_stats)

    corrs.to_csv(filename)


    return stats


if __name__ == '__main__':

    print(main(filename='./data/correlations.csv'))
