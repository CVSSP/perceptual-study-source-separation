import matplotlib.pyplot as plt
import pandas as pd
import listen as ln


frame = pd.read_csv('./data/ratings.csv')

frame = frame.query("~sound.isin(['ref', 'Quality', 'Interferer'])")

corrs, stats = ln.mushra.within_subject_agreement(frame,
                                                  'normalised_rating')

corrs.boxplot(by='experiment', column='concordance')
plt.show()

print('~~~ Concordance coefficients ~~~')
print('Medians')
print(stats.median)
print('IQR')
print(stats.iqr)
