import numpy as np
import scipy
import listen
import pandas as pd
import seaborn as sb
import argparse
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['text.usetex'] = True


def get_values(subjective, objective, col='normalised_rating'):
    '''
    This functions sorts subjective ratings and model predictions by sound
    and returns the values.
    '''

    objective = objective.sort_values(by='sound')
    subjective = (
        subjective[subjective.experiment.isin(objective.experiment) &
                   subjective.page.isin(objective.page)]
        .sort_values(by='sound')
    )

    return subjective['normalised_rating'].values, objective['score'].values


def spearman(x, y):
    return scipy.stats.spearmanr(*get_values(x, y))[0]


def correlate(path_to_ratings='./data/ratings.csv',
              path_to_measures='./data/bss_eval_and_peass_clean.csv',
              ):

    # Load subjective data
    ratings = pd.read_csv(path_to_ratings)

    # Drop hidden stimuli from ratings
    ratings = ratings.query("~sound.isin(['ref', 'Quality', 'Interferer'])")

    median_rating = listen.mushra.average(ratings, 'median')

    measures = pd.read_csv(path_to_measures)
    corrs = measures.groupby(['experiment', 'metric', 'page']).agg(
        lambda g: spearman(median_rating, g)
    ).reset_index(name='corr')

    return corrs


def paper_plot(corrs, filename):

    fig, ax = plt.subplots(figsize=(3.3, 3.0))

    colors = sb.color_palette("PRGn")

    order = ['APS', 'TPS', 'SAR', 'ISR', 'SIR', 'IPS']
    sb.boxplot(y='metric', x='corr',
               order=order,
               dodge=False,
               data=corrs,
               whis=0,
               fliersize=0,
               ax=ax,
               )

    # iterate over boxes
    for i, box in enumerate(ax.artists):
        box.set_edgecolor('black')
        box.set_facecolor('white')

    # Add some small jitter
    np.random.seed(1111)
    corrs['corr'] += np.random.uniform(-0.01, 0.01, size=len(corrs))

    sb.swarmplot(y='metric', x='corr',
                 data=corrs.query("experiment == 'quality'"),
                 order=order,
                 size=4,
                 dodge=True,
                 marker='o',
                 ax=ax,
                 color=colors[1],
                 label='Quality',
                 )

    sb.swarmplot(y='metric', x='corr',
                 data=corrs.query("experiment == 'interferer'"),
                 order=order,
                 size=4,
                 dodge=True,
                 marker='X',
                 ax=ax,
                 color=colors[4],
                 label='Interference',
                 )

    handles, labels = ax.get_legend_handles_labels()
    handles = [handles[0], handles[-1]]
    labels = ['Sound quality', 'Interference']
    ax.legend(handles, labels, loc='lower left', title='Task')

    labels = [
        'APS\n' + r'\scriptsize{PEASS}',
        'TPS\n' + r'{\scriptsize PEASS}',
        'SAR\n' + r'{\scriptsize BSS Eval}',
        'ISR\n' + r'{\scriptsize BSS Eval}',
        'SIR\n' + r'{\scriptsize BSS Eval}',
        'IPS\n' + r'{\scriptsize PEASS}'
    ]

    ax.set_yticklabels(labels, ha='right')

    plt.ylabel('')
    plt.xlabel('Spearman correlation')
    sb.despine(offset=10)
    plt.tight_layout(pad=0.2)
    plt.savefig(filename)
    plt.show()


def poster_plot(corrs, filename, style='poster.mplstyle'):
    plt.style.use(style)

    # Subset for poster
    corrs = corrs.query("metric.isin(['APS', 'SAR', 'SIR', 'IPS'])")

    fig, ax = plt.subplots(figsize=(11, 6))

    colors = sb.color_palette("PRGn")

    order = ['APS', 'SAR', 'SIR', 'IPS']
    sb.boxplot(y='metric', x='corr',
               order=order,
               dodge=False,
               data=corrs,
               whis=0,
               fliersize=0,
               ax=ax,
               )

    # iterate over boxes
    for i, box in enumerate(ax.artists):
        box.set_edgecolor('black')
        box.set_facecolor('white')

    # Add some small jitter
    np.random.seed(1111)
    corrs['corr'] += np.random.uniform(-0.01, 0.01, size=len(corrs))

    sb.swarmplot(y='metric', x='corr',
                 data=corrs.query("experiment == 'quality'"),
                 order=order,
                 size=15,
                 dodge=True,
                 marker='o',
                 ax=ax,
                 color=colors[1],
                 label='Quality',
                 )

    sb.swarmplot(y='metric', x='corr',
                 data=corrs.query("experiment == 'interferer'"),
                 order=order,
                 size=15,
                 dodge=True,
                 marker='X',
                 ax=ax,
                 color=colors[4],
                 label='Interference',
                 )

    handles, labels = ax.get_legend_handles_labels()
    handles = [handles[0], handles[-1]]
    labels = ['Sound quality', 'Interference']
    leg = ax.legend(handles, labels, loc='lower left', title='Task')
    plt.setp(leg.get_texts(), color='#1b656d')

    labels = [
        'APS\n' + r'\huge{PEASS}',
        'SAR\n' + r'\huge{BSS Eval}',
        'SIR\n' + r'\huge{BSS Eval}',
        'IPS\n' + r'\huge{PEASS}'
    ]

    ax.set_yticklabels(labels, ha='right')

    plt.ylabel('')
    plt.xlabel('Spearman correlation')
    sb.despine(offset=10)
    plt.tight_layout(pad=0.2)
    plt.savefig(filename, dpi=100)
    plt.show()


def main(path_to_ratings,
         path_to_measures,
         image_name,
         poster=False
         ):

    corrs = correlate(path_to_ratings, path_to_measures)

    print('Median of within-song Spearman correlations')
    print(corrs.groupby('metric').median())

    if poster:
        poster_plot(corrs, image_name)
    else:
        paper_plot(corrs, image_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--poster', dest='poster', action='store_true',
                        default=False)
    args = parser.parse_args()

    if args.poster:
        image_name = './paper/poster/resources/spearman_boxplot.png'
    else:
        image_name = './paper/images/spearman_boxplot.pdf'

    main(path_to_ratings='./data/ratings.csv',
         path_to_measures='./data/bss_eval_and_peass_clean.csv',
         image_name=image_name,
         poster=args.poster)
