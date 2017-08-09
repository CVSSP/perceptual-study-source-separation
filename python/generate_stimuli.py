import pandas as pd
import numpy as np
import masseval


def main():

    # masseval side
    masseval.config.mus_base_path = '/vol/vssp/maruss/data2/MUS2017'
    masseval.config.dsd_base_path = '/vol/vssp/maruss/data2/DSD100'
    audio_dir = '/scratch/stimuli'
    df = masseval.data.get_sisec_df()

    # Remove accompaniment
    df = df.query("target != 'accompaniment'")

    # config for selection
    only_these_algos = ['GRA3', 'KON', 'OZE', 'UHL3', 'NUG3']
    targets = ['vocals', 'bass', 'other', 'drums']
    metrics = ['SAR', 'SIR']
    num_tracks_per_metric = 2
    target_loudness = -30
    segment_duration = 7
    include_background_in_quality_anchor=False
    remove_outliers = False

    # Main processing
    full_test = pd.DataFrame()
    for target in targets:
        exclude_tracks = [] # Don't select the same source twice
        for metric in metrics:

            sample = masseval.data.get_sample(
                df,
                num_tracks=num_tracks_per_metric,
                num_algos=len(only_these_algos),
                metric=metric,
                target=target,
                only_these_algos=only_these_algos,
                exclude_tracks=exclude_tracks,
                remove_outliers=remove_outliers,
                selection_plot=False,
            )

            tracks = sample['track_id'].values
            exclude_tracks = np.append(exclude_tracks, np.unique(tracks))
            full_test = pd.concat([full_test, sample])

            # Store the test wav files
            masseval.audio.write_target_from_sample(
                sample,
                target=target,
                directory=audio_dir,
                force_mono=True,
                target_loudness=target_loudness,
                segment_duration=segment_duration,
                include_background_in_quality_anchor=include_background_in_quality_anchor
                )

    #frames.to_csv('../data/stimuli.csv', index=None)


if __name__ == '__main__':

    main()
