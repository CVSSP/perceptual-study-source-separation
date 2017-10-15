import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import listen as ln


ratings = pd.read_csv('./data/ratings.csv')

ratings = ratings.query("~sound.isin(['ref', 'Quality', 'Interferer'])")

ratings = ln.mushra.average_replicates(ratings)

corrs, median = ln.mushra.subject_vs_group(ratings, 'normalised_rating')

# Median correlation with the group
subjects = median.reset_index()

corrs = corrs.reset_index()

sb.boxplot('experiment', 'pearson',
            data=corrs,
             )

plt.show()

sub = ratings.query(
    "experiment == 'quality' & page == 'vocals-49-SIR'")
subject = sub.query("subject == 'X'")
med = sub.query("subject != 'X'").groupby('sound').median().reset_index()

import numpy as np
from scipy import stats
x = subject['normalised_rating']
y = med['normalised_rating']

print(stats.pearsonr(x, y))
print(ln.correlation.krippendorffs_alpha(np.array([x, y]), 'ratio'))

plt.plot(med['sound'], med['normalised_rating'], 'o')
plt.plot(subject['sound'], subject['normalised_rating'], 'o')
plt.show()
