import matplotlib.pyplot as plt
from untwist import data
import soundfile as sf
import numpy as np
import pandas as pd
import os



def main(stimulus_folder,
         filename=None):

    x = [_ for _ in os.walk(stimulus_folder)]
    page_names = x[0][1]

    frame = pd.DataFrame(columns=['RelLoudness'],
                         index=page_names)

    for i, page in enumerate(page_names):

        ref_path = '{0}/{1}/{2}'.format(stimulus_folder,
                                        page,
                                        'ref.wav')

        accomp_path = '{0}/{1}/{2}'.format(stimulus_folder,
                                           page,
                                           'ref_accompaniment.wav')

        ref, fs = sf.read(ref_path)
        accomp, fs = sf.read(accomp_path)

        accomp = data.audio.Wave(accomp, fs)
        ref = data.audio.Wave(ref, fs)

        frame.iloc[i] = ref.loudness - accomp.loudness

    print(frame)


if __name__ == '__main__':


    main(stimulus_folder='./site/sounds',
         filename='./site/_data/interferer_anchor_balances.csv')
