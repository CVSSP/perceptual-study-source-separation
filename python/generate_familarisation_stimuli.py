import pandas as pd
import numpy as np
from untwist import (data, utilities)
import masseval
import yaml
import os
import shutil


if __name__ == '__main__':

    '''
    Generates stimuli for the soundboard on the familiarisation page of the
    introduction to the listening test. Its goal is to demonstarte the
    difference between sound quality and interference.
    '''

    masseval.config.dsd_base_path = '/vol/vssp/maruss/data2/DSD100'
    audio_dir = 'sounds_familiarisation/'
    config_file = ['./site/_data/quality_familiarisation.yaml',
                   './site/_data/interference_familiarisation.yaml']

    # Create folder for training stimuli
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, '../site/', audio_dir)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

    # Take the development set as we don't use this in the main test
    df = masseval.data.get_dsd100_df()
    df = df[df.test_set == 0]

    # Pick some songs at random and get stems
    num_songs = 1
    titles = pd.unique(df.title)
    selected = ['Bulldozer']
    df = df[df.title.isin(selected) & (df.audio != 'mixture')]

    # Loudness balance params, where 0dB is the ref
    target_source = 'vocals'
    levels = [0, -6, -12, -18]
    labels = ['Reference', 'A', 'B', 'C']

    # Audio quality params, just generate 3 because we have our reference
    trim_factor_distorted = [0.1, 0.2, 0.4]
    trim_factor_artefacts = [0.99, 0.99, 0.99]
    balances = [[0, -24], [0, -16], [0, -6]]
    anchor_types = ['fair', 'poor', 'bad']

    # Target loudness for all mixes
    target_loudness = -26

    '''
    Create the config files
    '''

    song_idx = stim_idx = 0
    for title, song in df.groupby('title'):

        new_config = {
                'continuous_playback': True,
                'loop_playback': True,
                'rows': [
                    {'name':
                     "All of these have the same quality as the reference because the other instruments do not affect sound quality",
                     'sounds': []},
                    {'name':
                     "In this example the sound quality is degraded by introducing artefacts and distortions",
                     'sounds': []},
                ]}

        # Grab audio for this song, mono and segment as per the experiment
        target = song[song.audio == target_source]
        others = song[song.audio != target_source]

        target = data.audio.Wave.read(
            target['audio_filepath'].values[0]).as_mono()

        start, end = masseval.audio.find_active_portion(target, 7, 75)
        target = masseval.audio.segment(target, start, end)

        # Stim non-target instruments
        stems = []
        for idx, other in others.iterrows():
            stem = data.audio.Wave.read(other['audio_filepath']).as_mono()
            stems.append(masseval.audio.segment(stem, start, end))

        mix = sum(stems)

        # Create our mixes with changes in relative loudness
        for i, level in enumerate(levels):

            # 0dB has the special meaning of no mix in this case
            if (i == 0):
                mix_tmp = target
            else:
                mix_tmp = target + mix * utilities.conversion.db_to_amp(level)

            mix_tmp.loudness = target_loudness

            filename = '{0}dB-{1}.wav'.format(level, title)
            masseval.audio.write_wav(mix_tmp, path + filename, target_loudness)

            new_config['rows'][0]['sounds'].append(
                {'button_label': labels[i],
                 'url': audio_dir + filename}
            )

            # Store the target as reference
            if (i == 0):
                ref = mix_tmp

            stim_idx += 1

        # Now create artefacts, here were add the reference again
        new_config['rows'][1]['sounds'].append(
            {'button_label': labels[0],
             'url': audio_dir + '0dB-{}.wav'.format(title)}
        )

        stim_idx += 1

        for trim_d, trim_a, balance, anchor_type, label in zip(trim_factor_distorted,
                                                               trim_factor_artefacts,
                                                               balances,
                                                               anchor_types,
                                                               labels[1:]):

            creator = masseval.anchor.RemixAnchor(ref,
                                                  0.0,
                                                  trim_d,
                                                  trim_a,
                                                  0,
                                                  balance,
                                                  20000)

            anchor = creator.quality_anchor()
            filename = '{0}-{1}.wav'.format(anchor_type, title)
            masseval.audio.write_wav(anchor, path + filename, target_loudness)

            new_config['rows'][1]['sounds'].append(
                {'button_label': label,
                 'url': audio_dir + filename}
            )

            stim_idx += 1

        # Write config file for this soundboard (song)
        with open(config_file[0], 'w') as f:
            yaml.dump(new_config,
                      f,
                      default_flow_style=False)

        new_config['rows'][0], new_config['rows'][1] = new_config['rows'][1], new_config['rows'][0]
        new_config['rows'][0]['name'] = 'All of these have no interference from other instruments despite the sound quality being different'
        new_config['rows'][1]['name'] = 'In this example the amount of interference is changed by varying the relative loudness of the backing instruments'
        with open(config_file[1], 'w') as f:
            yaml.dump(new_config,
                      f,
                      default_flow_style=False)



        song_idx += 1
