import os
import pandas as pd
import numpy as np
import soundfile as sf
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


def reference_files(path, audio_format='wav', suffix=''):

    vocal = '{0}ref{1}.{2}'.format(path, suffix, audio_format.lower())
    accomp = '{0}ref{1}_accompaniment.{2}'.format(path, suffix,
                                                 audio_format.lower())
    return vocal, accomp


def estimated_file(path, method, audio_format='wav', suffix=''):
    estimated_vocal = ''.join((path, method, suffix,
                               '.' + audio_format.lower()))
    return estimated_vocal


def bss_eval(reference_sources, estimated_target, audio_format='wav'):

    s_true, e_spat, e_interf, e_artif = \
        separation._bss_decomp_mtifilt(reference_sources,
                                       estimated_target,
                                       0, 512)
    sdr, isr, sir, sar = \
        separation._bss_image_crit(s_true, e_spat, e_interf, e_artif)
    return sir, sar, isr


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


def main(peass_path='/vol/vssp/maruss/matlab_toolboxes/PEASS-Software-v2.0_audioread_compiled',
         experiment_file='./data/experiment_stimuli.csv',
         result_file='./data/bss_eval_and_peass.csv',
         suffix='',
         stim_path='./site/sounds/',
         audio_format='wav'
         ):

    df = df_experiment(experiment_file)
    df['task'] = 'quality'

    track_df = df.query("track_id == 18 & method == 'GRA3'")

    path = '{}{}-{}-{}/'.format(stim_path,
                                track_df['target'].iloc[0],
                                track_df['track_id'].iloc[0],
                                track_df['metric'].iloc[0])

    vocal_file, accomp_file = reference_files(path, audio_format, suffix)
    vocal, _ = sf.read(vocal_file)
    accomp, fs = sf.read(accomp_file)
    ref_sources = np.array([vocal, accomp])

    for idx, row in track_df.iterrows():

        est_file = estimated_file(path, row['method'],
                                    audio_format, suffix)
        est_target, _ = sf.read(est_file)

        sir, sar, isr = bss_eval(ref_sources, est_target)

        print(sir, sar, isr)


if __name__ == '__main__':

    for suffix, result_file in zip(
        [''],
        ['./data/bss_eval_and_peass.csv'],
    ):

        main(suffix=suffix,
             result_file=result_file)
