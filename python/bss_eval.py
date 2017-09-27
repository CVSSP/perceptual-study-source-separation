import pandas as pd
import numpy as np
import soundfile as sf
from mir_eval import separation
# from scipy.signal import butter, lfilter


def condition_df(input_filename='../data/experiment_stimuli.csv'):

    df = pd.read_csv(input_filename)

    df = df.drop(['is_dev', 'target_id', 'method_id', 'metric_id',
                  'title', 'genre', 'filename', 'filepath'],
                 axis=1)

    df = df.loc[df['target'] == 'vocals']
    df = df.loc[df['method'] != 'ref']

    df['eval_metric'] = 'SAR'
    df['measure'] = np.nan
    df['task'] = 'quality'

    df2 = df.copy()
    df2['eval_metric'] = 'SIR'
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


def reference_sources(path, audio_format='flac'):
    vocal, fs = sf.read(path + "ref." + audio_format)
    mix, fs = sf.read(path + "Interferer." + audio_format)
    interferer = mix - vocal
    return np.array([vocal, interferer])


def estimated_target(path, method, audio_format='flac'):
    estimated_vocal, fs = sf.read(path + method + "." + audio_format)
    # estimated_vocal = lowpass(estimated_vocal, 2000, SAMPLERATE)
    return estimated_vocal

def bss_eval(reference_sources, estimated_target):
    s_true, e_spat, e_interf, e_artif = \
        separation._bss_decomp_mtifilt(reference_sources,
                                       estimated_target,
                                       0, 512)
    sdr, sir, sar = \
        separation._bss_source_crit(s_true, e_spat, e_interf, e_artif)
    return sir, sar

def main(stim_path='../site/sounds/'):

    df = condition_df()

    quality_df = df.query("task == 'quality'").copy()
    interferer_df = df.query("task == 'interferer'").copy()

    for _, track_df in quality_df.groupby('track_id'):

        path = '{}{}-{}-{}/'.format(stim_path,
                                    track_df['target'].iloc[0],
                                    track_df['track_id'].iloc[0],
                                    track_df['metric'].iloc[0])
        ref_sources = reference_sources(path, 'wav')
        print(path)

        for idx, row in track_df.iterrows():

            est_target = estimated_target(path, row['method'], 'wav')
            sir, sar = bss_eval(ref_sources, est_target)
            quality_df.loc[idx, 'measure'] = sar
            interferer_df.loc[idx, 'measure'] = sir

    df = pd.concat([quality_df, interferer_df])
    df.to_csv('test.csv', index=None)

main()

# sf.write("s_target.flac", s_true + e_spat, SAMPLERATE)
# sf.write("e_interf.flac", e_interf, SAMPLERATE)
# sf.write("e_artif.flac", e_artif, SAMPLERATE)
