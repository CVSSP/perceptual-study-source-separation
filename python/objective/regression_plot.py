import os
import argparse
import listen as ln
from collections import namedtuple
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy


def fit(g, medians):
    '''
    Uses linear regression to fits the objective predictions to the
    subjective medians using linear regression.
    '''

    Fit = namedtuple('Fit', 'r rmse target fitted residuals')

    ratings = medians[medians.experiment.isin(g.experiment)]
    ratings = ratings['normalised_rating'].values
    out = scipy.stats.linregress(g['score'], ratings)
    fitted = out.slope * g['score'] + out.intercept
    n = len(fitted)
    p = 2  # Degrees of freedom

    return Fit(out.rvalue,
               np.sqrt(np.sum((fitted - ratings)**2) / (n - p)),
               ratings,
               fitted,
               ratings - fitted)


def fit_metrics(path_to_measures,
                path_to_ratings):

    predictions = pd.read_csv(path_to_measures)

    # Subjective ratings, remove hidden stimuli
    ratings = pd.read_csv(path_to_ratings)
    ratings = ratings.query("~sound.isin(['ref', 'Interferer', 'Quality'])")

    # Sort the two dataframes
    predictions = predictions.sort_values(
        by=['metric', 'experiment', 'page', 'sound'])

    medians = ln.mushra.average(ratings, 'median')
    medians = medians.sort_values(
        by=['experiment', 'page', 'sound'])

    print('Pearson correlation and RMSE for each metric')
    out = {}
    for metric in predictions.groupby('metric'):
        tmp = fit(metric[1], medians)
        out[metric[0]] = tmp

        print("Metric: {} r: {} RMSE: {}".format(metric[0], tmp.r, tmp.rmse))

    return out


def paper_plot(fits, image_dir):

    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    colors = sb.color_palette("PuOr", 10)

    sb.regplot(x=fits['APS'].target, y=fits['APS'].fitted,
               fit_reg=False,
               color=colors[2],
               ax=ax,
               label='APS',
               )

    sb.regplot(x=fits['SAR'].target, y=fits['SAR'].fitted,
               fit_reg=False,
               color=colors[6],
               marker='^',
               ax=ax,
               label='APS',
               )

    handles, labels = ax.get_legend_handles_labels()
    labels[0] = ('APS: $r$ = {r:.{digits}f} RMSE = {rmse:.{digits}f}'
                 .format(r=fits['APS'].r, rmse=fits['APS'].rmse, digits=2))

    labels[1] = ('SAR: $r$ = {r:.{digits}f}  RMSE = {rmse:.{digits}f}'
                 .format(r=fits['SAR'].r, rmse=fits['SAR'].rmse, digits=2))

    ax.legend(handles, labels, loc='upper left')

    ax.plot([-20, 100], [-20, 100], '--',
            color='0.25', zorder=-3, linewidth=0.5)
    plt.xlim(0, 90)
    plt.ylim(0, 90)
    plt.ylabel('Fitted objective rating')
    plt.xlabel('Median subjective rating')

    ticks = np.arange(0, 85, 10)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    sb.despine(offset=0)
    plt.tight_layout(pad=0.2)

    plt.savefig(os.path.join(image_dir, 'subjective_vs_sar_aps.pdf'))
    plt.show()


def poster_plot(fits, image_dir, style='poster.mplstyle'):
    plt.style.use(style)

    for task, combo in zip(['Sound quality', 'Interference'],
                           [('APS', 'SAR'), ('IPS', 'SIR')]):

        peass, bss = combo

        fig, ax = plt.subplots(figsize=(10, 10))
        colors = sb.color_palette("PuOr", 10)

        sb.regplot(x=fits[peass].target,
                   y=fits[peass].fitted,
                   fit_reg=False,
                   color=colors[2],
                   ax=ax,
                   label='APS',
                   scatter_kws={'s': 300},
                   )

        sb.regplot(x=fits[bss].target,
                   y=fits[bss].fitted,
                   fit_reg=False,
                   color=colors[6],
                   marker='^',
                   ax=ax,
                   label='APS',
                   scatter_kws={'s': 300},
                   )

        handles, labels = ax.get_legend_handles_labels()
        labels[0] = (
            '{}: $r$ = {r:.{digits}f} RMSE = {rmse:.{digits}f}'
            .format(peass, r=fits[peass].r, rmse=fits[peass].rmse, digits=2)
        )

        labels[1] = (
            '{}: $r$ = {r:.{digits}f}  RMSE = {rmse:.{digits}f}'
            .format(bss, r=fits[bss].r, rmse=fits[bss].rmse, digits=2)
        )

        ax.legend(handles, labels, loc='upper left')

        ax.text(50, 10, task, color='#1b656d', fontsize=40)

        ax.plot([-20, 100], [-20, 100], '--',
                color='0.1', zorder=-3, linewidth=1)
        plt.xlim(0, 95)
        plt.ylim(0, 95)
        plt.ylabel('Fitted objective rating')
        plt.xlabel('Median subjective rating')

        ticks = np.arange(0, 100, 10)
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        sb.despine(offset=0)
        plt.tight_layout(pad=0.2)

        plt.savefig(os.path.join(image_dir,
                                 'subjective_vs_{}_{}.png'.format(peass, bss)),
                    dpi=100)
        plt.show()


def main(measures, ratings, image_dir, poster):

    fits = fit_metrics(measures, ratings)

    if poster:
        poster_plot(fits, image_dir)
    else:
        paper_plot(fits, image_dir)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--poster', dest='poster', action='store_true',
                        default=False)
    args = parser.parse_args()

    if args.poster:
        image_dir = './site/images'
    else:
        image_dir = './paper/images'

    main(measures='./data/bss_eval_and_peass_clean.csv',
         ratings='./data/ratings.csv',
         image_dir=image_dir,
         poster=args.poster)
