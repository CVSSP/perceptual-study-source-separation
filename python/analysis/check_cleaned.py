import numpy as np
import listen as ln
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from scipy import stats


ratings = pd.read_csv('./data/ratings.csv')
ratings = ratings.query("~sound.isin(['ref', 'Quality', 'Inteference'])")

ratings2 = pd.read_csv('./data/ratings_dropped.csv')
ratings2 = ratings2.query("~sound.isin(['ref', 'Quality', 'Inteference'])")


# Medians
meds = ratings.groupby(['experiment', 'page', 'sound']).agg(
    {'normalised_rating': np.median}).reset_index()
meds2 = ratings2.groupby(['experiment', 'page', 'sound']).agg(
    {'normalised_rating': np.median}).reset_index()

meds['normalised_rating2'] = meds2['normalised_rating']

func = ln.utils.concordance

concordance = meds.groupby(['experiment', 'page']).apply(
    lambda g: func(g['normalised_rating'].values,
                   g['normalised_rating2'].values
                   )
).reset_index()

concordance.boxplot(column=0, by=['experiment'])
plt.show()

error = (meds['normalised_rating'] - meds['normalised_rating2']).abs()
print(error.quantile(0.95))
sb.boxplot(error)
plt.show()
