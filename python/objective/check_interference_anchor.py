from untwist import data
import pandas as pd
import os


def main(stimulus_folder):

    x = [_ for _ in os.walk(stimulus_folder)]
    page_names = x[0][1]

    frame = pd.DataFrame(columns=['RelLoudness'],
                         index=page_names)

    for i, page in enumerate(page_names):

        ref_path = '{0}/{1}/{2}'.format(stimulus_folder,
                                        page,
                                        'ref.flac')

        accomp_path = '{0}/{1}/{2}'.format(stimulus_folder,
                                           page,
                                           'ref_accompaniment.flac')

        accomp = data.audio.Wave.read(accomp_path)
        ref = data.audio.Wave.read(ref_path)

        frame.iloc[i] = ref.loudness - accomp.loudness

    print(frame)


if __name__ == '__main__':

    main(stimulus_folder='./site/sounds')
