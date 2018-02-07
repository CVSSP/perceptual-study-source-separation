import numpy as np
import pandas as pd
import listen


def calculate_alpha(frame):

    alpha, _ = listen.mushra.inter_rater_reliability(
        frame, 'normalised_rating', 'ratio')

    alpha2, _ = listen.mushra.inter_rater_reliability(
        frame, 'rank', 'ordinal')

    alpha, alpha2 = alpha.reset_index(), alpha2.reset_index()
    alpha['type'] = 'rating'
    alpha2['type'] = 'rank'
    alpha = alpha.append(alpha2)

    return alpha


frame = pd.read_csv('./data/ratings.csv')
frame = frame.query("~sound.isin(['ref', 'Quality', 'Interferer'])")
frame = listen.mushra.rank_ratings(frame)

alpha = calculate_alpha(frame)

for g in alpha.groupby(['experiment', 'type']):
    print(g[0])

    median = g[1][0].agg(np.median)

    iqr = g[1][0].agg(lambda g2: g2.quantile(0.75) - g2.quantile(0.25))

    print('median : ', median, 'IQR : ', iqr)
