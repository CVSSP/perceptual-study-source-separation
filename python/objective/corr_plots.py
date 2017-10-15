import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


corrs = pd.read_csv('./data/correlations.csv')

fig, ax = plt.subplots(figsize=(3.39, 3.39))

red, blue = sb.xkcd_rgb["pale red"], sb.xkcd_rgb["denim blue"]

sb.boxplot(y='metric', x='corr', hue='experiment',
           dodge=False,
           data=corrs.query("corr_type == 'spearman'"),
           whis=0,
           fliersize=0,
           ax=ax,
           )

# iterate over boxes
for i,box in enumerate(ax.artists):
    box.set_edgecolor('black')
    box.set_facecolor('white')

sb.swarmplot(y='metric', x='corr',
             data=corrs.query("corr_type == 'spearman' & experiment == 'quality'"),
             marker='o',
             ax=ax,
             color=red,
             label='Quality',
             )

sb.swarmplot(y='metric', x='corr',
             data=corrs.query("corr_type == 'spearman' & experiment == 'interferer'"),
             marker='^',
             ax=ax,
             color=blue,
             label='Interference',
             )

handles, labels = ax.get_legend_handles_labels()
handles = [handles[2], handles[7]]
labels = [labels[2], labels[7]]
ax.legend(handles, labels, title='Task')
ax.legend_.remove()

plt.ylabel('')
plt.xlabel('Spearman correlation')
sb.despine(left=True)
plt.tight_layout()
plt.savefig('./paper/images/spearman_boxplot.png', dpi=300)
plt.show()


'''
    sb.boxplot(x='metric', y='corr',
            data=corrs.query("experiment == 'interferer' & corr_type == 'pearson'"),
            )

    plt.ylabel('pearson r')
    plt.title('Interference')
    plt.show()


    # Average by algorithm
    x = predictions.query("metric == 'IPS' & experiment == 'interferer'")
    y = median_rating.query("experiment == 'interferer'")

    x = x.groupby('sound')['score'].mean()
    y = y.groupby('sound')['normalised_rating'].mean()

    print(stats.pearsonr(x, y))
    print(stats.spearmanr(x, y))

    #plt.plot(x, y, 'o')
    sb.regplot(x, y)
    plt.ylabel('Subjective rating')
    plt.xlabel('PEASS: IPS')
    plt.title('Interferer - Algorithm averages')
    plt.show()

    sub1 = ratings.query("experiment == 'quality' & page == 'vocals-26-SIR'")
    sub1 = sub1.sort_values(by='sound')

    pred = predictions.query("metric == 'APS' & page == 'vocals-26-SIR' & experiment == 'quality'")
    pred = pred.sort_values(by='sound')
    fig, ax = plt.subplots(2, 1)
    sb.boxplot(x='sound', y='normalised_rating',
            ax=ax[0],
            data=sub1)
    ax[0].set_ylabel('Quality rating')

    sb.boxplot(x='sound', y='score',
            ax=ax[1],
            data=pred)
    ax[1].set_ylabel('PEASS: APS')

    plt.show()
'''
