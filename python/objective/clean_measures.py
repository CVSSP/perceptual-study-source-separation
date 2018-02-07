import pandas as pd


def main(expected_metrics_only=True):

    for filename in ["./data/bss_eval_and_peass.csv",
                     "./data/bss_eval_and_peass_all_stems.csv",
                     "./data/bss_eval_and_peass_nonorm_all_stems.csv"]:

        # Load subjective data
        ratings = pd.read_csv("./data/ratings.csv")

        # Load model predictions
        predictions = pd.read_csv(filename)

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
        predictions = predictions.melt(
            id_vars=['experiment', 'page', 'sound'],
            value_vars=['SAR', 'ISR', 'SIR', 'APS', 'TPS', 'IPS'],
            var_name='metric',
            value_name='score',
        )

        if expected_metrics_only:
            predictions = predictions.query(
                ("metric == 'SAR' and experiment == 'quality' or "
                 "metric == 'APS' and experiment == 'quality' or "
                 "metric == 'ISR' and experiment == 'quality' or "
                 "metric == 'TPS' and experiment == 'quality' or "
                 "metric == 'SIR' and experiment == 'interferer' or "
                 "metric == 'IPS' and experiment == 'interferer'")
            )

        predictions = predictions.sort_values(
            by=['experiment', 'page', 'sound', 'metric'])

        predictions.to_csv(filename[:-4] + '_clean.csv', index=None)


if __name__ == '__main__':

    main()
