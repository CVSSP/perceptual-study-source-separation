import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import listen


def calculate_alpha(frame, remove_these=['Quality', 'Interferer', 'ref']):

    if isinstance(remove_these, list):
        frame = frame[~frame.sound.isin(remove_these)]

    alpha, _ = listen.mushra.inter_rater_reliability(
        frame, 'normalised_rating')

    alpha2, _ = listen.mushra.inter_rater_reliability(
        frame, 'rank')

    alpha, alpha2 = alpha.reset_index(), alpha2.reset_index()
    alpha['type'] = 'rating'
    alpha2['type'] = 'rank'
    alpha = alpha.append(alpha2)

    return alpha


plot = False
frame = pd.read_csv('./data/ratings.csv')
frame = listen.mushra.rank_ratings(frame)

alpha = calculate_alpha(frame)
alpha['Hidden included'] = 'No'
alpha2 = calculate_alpha(frame, None)
alpha2['Hidden included'] = 'Yes'
alpha = alpha.append(alpha2)

for g in alpha.groupby(['experiment', 'Hidden included', 'type']):
    print(g[0])

    median = g[1][0].agg(np.median)

    ci = g[1][0].agg(lambda g2: listen.utils.bootstrap_ci(g2, np.median))

    iqr = g[1][0].agg(lambda g2: g2.quantile(0.75) - g2.quantile(0.25))

    print('median : ', median, 'CI95 : ', ci, 'IQR : ', iqr)


if plot:
    fig, ax = plt.subplots(figsize=(3.39, 2.5))
    pal = sb.color_palette('Pastel1')
    pal = pal.as_hex()

    sb.pointplot(y=0, x='experiment', hue='Hidden included',
                 markers='o',
                 linestyles=['-', 'dotted'],
                 dodge=0.3,
                 errwidth=2,
                 data=alpha.query("type == 'rating'"), palette='Set1', ax=ax)

    sb.pointplot(y=0, x='experiment', hue='Hidden included',
                 markers='*',
                 linestyles=['-', 'dotted'],
                 dodge=0.3,
                 errwidth=2,
                 data=alpha.query("type == 'rank'"), palette='Set1', ax=ax)

    plt.setp(ax.artists, alpha=0.3)
    ax.set_ylabel("Krippendorff's alpha")
    ax.set_ylim(0.25, 0.9)
    ax.set_xticklabels(['Interference', 'Quality'])
    ax.set_xlabel('Task')
    ax.legend_.remove()
    ax.text(0.0, 0.5, 'Hidden stimuli excluded', color=pal[0], fontsize=10)
    ax.text(0.4, 0.73, 'Hidden stimuli included', color=pal[1], fontsize=10)

    sb.despine()
    plt.tight_layout()
    plt.show()
