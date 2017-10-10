import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import numpy as np


frame = pd.read_csv('./data/ratings.csv')

sub = frame.query("sound.isin(['Quality', 'Interferer', 'ref'])")

ref = sub.query("sound == 'ref'")

out = ref.groupby('experiment')['normalised_rating'].agg(
    lambda g: 100 * np.sum(g == 100) / g.size
)

print('Percentage of ratings for the reference equal to 100:', out)

fig, ax = plt.subplots(figsize=(3.39, 2.5))

sb.swarmplot(y="sound", x="normalised_rating", hue='experiment',
             palette='Set1',
             dodge=True,
             ax=ax,
             data=sub)

ax.set_xlabel('Normalised rating')
ax.set_ylabel('')
ax.set_yticklabels(['$A_{Q}$', '$A_{I}$', 'Ref'])
ax.legend(labels=['Interference', 'Quality'], title='Task')
ax.set_xlim(-5, 105)

sb.despine()
plt.tight_layout()
plt.savefig('./paper/images/swarmplot_hidden_sounds.png', dpi=300)
plt.show()
