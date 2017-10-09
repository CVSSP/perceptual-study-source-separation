import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import listen as ln


ratings = pd.read_csv('./data/ratings.csv')

ratings = ratings.query("~sound.isin(['ref', 'Quality', 'Interferer'])")

corrs = ln.mushra.within_subject_agreement(ratings, 'rating')

print(corrs)

subjects = corrs.correlation.reset_index()

subjects = subjects.sort_values(by=['experiment', 'concordance'])

sb.boxplot('experiment', 'concordance',
           data=subjects,
           )

plt.show()

d = ratings.query("subject.isin(['L']) & " +
                  "is_replicate & experiment == 'quality'")

for g in d.groupby('subject'):

    fig, ax = plt.subplots()
    g[1].groupby('page_order').plot(x='sound', y='rating', ax=ax)
    ax.set_title(g[0])

    plt.show()
