This is the repository for the paper:

```bibtex
@inproceedings{Ward_2018,
	year = 2018,
	month = {April},
	publisher = {{IEEE}},
	author = {Dominic Ward and Hagen Wierstorf and Russell D. Mason and Emad M. Grais and Mark D. Plumbley},
	title = {{{BSS EVAL or PEASS?} Predicting the Perception of Singing-Voice Separation}},
	booktitle = {2018 {IEEE} International Conference on Acoustics, Speech and Signal Processing ({ICASSP})}
}
```

which is available via [Surrey Research Insight Open Access](http://epubs.surrey.ac.uk/845998/).

# What's what?

- The website, hosted on GitHub pages, is in the `site` folder
- The submitted (raw) subjective ratings are in `site/_data/results`
- Audio files are in `site/sounds/`
- The source files and images for the paper are in the `paper` folder
- The content for the poster (as presented by Emad M. Grais at ICASSP 2018) is
    `site/_pages/poster.md`. Images, styling and layout are can be found at
    `site/images`, `site/assets/css/poster.scss` and `site/_layouts/poster.html`,
    respectively.
- Python code lives in the `python` folder

The experiment lives in the `site` folder, which is deployed to the `gh-pages`
branch via
```
git subtree push --prefix site origin gh-pages
```

Go to https://cvssp.github.io/perceptual-study-source-separation/ to see the
experiment and additional resources.

## Main data files you should care about

There are quite a few intermediate files and things left for future work.

In short, the main data are:

- `data/ratings.csv` is the compiled subjective dataset
- `data/experiment_stimuli.csv` describes the main audio files used in the 
    experiment
- `data/bss_eval_and_peass_clean.csv` the predictions of BSS Eval and PEASS

The stimuli used for the experiment can be found in the `./site/sounds` folder.
The `flac` files are provided, but we used original `wavs` for the lab
experiment and all objective measures. If you would like to generate the stimuli
yourself, read on.

# Python

Create and source the Python 3 virtual environment:
```
cd ./venvs
make
source py3/bin/active
```
In order to run the PEASS model, you will need to install the Matlab engine
inside the Python virtual environment. To do this, go to
`$MATLABROOT/extern/engines/python` and run:
```
python setup.py build --build-base=$HOME/tmp/build install
```

You should now be good to go. 

**All python scripts should be run from the root folder of the repository.**

## Generating the stimuli

### Datasets

`DSD100`: 
The demixing Secret Dataset dataset can be downloaded
[here](http://liutkus.net/DSD100.zip). This was used for the ground truth data,
i.e. the reference vocals and accompaniments.

`MUS2017`: 
For our analysis, we used the SiSEC submission data (~400 GB), which was kindly
provided by Fabian-Robert Stöter. You can contact me for the complete submission
data.

### Scripts

```
python/generation/generate_familarisation_stimuli.py
```
Generates the configuration files and audio files for the [quality familiarisation
page](https://cvssp.github.io/perceptual-study-source-separation/familiarisation_quality/)  and the [interference familiarisation page](https://cvssp.github.io/perceptual-study-source-separation/familiarisation_interferer/).
You will need to set the path, in the `main` function, to the demixing Secret
Dataset (DSD100) dataset, which can be downloaded [here](http://liutkus.net/DSD100.zip).

```
python/generation/generate_stimuli.py
```
This script generates all wav files for the training stages, e.g.
[here](https://cvssp.github.io/perceptual-study-source-separation/training_interferer/)
and the main experiment, e.g.
[here](https://cvssp.github.io/perceptual-study-source-separation/interferer/).
This includes the reference vocals and original accompaniment (required for
objective evaluation), the estimated vocals (from the algorithms) and the
anchors.  Audio files belonging to a single song are placed in their own folder,
e.g.  `./site/sounds/vocals-10-SIR` holds the audio associated with the vocals
of song 10.

The `main` function requires the path to `DSD100` and `MUS2017`.

Naming convention:

- The estimated files have been named as done [here](http://sisec17.audiolabs-erlangen.de/#/results/1/4/2). 
- The reference vocal is named `ref.flac`.
- The accompaniment (sum of other sources) associated with each reference vocal
    has the name `ref_accompaniment.flac`.
- `Artefacts.wav` is the sound-quality anchor.
- `Interferer.wav` is the original mixture.

Note:

Files with the suffix `non_norm` were **not** loudness normalised, nor were they
used for the listening test, so we haven't included these in the repository. The
purpose of these files was to investigate the sensitivity of PEASS to loudness
normalisation, which is not discussed in the paper.  Furthermore, files with
`drums`, `other` or `bass` in their name were not used (and thus not included)
but may be useful for future work.

The reference vocals, estimated vocals and anchors (without `non_norm` in the
filename) were loudness normalised according to ITU-R BS.1770-4. The
accompaniment signals, e.g. `ref_accompaniment.flac` were scaled by the same
gain factor used to loudness normalise the reference vocal, i.e.

```
mixture = gain_used_to_normalise_vocal * ref + gain_used_to_normalise_vocal * ref_accompaniment
```
In other words, the resulting mixture is just a scaled version of the original
mixture, where the loudness of the vocal matches that of the extracted vocals.

Finally, the above script also generates the csv files `data/experiment_stimuli.csv`
and `data/training_stimuli.csv`.

```
python/generation/generate_interface_config_file.py
```
Generates the configuration files required for each instance of the MUSHRA test
(training and main experiment).

## Subjective Data

```
python/subjective/compile_dataset.py
```
Compiles the ratings and stores them as a csv file named `./data/ratings.csv`.
The python module `from rename_subjects` is not provided, and was used to
preserve the anonymity of a few listeners who entered their name when
submitting. You will still be able to run this script, but shouldn't need to.

```
python/subjective/concordance.py
```
Plots the concordance coefficients and prints out other measures of agreement
(sort of) for each task, based on the replicated trials. This is the script used
for the first paragraph of section 3.1 of the paper.

```
python/subjective/hidden_sounds_swarmplot.py
```
Generates the Bee Swarm plot shown in Figure 1 of the paper.

```
python/subjective/kripperndorffs_alpha.py.py
```

Measures of inter-rater reliability as reported in paragraph 3 of the paper
(thanks to [kripperndorff-alpha](https://github.com/grrrr/krippendorff-alpha)
for the python implementation).

## Objective Data

```
python/objective/compute_objective_measures.py
```
Computes the objective measures according to [BSS
Eval](http://bass-db.gforge.inria.fr/bss_eval/) and
[PEASS](http://bass-db.gforge.inria.fr/peass/PEASS-Software.html). We are
essentially using
[`mir_eval.separation.bss_eval_images`](https://github.com/craffel/mir_eval) for
BSS Eval. You will need Matlab to run PEASS; see
[this](https://github.com/CVSSP/peass-software) repo.

In the `main` function, you will need to:

- Set the path to the compiled PEASS toolbox
- Specify whether you will be loading `wav` or `flac` files. We used `wav`.

This script generates 3 files:

1. `./data/bss_eval_and_peass.csv`

    This is the main data we used for the paper. The predictions are made using
    the same stimuli as used in the experiment, with the original (reference)
    vocal and accompaniment (sum of all other instruments) as the ground truth
    sources.  The `flac` files are included for the accompaniments so you can
    run this script. 

2. `./data/bss_eval_and_peass_all_stems.csv`

    We later discovered that you get different results depending on whether you
    input the vocals, bass, drums and other as separate ground truth sources
    (rather than the vocal and accompaniment). This is possibly the subject of
    future work.

3. `./data/bss_eval_and_peass_nonorm_all_stems.csv`
    
    Same as #2 but with no loudness normalisation applied, i.e. it uses the
    original audio files. This is possibly the subject of future work.

```
python/objective/clean_measures.py
```
Transforms the above `csv` files to long format, applying the task label
`quality` of `interferer` to the appropriate metric. New files are created with
the suffix `_clean` appended to the filename;
`./data/bss_eval_and_peass_clean.csv` is the one used in the paper.

```
python/objective/compare_methods.py
```
Not used for the paper, but shows differences due to how the ground truth
sources are specified (compares `./data/bss_eval_and_peass.csv` with
`./data/bss_eval_and_peass_all_stems.csv`).

```
python/objective/bee_swarm_plot.py
```
Computes the within-song Spearman correlations reported in Section 3.2 of the
paper, and generates Figure 2. Add the flag `--poster` to generate the poster
image instead.

```
python/objective/regression_plot.py
```
Prints the Pearson correlation coefficients and RMSEs as reported in the final
paragraph of Section 3 and generates the Figure 3 in the paper. Add the flag
`--poster` to generate the poster images instead.

# Building the paper

The source files:

- `paper/paper.md`: The paper content, written in Markdown
- `paper/metadata.yaml`: Authors, abstract, and some configuration settings
- `paper/icassp_template.latex`: `pandoc` template for generating the tex
    file for the PDF build.
- `paper/refs.bib`: References
- `paper/images`: Images generated by the python scripts (see above)

In order to build the paper, you will need to install

- [pandoc](https://pandoc.org/installing.html)
- The `pandoc` filter [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref) 
- A TeX distribution such as [TeX Live](https://www.tug.org/texlive/)
- The [biber](https://ctan.org/pkg/biber?lang=en) package

Then do (from the root of this repo)

```
cd paper
make
```

which calls `pandoc` to run `paper.md` and `metadata.yaml` through the `latex`
template `icassp_template.latex`, generating `paper/build/paper.tex`.  In the
`build` folder you will find various intermediate files generated by the
`pdflatex` and `biber` commands, in addition to the built PDF file `paper.pdf`.
