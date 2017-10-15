import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import listen


frame = pd.read_csv('./data/ratings.csv')
frame = frame.query("~sound.isin(['ref', 'Quality', 'Interferer'])")
frame = listen.mushra.average_replicates(frame)

# Rank algorithms
frame = listen.mushra.rank_ratings(frame)

for g in frame.groupby(['page']):

    sb.swarmplot(x='sound', y='rank', hue='experiment',
                 split=True, data=g[1])

    plt.title(g[0])
    plt.show()
