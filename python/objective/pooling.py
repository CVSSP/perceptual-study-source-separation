from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


predictions = pd.read_csv('./data/bss_eval_and_peass_corrected.csv')

predictions['aligned_score'] = predictions.groupby(['experiment', 'page', 'metric'])['score'].transform(
    lambda g: g - np.mean(g)
)

aps = predictions.query("metric == 'APS' & experiment == 'quality'")
sir = predictions.query("metric == 'SIR' & experiment == 'interferer'")

ratings = pd.read_csv('./data/ratings.csv')
ratings = ratings.query("~sound.isin(['ref', 'Interferer', 'Quality'])")
medians = (
    ratings.groupby(['experiment', 'page', 'sound']).median()
                                                    .reset_index()
)

medians['aligned_rating'] = medians.groupby(['experiment', 'page'])['normalised_rating'].transform(
    lambda g: g - np.mean(g)
)

quality = medians.query("experiment == 'quality'")
interference = medians.query("experiment == 'interferer'")

print(
    stats.pearsonr(aps['score'].values, quality['normalised_rating'].values)
)

fig, axes = plt.subplots(2, 1)

sb.regplot(aps['score'].values,
           quality['normalised_rating'].values,
           ax=axes[0])

axes[0].set_xlabel('APS')
axes[0].set_ylabel('Subjective medians')

sb.regplot(aps['aligned_score'].values,
           quality['aligned_rating'].values,
           ax=axes[1])

axes[1].set_xlabel('Aligned APS')
axes[1].set_ylabel('Aligned Subjective medians')
plt.tight_layout()
plt.savefig('./aps_fit.png', dpi=300)
plt.show()

# print(stats.linregress(x, y))
