import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats


def fit(g, sample=True):
    '''
    Uses linear regression to fits the objective predictions to the subjective
    medians using linear regression. Returns correlation coefficient
    '''
    idx = np.arange(len(g))
    if sample:
        idx = np.random.choice(idx, len(g), replace=True)

    r = stats.pearsonr(g['score'].values[idx], g['subjective_median'].values[idx])[0]
    return r


predictions = pd.read_csv('./data/subjective_objective_global.csv')

num_iters = 5000

songs = pd.Series(pd.unique(predictions.page))
num_songs = songs.size

effect = pd.DataFrame(columns=pd.unique(predictions.metric),
                      index=np.arange(num_iters))

global_resample = True
for i in range(num_iters):

    if not global_resample:
        song_selection = songs.sample(num_songs, replace=True)
        temp = predictions[predictions.page.isin(song_selection)]
    else:
        temp = predictions

    # Fit prediction to subjective medians (global fit)
    effect.iloc[i] = temp.groupby('metric').apply(
        lambda g: fit(g, global_resample)
    )

effect = pd.melt(effect, var_name='metric', value_name='corr')

'''
for g in effect.groupby('metric'):
    sm.qqplot(g[1]['corr'].values, fit=True, line='45')
    plt.show()
'''

r = predictions.groupby('metric').apply(
    lambda g: fit(g, False)
)

ci95 = effect.groupby('metric')['corr'].apply(
    lambda g: pd.Series({'lo': np.percentile(g, 2.5),
                        'hi': np.percentile(g, 97.5)})
)

print('Correlation')
print(r)

print('Confidence intervals')
print(ci95)

effect.boxplot(by='metric', column='corr')
plt.show()
