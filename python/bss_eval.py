import pandas as pd
import numpy as np
import soundfile as sf
import matlab.engine
from mir_eval import separation
from tempfile import TemporaryDirectory
# from scipy.signal import butter, lfilter


def condition_df(input_filename='../data/experiment_stimuli.csv'):

    df = pd.read_csv(input_filename)

    df = df.drop(['is_dev', 'target_id', 'method_id', 'metric_id',
                  'title', 'genre', 'filename', 'filepath'],
                 axis=1)

    df = df.loc[df['target'] == 'vocals']
    df = df.loc[df['method'] != 'ref']

    df['eval_metric'] = 'SAR'
    df['eval_score'] = np.nan
    df['peass_metric'] = 'APS'
    df['peass_score'] = np.nan
    df['task'] = 'quality'

    df2 = df.copy()
    df2['eval_metric'] = 'SIR'
    df2['peass_metric'] = 'IPS'
    df2['task'] = 'interferer'

    df = pd.concat([df, df2])

    return df


# def butter_lowpass(cutoff, fs, order=4):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff / nyq
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     return b, a
#
# def lowpass(data, cutoff, fs, order=4):
#     b, a = butter_lowpass(cutoff, fs, order=order)
#     y = lfilter(b, a, data)
#     return y


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

    return ips, aps


def main(stim_path='../site/sounds/'):

    audio_format = 'flac'
    result_file = '../data/bss_eval_and_peass.csv'

    df = condition_df()

    quality_df = df.query("task == 'quality'").copy()
    interferer_df = df.query("task == 'interferer'").copy()

    for _, track_df in quality_df.groupby('track_id'):

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
            ips, aps = peass([vocal_file, mix_file],
                             est_file,
                             '/user/HS203/hw0016/git/maruss/peass-software')

            quality_df.loc[idx, 'eval_score'] = sar
            quality_df.loc[idx, 'peass_score'] = aps
            interferer_df.loc[idx, 'eval_score'] = sir
            interferer_df.loc[idx, 'peass_score'] = ips

    df = pd.concat([quality_df, interferer_df])
    df.to_csv(result_file, index=None)

main()

# sf.write("s_target.flac", s_true + e_spat, SAMPLERATE)
# sf.write("e_interf.flac", e_interf, SAMPLERATE)
# sf.write("e_artif.flac", e_artif, SAMPLERATE)
