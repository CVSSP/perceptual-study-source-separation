from scipy import stats
import numpy as np
import pandas as pd
import listen as ln
import seaborn as sb
import matplotlib.pyplot as plt

ratings = pd.read_csv('./data/ratings.csv')

ratings['norm'] = ratings.groupby(['subject', 'experiment', 'page'])['rating'].transform(
    lambda g: 100 * (g - g.min()) / (g.max() - g.min())
)

# These three subjects didn't quite understand the task or had some
# difficulties in judging extreme artefacts.
ratings = ratings.query("~subject.isin(['SE-WEB', 'SS-WEB', 'J', 'DB-WEB'])" +
                        "& experiment == 'interferer'")

sb.boxplot('sound', 'norm', data=ratings)
plt.show()

# corr_data = ln.mushra.between_subject_agreement(ratings)

for g in ratings.groupby(['subject']):
    print(g[0])
    g2 = g[1].query("sound.isin(['ref', 'Quality', 'Interferer'])")
    sb.stripplot('sound', 'norm', data=g2, jitter=True)
    plt.show()
