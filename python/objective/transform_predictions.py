import pandas as pd


# Load subjective data
ratings = pd.read_csv("./data/ratings.csv")

# Load model predictions
predictions = pd.read_csv("./data/bss_eval_and_peass.csv")

# Drop first half
# predictions = predictions.query("task == 'quality'")

# don't need these columns
predictions = predictions.drop(['metric', 'score', 'target'], axis=1)

# Rename needed columns to match subjective dataframe
predictions = predictions.rename(columns={'track_id': 'page',
                                          'target': 'target',
                                          'method': 'sound',
                                          'task': 'experiment',
                                          }
                                 )

# Rename pages
pages = pd.unique(ratings['page'])
sound_id = [_.split('-')[1] for _ in pages]

for i, row in predictions.iterrows():
    j = sound_id.index(str(row['page']))
    predictions.ix[i, 'page'] = pages[j]

# Wide to long
predictions = predictions.melt(id_vars=['experiment', 'page', 'sound'],
                               value_vars=['SAR', 'SIR', 'APS', 'TPS', 'IPS'],
                               var_name='metric',
                               value_name='score',
                               )

'''
# Associate metrics with correct experiment
#predictions['experiment'] = 'quality'
predictions.loc[
    predictions.metric.isin(['SIR', 'IPS']),
    'experiment'] = 'interferer'
'''

predictions = predictions.sort_values(
    by=['experiment', 'page', 'sound', 'metric'])

predictions.to_csv('./data/predictions.csv', index=None)
