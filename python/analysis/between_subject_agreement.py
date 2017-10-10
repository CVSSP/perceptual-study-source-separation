import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import listen


frame = pd.read_csv('./data/ratings.csv')


def calculate_alpha(remove_these=['Quality', 'Interferer', 'ref']):

    alpha, _ = listen.mushra.inter_rater_reliability(
        frame, 'normalised_rating', remove_these)
    alpha2, _ = listen.mushra.inter_rater_reliability(
        frame, 'rank', remove_these)
    alpha, alpha2 = alpha.reset_index(), alpha2.reset_index()
    alpha['type'] = 'rating'
    alpha2['type'] = 'rank'
    alpha = alpha.append(alpha2)

    return alpha

alpha = calculate_alpha()
alpha['Hidden included'] = 'No'
alpha2 = calculate_alpha(None)
alpha2['Hidden included'] = 'Yes'
alpha = alpha.append(alpha2)

fig, ax = plt.subplots(figsize=(3.39, 2.5))
pal = sb.color_palette('Pastel1')
pal = pal.as_hex()

sb.pointplot(y=0, x='experiment', hue='Hidden included',
             markers='o',
             linestyles=['-', 'dotted'],
             dodge=0.2,
             errwidth=2,
             data=alpha.query("type == 'rating'"), palette='Set1', ax=ax)

sb.pointplot(y=0, x='experiment', hue='Hidden included',
             markers='*',
             linestyles=['-', 'dotted'],
             dodge=0.2,
             errwidth=2,
             data=alpha.query("type == 'rank'"), palette='Set1', ax=ax)

plt.setp(ax.artists, alpha=0.3)
ax.set_ylabel("Krippendorff's alpha")
ax.set_ylim(0.25, 0.9)
ax.set_xticklabels(['Interference', 'Quality'])
ax.set_xlabel('Task')
ax.legend_.remove()
ax.text(0.0, 0.5, 'Hidden stimuli excluded', color=pal[0], fontsize=8)
ax.text(0.3, 0.73, 'Hidden stimuli included', color=pal[1], fontsize=8)

sb.despine()
plt.tight_layout()
plt.savefig('./paper/images/inter-rater_agreement.png', dpi=300)
plt.show()
