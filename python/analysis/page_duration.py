import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import pandas as pd
from scipy import stats


frame = pd.read_csv('./data/ratings.csv')

group = frame.groupby(['subject', 'experiment'])
page_durs = group['page_duration'].mean().reset_index()

median = page_durs.groupby('experiment').median()
iqr = page_durs.groupby('experiment').agg(stats.iqr)

print(median, iqr)

'''
So we get notably higher variance on the quality example.
'''

sb.boxplot(x='experiment',
           y='page_duration',
           data=page_durs)
plt.show()
