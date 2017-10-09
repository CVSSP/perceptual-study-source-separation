import numpy as np
import listen as ln
import pandas as pd
import matplotlib.pyplot as plt


ratings = pd.read_csv('./data/ratings.csv')

ratings = ratings.query("~sound.isin(['ref', 'Quality', 'Inteference'])")

subjects = pd.unique(ratings.subject)

out = np.zeros((1000, 2))

which = []

mine = ['B', 'D', 'F', 'J', 'L', 'U', 'I', 'U']

choose = [x for x in subjects if x not in mine]

for i in range(out.shape[0]):

    these = np.random.choice(choose, 7, replace=False)
    which.append(these)

    for j, g in enumerate(ratings.groupby(['experiment'])):

        # rating2 = g[1].query("~subject.isin(['B', 'D', 'F', 'J', 'L', 'U', 'I', 'U'])")

        rating2 = g[1][~g[1].subject.isin(these)]

        medians1 = ln.mushra.average(g[1], 'median')
        medians2 = ln.mushra.average(rating2, 'median')

        concor = ln.utils.concordance(medians1['rating'].values,
                                    medians2['rating'].values)

        out[i, j] = concor

print(np.sum(out[:, 0] < 0.889) / out.shape[0])
print(np.sum(out[:, 1] < 0.9696) / out.shape[0])

plt.boxplot(out)
plt.show()
