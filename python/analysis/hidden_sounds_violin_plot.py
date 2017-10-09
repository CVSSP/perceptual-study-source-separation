import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
import listen


plt.rcParams.update(
    {'mathtext.default': 'regular',
     'font.size': 10,
     'font.family': 'sans-serif',
     'font.sans-serif':['Helvetica'],
     })

frame = pd.read_csv('./data/ratings.csv')

frame = listen.mushra.normalise_ratings(frame)

sub = frame.query("sound.isin(['Quality', 'Interferer', 'ref'])")

fig, ax = plt.subplots(figsize=(3.39, 2.5))

sb.swarmplot(y="sound", x="rating", hue='experiment',
             palette='Set2',
             dodge=True,
             ax=ax,
             data=sub)

ax.set_xlabel('Normalised rating')
ax.set_ylabel('')
ax.set_yticklabels(['$A_{Q}$', '$A_{I}$', 'R'])
ax.legend(labels=['Interference', 'Quality'], title='Task')
ax.set_xlim(0, 100)
plt.tight_layout()
plt.savefig('./paper/images/swarmplot_hidden_sounds.png', dpi=300)
plt.show()
