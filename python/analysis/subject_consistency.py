import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import listen as ln


def iqr(data):

    return data.quantile(0.75) - data.quantile(0.25)


frame = pd.read_csv('./data/ratings.csv')

frame = frame.query("~sound.isin(['ref', 'Quality', 'Interferer'])")

# frame = frame.query("subject == 'R'")

corrs, stats = ln.mushra.within_subject_agreement(frame,
                                                  'normalised_rating')

corrs.boxplot(by='experiment', column='concordance')
plt.show()

print('~~~ Estimated correlation ~~~')
print('Medians')
print(stats.median)
print('IQR')
print(stats.iqr)
