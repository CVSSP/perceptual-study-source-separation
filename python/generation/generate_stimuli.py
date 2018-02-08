import pandas as pd
import numpy as np
import masseval


def main(dsd_path, mus_path):

    # masseval side
    masseval.config.mus_base_path = mus_path
    masseval.config.dsd_base_path = dsd_path

    exclude_tracks = experiment_stimuli(target_loudness=None,
                                        suffix='non_norm',
                                        overall_gain=-6)

    exclude_tracks = experiment_stimuli(target_loudness=-24)

    training(exclude_tracks)


def experiment_stimuli(target_loudness=-24, suffix=None, overall_gain=0):

    audio_dir = './site/sounds'

    # config for selection
    only_these_algos = None
    targets = ['vocals']
    metrics = ['SAR', 'SIR']
    num_algos = 5
    num_tracks_per_metric = [8, 8]
    segment_duration = 7
    remove_outliers = False
    trim_factor_distorted = 0.4

    df = masseval.data.get_sisec_df(False)

    # Main processing
    full_test = pd.DataFrame()
    for target in targets:
        exclude_tracks = [3]  # Song 3 has strange vocals

        exclude_algos_in_tracks = {'DUR': [11],
                                   'KON': [48]}
        song_start_and_end_times = {
                '10': [96.5],
                '12': [38.4],
                '24': [122.35],
                '25': [64.5],
                '45': [51.49],
                '47': [110]}

        for metric, num_tracks in zip(metrics, num_tracks_per_metric):

            sample = masseval.data.get_sample(
                df,
                num_tracks=num_tracks,
                num_algos=num_algos,
                metric=metric,
                target=target,
                only_these_algos=only_these_algos,
                exclude_tracks=exclude_tracks,
                remove_outliers=remove_outliers,
                selection_plot=False,
                exclude_algos_in_tracks=exclude_algos_in_tracks,
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
                song_start_and_end_times=song_start_and_end_times,
                segment_duration=segment_duration,
                trim_factor_distorted=trim_factor_distorted,
                include_background_in_quality_anchor=False,
                loudness_normalise_interferer=False,
                suffix=suffix,
                overall_gain=overall_gain,
                )

    full_test.to_csv('./data/experiment_stimuli.csv', index=None)

    return exclude_tracks


def training(exclude_tracks):

    # masseval side
    masseval.config.mus_base_path = '/vol/vssp/maruss/data2/MUS2017'
    masseval.config.dsd_base_path = '/vol/vssp/maruss/data2/DSD100'
    audio_dir = './site/sounds_training'

    # config for selection
    only_these_algos = ['GRA3', 'KON', 'OZE', 'UHL3', 'NUG3']
    # only_these_algos = None
    target = 'vocals'
    metric = 'SAR'
    num_algos = 5
    num_tracks = 1
    target_loudness = -30
    segment_duration = 7
    remove_outliers = False
    trim_factor_distorted = 0.4

    df = masseval.data.get_sisec_df(False)

    sample = masseval.data.get_sample(
        df,
        num_tracks=num_tracks,
        num_algos=num_algos,
        metric=metric,
        target=target,
        only_these_algos=only_these_algos,
        exclude_tracks=exclude_tracks,
        remove_outliers=remove_outliers,
        selection_plot=False,
    )

    # Store the test wav files
    masseval.audio.write_target_from_sample(
        sample,
        target=target,
        directory=audio_dir,
        force_mono=True,
        target_loudness=target_loudness,
        segment_duration=segment_duration,
        trim_factor_distorted=trim_factor_distorted,
        include_background_in_quality_anchor=False,
        loudness_normalise_interferer=False,
        )

    sample.to_csv('./data/training_stimuli.csv', index=None)


if __name__ == '__main__':

    main('/vol/vssp/maruss/data2/DSD100', '/vol/vssp/maruss/data2/MUS2017')
