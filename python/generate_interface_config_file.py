import os
import yaml


def main(stimuli_input_folder,
         stimuli_website_folder,
         ref_name='ref.wav',
         excluse_these_wav_files=[],
         labels=['Dissimilar', 'Similar'],
         filename=None):

    x = [_ for _ in os.walk(stimuli_input_folder)]
    page_names = x[0][1]
    sounds = [_[2] for _ in x[1:]]

    pages = []
    for page, page_sounds in zip(page_names, sounds):

        page_sounds = [_ for _ in page_sounds
                       if _ not in excluse_these_wav_files]

        sounds_list = []
        for sound in page_sounds:
            sounds_list.append(
                {'name': sound.strip('.wav'),
                 'url': '{0}/{1}/{2}'.format(stimuli_website_folder,
                                             page,
                                             sound)}
            )

        page_dict = {'name': page,
                     'reference_url': '{0}/{1}/{2}'.format(stimuli_website_folder,
                                                           page,
                                                           ref_name),
                     'sounds': sounds_list}

        pages.append(page_dict)

    config = {'continuous_playback': True,
              'loop_playback': True,
              'randomise_slider_handle': True,
              'randomise_sounds_within_page': True,
              'randomise_pages': True,
              'include_number_box': True,
              'must_play_all_samples_to_continue': True,
              'labels': labels,
              'pages': pages,
              }

    with open(filename, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)


if __name__ == '__main__':

    main(stimuli_input_folder='./experiment/sounds',
         stimuli_website_folder='sounds',
         ref_name='ref.wav',
         excluse_these_wav_files=['Artefacts.wav',
                                  'Distortion.wav'],
         labels=['Worse quality', 'Same quality'],
         filename='./experiment/_data/quality.yaml')

    main(stimuli_input_folder='./experiment/sounds',
         stimuli_website_folder='sounds',
         ref_name='ref.wav',
         excluse_these_wav_files=['Artefacts.wav',
                                  'Distortion.wav'],
         labels=['Much interference', 'No interference'],
         filename='./experiment/_data/interferer.yaml')
