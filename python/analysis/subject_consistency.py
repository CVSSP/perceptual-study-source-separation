import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import listen as ln


def iqr(data):

    return data.quantile(0.75) - data.quantile(0.25)


frame = pd.read_csv('./data/ratings.csv')

frame = frame.query("~sound.isin(['ref', 'Quality', 'Interferer'])")

corr_data = ln.mushra.within_subject_agreement(frame, 'rating', 'median')

corrs = corr_data.correlation.reset_index()

spread = corrs.groupby('experiment').agg(iqr)

corrs.boxplot(by='experiment', column='concordance')
plt.show()

print('~~~ Estimated correlation ~~~')
print(corr_data.concordance)
print(spread)
print(corr_data.concordance_ci)
