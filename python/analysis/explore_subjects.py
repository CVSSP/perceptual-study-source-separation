'''
From visual analysis, these subjects stand out from the group in terms of the
two anchors and the reference:
    J, D, B, F, U, X

The remaining subjects highlighted below were also selected as they had a low
concordance value compared to the remaining subjects.

'''
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


ratings = pd.read_csv('./data/ratings.csv')

print(ratings.head())

for exp, group in ratings.groupby('experiment'):

    sb.boxplot('sound', 'normalised_rating', data=group)
    plt.title('Experiment: {}'.format(exp))
    plt.show()

    sub = group.query(
        "subject.isin(['J', 'D', 'B', 'F', 'U', 'X', 'T', 'I', 'L'])")

    for g in sub.groupby(['subject']):
        g2 = g[1].query("sound.isin(['ref', 'Quality', 'Interferer'])")

        print(g[1].query("sound.isin(['ref'])"))

        sb.stripplot('sound', 'normalised_rating', data=g2, jitter=True)
        plt.title('Experiment: {0}, subject: {1}'.format(exp, g[0]))
        plt.show()
