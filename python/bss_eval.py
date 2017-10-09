import os

import pandas as pd
import numpy as np

import soundfile as sf
import matlab.engine
from mir_eval import separation
from tempfile import TemporaryDirectory


def df_experiment(input_filename):

    df = pd.read_csv(input_filename)

    df = df.drop(['is_dev', 'target_id', 'method_id', 'metric_id',
                  'title', 'genre', 'filename', 'filepath'],
                 axis=1)

    df = df.loc[df['target'] == 'vocals']
    df = df.loc[df['method'] != 'ref']

    df['SAR'] = np.nan
    df['SIR'] = np.nan
    df['APS'] = np.nan
    df['TPS'] = np.nan
    df['IPS'] = np.nan

    return df


def reference_files(path, audio_format='flac'):
    vocal = path + 'ref.' + audio_format.lower()
    mix = path + 'Interferer.' + audio_format.lower()
    return vocal, mix


def estimated_file(path, method, audio_format='flac'):
    estimated_vocal = path + method + "." + audio_format
    return estimated_vocal


def bss_eval(reference_sources, estimated_target, audio_format='flac'):

    s_true, e_spat, e_interf, e_artif = \
        separation._bss_decomp_mtifilt(reference_sources,
                                       estimated_target,
                                       0, 512)
    sdr, sir, sar = \
        separation._bss_source_crit(s_true, e_spat, e_interf, e_artif)
    return sir, sar


def peass(reference_files, estimated_file, path_to_peass_toolbox):

    m = matlab.engine.start_matlab()
    m.eval("addpath(genpath('{}'));".format(path_to_peass_toolbox))

    with TemporaryDirectory() as tmp_dir:
        options = {'destDir': tmp_dir, 'segmentationFactor': 1}
        result = m.PEASS_ObjectiveMeasure(reference_files,
                                          estimated_file,
                                          options)

    ips = result['IPS']
    aps = result['APS']
    tps = result['TPS']

    return ips, aps, tps


def main(peass_path):

    audio_format = 'flac'
    pwd = os.path.dirname(os.path.realpath(__file__))
    result_file = pwd + '/../data/bss_eval_and_peass.csv'
    experiment_file = pwd + '/../data/experiment_stimuli.csv'
    stim_path = pwd + '/../site/sounds/'

    df = df_experiment(experiment_file)
    df['task'] = 'quality'

    for _, track_df in df.groupby('track_id'):

        path = '{}{}-{}-{}/'.format(stim_path,
                                    track_df['target'].iloc[0],
                                    track_df['track_id'].iloc[0],
                                    track_df['metric'].iloc[0])
        vocal_file, mix_file = reference_files(path, audio_format)
        vocal, _ = sf.read(vocal_file)
        mix, _ = sf.read(mix_file)
        interferer = mix - vocal
        ref_sources = np.array([vocal, interferer])

        for idx, row in track_df.iterrows():

            est_file = estimated_file(path, row['method'], audio_format)
            est_target, _ = sf.read(est_file)

            sir, sar = bss_eval(ref_sources, est_target)
            ips, aps, tps = peass([vocal_file, mix_file], est_file, peass_path)

            df.loc[idx, 'SAR'] = sar
            df.loc[idx, 'APS'] = aps
            df.loc[idx, 'TPS'] = tps
            df.loc[idx, 'SIR'] = sir
            df.loc[idx, 'IPS'] = ips

    df2 = df.copy()
    df2['task'] = 'interferer'

    df = pd.concat([df, df2])
    df.to_csv(result_file, index=None)


peass_path = '/user/HS203/hw0016/git/maruss/peass-software'
main(peass_path)
