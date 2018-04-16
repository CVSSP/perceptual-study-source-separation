# Introduction

High-quality separation of the singing voice from accompanying instruments is an
important yet difficult task serving many applications, from remixing and
upmixing music [@Roma2016] to increasing vocal intelligibility for the hearing
impaired [@Pons_2016]. Unfortunately, source separation introduces distortions
and artifacts, consequently degrading the _sound quality_ of the extracted
source. A second issue is _interference_, whereby the unwanted sources remain
present to some extent. It would therefore be useful to know how well source
separation techniques are suited to a given application. This requires
perceptual evaluation where experienced listeners judge real systems according
to different perceptual attributes. An alternative is to employ objective
metrics which have been developed to predict human perception. The purpose of
this paper is to assess the performance of two predictors of audio source
separation quality: BSS Eval [@Vincent_2006] and PEASS [@Emiya_2011].

## Previous work

The Blind Source Separation Evaluation (BSS Eval) toolkit [@Vincent_2006;
@Vincent_2007] decomposes the error between the target source and the extracted
source into a target distortion component reflecting spatial or filtering
errors, an artifacts component pertaining to artificial noise, and an
interference component associated with the unwanted sources. The salience of
these components is quantified using three energy ratios: source
Image-to-Spatial distortion Ratio (ISR), Source-to-Artifacts Ratio (SAR), and
Source-to-Interference Ratio (SIR). A fourth metric, the Source-to-Distortion
Ratio (SDR), measures the global quality (all impairments combined).

A perceptually-motivated adaptation of this toolkit is PEASS (Perceptual
Evaluation method for Audio Source Separation) [@Emiya_2011; @Vincent2012],
which estimates the three distortion components from auditory representations of
the reference and extracted sources, which are then input to the PEMO-Q auditory
model [@Huber_2006] to measure their salience. In the final stage, a
neural-network trained on human data combines the resulting component-wise
salience features into four objective predictors: Target-related Perceptual
Score (TPS), Artifacts-related Perceptual Score (APS), Interference-related
Perceptual Score (IPS), and Overall Perceptual Score (OPS). The subjective data
were obtained from a "MUlti-Stimulus test with Hidden Reference and Anchor"
(MUSHRA) [@ITUR_BS1534_3_2015] listening assessment in which listeners were
asked to rate target preservation, absence of artificial noises, suppression of
other sources, and overall quality of 10 audio excerpts (primary speech/singing
voice) estimated using 13 source separation algorithms.  Vincent [@Vincent2012]
later revised the model parameters to increase the correlation with the mean
opinion scores of the same subjective data.

Despite the development of evaluation toolkits, there is some conflicting and
inconclusive evidence as to their perceptual relevance.  For example, Cano et
al.\ [@Cano2016] performed a correlation analysis to compare the measures of BSS
Eval and PEASS with the mean opinion scores obtained from a MUSHRA experiment.
They asked the same four questions as Emiya et al.\ [@Emiya_2011], but used
musical sounds as estimated by two harmonic-percussive separation algorithms. An
across-song correlation between the subjective scores and objective values
showed that PEASS performed slightly better than BSS Eval, but that the
correlations were weak and inconsistent across the two separation algorithms,
indicating poor generalisation to other sources and types of algorithms.

Gupta et al.\ [@Gupta2015] conducted an experiment in which listeners were asked
to rate the overall quality, interference, and intelligibility of vocal and
accompaniment excerpts extracted by four singing-voice separation algorithms
from nine songs. A correlation analysis was performed between each participant's
rating and the BSS Eval measures, but the effect sizes were not consistently
high, with wide confidence intervals. The authors concluded that SIR and SAR
provided some indication of the perceived vocal isolation and intelligibility,
respectively, and that overall quality correlations were generally poor.
Cartwight et al.\ [@Cartwright2016] repeated the original PEASS experiment
[@Emiya_2011], and found consistent positive correlations for all four BSS Eval
statistics (PEASS was not assessed), with the highest being around 0.75 for SIR
(interference) and 0.55 for SAR (artificial noise). Finally, Simpson et al.\
[@Simpson2017] asked listeners to rate the overall similarity of 10 vocal
segments, whilst ignoring the accompaniment, extracted by five algorithms
against the original source. They carried out a second experiment in which
listeners judged the amount of interference indirectly by rating the similarity
of the vocal-to-accompaniment loudness ratio to that of the original mixture.
Simpson et al.\ reported high within-song Pearson correlations of around 0.91
for both SAR (similarity) and SIR (interference). Their correlations were,
however, likely inflated by including the original mixture in the objective
measurement, as this stimulus is often an outlier, especially in terms of SAR.

## This work

The previous studies suggest that there is an association between the BSS Eval
measures and perceptual characteristics of source separation algorithms when
applied to speech/singing voice, but that the strength of these relationships
depends on the perceptual attribute that listeners are asked to judge when
rating different systems. Furthermore, the predictive success of PEASS when
applied to new subjective data remains unknown. The present work investigates
these issues by assessing both toolkits in terms of predicting _sound quality_
and _interference_ of singing voices extracted from musical mixtures. A revised
experiment design is presented whereby the sound-quality rating scale is
modified to better assess the influence of distortions and artifacts on
perceived quality, independently of interference. In contrast to previous work,
a broader sample of source separation algorithms (21) and mixtures (16) have
been collated to better assess the generalisation of these metrics.

# Subjective assessment

In previous MUSHRA assessments [@Emiya_2011; @Cano2016; @Cartwright2016],
listeners rated the quality of each test sound compared to a reference sound
(the original isolated source) in terms of global quality (all impairments
combined), preservation of the target source, suppression of other sources, and
absence of additional artificial noise. However, in our previous experiment
[@Wierstorf_2017], listeners found it difficult to separate specific distortions
when auditioning the output of real systems, which agrees with the post-hoc
observations of Emiya et al.\ [@Emiya_2011] and Cartwright et al.\
[@Cartwright2016]. We therefore simplified the task by asking listeners to
assess stimuli according to two criteria: **Sound quality** relates to the
amount of artifacts and distortions that you can perceive, ranging from _worse
quality_ to _same quality_, with respect to the reference sound;
**Interference** describes the loudness of the instruments compared to the
loudness of the vocals, ranging from _strong interference_ to _no interference_.
Training examples were used to emphasize that sound quality focuses on general
distortions and not the presence of accompanying instruments. Similar examples
were presented to explain that interference should be judged independently of
such distortions. The perception of global quality [@Emiya_2011], and thus the
evaluation of all-encompassing performance metrics like SDR and OPS, is the
subject of future work.

## Procedure

Our test interface was based on MUSHRA [@ITUR_BS1534_3_2015]. The listener
clicked a 'reference' button to audition a reference singing voice, and clicked
and dragged sliders to play and rate eight test sounds on a scale from 0--100,
respectively.^[
The interface was developed using
[https://github.com/deeuu/listen](https://github.com/deeuu/listen)
]
Unlike MUSHRA, the scores were hidden from the listener and only the end points
of the scale were labelled.  These modifications were made to reduce potential
bias effects introduced by verbal labels [@Zielinski_2016].

Participants were asked to rate the sound quality and perceived interference of
eight test sounds in comparison to a reference. Sixteen vocals, each from a
different song, were used, with one excerpt randomly selected (for each listener
and task) as a replicate, resulting in 17 trials per task. The replication
allowed for the measurement of intra-rater agreement and facilitated
post-screening of participants. Both the order of the trials and the order of
the test sounds within trial was random, and task order was counterbalanced
across participants. Project resources can be found on the GitHub repository
associated with the online assessment.^[
[https://cvssp.github.io/perceptual-study-source-separation/](https://cvssp.github.io/perceptual-study-source-separation/)
]

## Stimuli

Eight test sounds were used per trial: a hidden reference (the original vocal
excerpt), two hidden anchors, and five vocals extracted from the mixture by five
different source separation algorithms. The reference vocals were taken from the
Demixing Secret Database [@Liutkus2017], a set of 100 rock and pop songs each
comprising four sources: bass, drums, vocals (lead and backing), and 'other'.
This database was compiled to assess 23 source separation algorithms competing
in the 2016 Signal Separation Evaluation Campaign (SiSEC16) [@Liutkus2017], from
which the submitted audio files were kindly provided by Fabian-Robert Stöter.
We selected 16 songs and five different algorithms per song, using a sampling
procedure which achieves a range of distortions and interference levels
according to SAR and SIR [@Wierstorf_2017]. The resulting stimuli comprised
vocals estimated by 21 source separation algorithms. 

In the MUSHRA protocol, low-quality anchors are test sounds that have been
included (unbeknownst to the listener) to represent large impairments. In
previous work [@Wierstorf_2017] we found the artifacts and target distortion
anchors defined by Emiya et al.\ [@Emiya_2011] to be of higher quality than the
worst performing algorithms of SiSEC16. We therefore modified their
specifications to establish a more appropriate anchor for the sound-quality
task. The sound-quality anchor was generated by removing 20% of the time frames
from the spectrogram of the reference and lowpass filtering it with a cutoff
frequency of $3.5\,$kHz. Musical noise was then created by randomly removing 99%
of the time-frequency bins from a second spectrogram before applying the same
lowpass filter. The inverse of these two spectrograms were loudness normalized
according to ITU-R BS.1770 [@ITUR2015] and then summed. The original mixture
associated with each reference vocal was used as the interference anchor. All
stimuli were shortened to seven seconds, converted to mono, and then loudness
normalized [@ITUR2015].

## Participants

The listening assessment involved 24 listeners, 18 of which were assessed in an
audio booth at CVSSP, and six experienced listeners completed the test online.
Of the 24 participants, three were female and 21 were male, and all were aged
between 21 and 41, with no known hearing impairments. Stimuli were reproduced
over headphones.

# Analysis and Results

Each participant's per-trial ratings were min-max scaled such that the sound
with the lowest rating was equal to zero and the sound with the highest rating
was equal to 100 [@ITUR_BS1534_3_2015]. In what follows, median (second
quartile) values are supplemented with measures of spread using the
interquartile range (IQR) which is the difference between the third and first
quartile. 

## Descriptive analysis

Intra-rater agreement was evaluated using the concordance correlation
coefficient [@Lin_1989], which ranges between -1 (perfect negative agreement)
and 1 (perfect agreement), applied to the paired scores obtained from the
replicated trials. The three hidden stimuli were removed to measure agreement on
the systems under test only. The median of the 24 participant correlations was
0.79 (IQR = 0.39) for the sound-quality task, and 0.82 (IQR = 0.21) for the
interference task. Although the magnitude of the two coefficients are
comparable, the between-listener spread is roughly twice as large for the
sound-quality task. 

![[Bee swarm plot of _all_ ratings assigned to the hidden sound-quality and
interference anchors, and the hidden reference in each task.](https://github.com/CVSSP/perceptual-study-source-separation/blob/master/python/subjective/hidden_sounds_swarmplot.py)
](./images/swarmplot_hidden_sounds.pdf){#fig:swarmplot}

[@Fig:swarmplot] shows all ratings assigned to the two hidden anchors and the
hidden reference in each task. Ratings close to zero were expected for the
sound-quality anchor in the quality task and for the interference anchor in
interference task as these anchors were designed to emphasize low-quality
degradations beyond those exhibited by real systems. It can be seen that
listener agreement is highest when judging each anchor in its associated task.
However, listeners were less certain when judging the interference present in
the sound-quality anchor, which suggests that they were uncomfortable assigning
'no interference' to artificial musical noise. The figure also highlights that
the majority of listeners were able to identify the hidden references.

Following Gupta et al.\ [@Gupta2015], inter-rater agreement was measured using
Krippendorff's $\alpha$ [@Krippendorff_2011], which ranges from 0 (absence of
reliability) to 1 (perfect reliability). With the three hidden stimuli excluded,
the across-song median $\alpha$ was 0.34 (IQR = 0.12) for the sound-quality task
and 0.40 (IQR = 0.07) for the interference task. We repeated the analysis using
the rank transformed rating data, i.e.\ treating the data as ordinal, and
obtained higher medians of 0.77 (IQR = 0.17) for the sound-quality task and 0.81
(IQR = 0.19) for the interference task. This suggests that listeners were
consistent with one another as to the relative ordering of the algorithms, and
that the lower absolute agreement can be attributed to between-listener
differences in the use of the rating scale.

## Objective metrics

![[Bee swarm plots (with boxplots underlaid) of the within-song Spearman
correlations. Markers have been perturbed by $\pm\,0.01$ to facilitate visual separation.](https://github.com/CVSSP/perceptual-study-source-separation/blob/master/python/objective/bee_swarm_plot.py)](./images/spearman_boxplot.pdf){#fig:spearman}

A Spearman correlation analysis, which assesses rank agreement between two
variables, was first used to assess the performance of two objective toolkits:
BSS Eval (SAR/ISR/SIR) and PEASS (APS/TPS/IPS).  Objective measurements were
made using the same (loudness normalized) stimuli as used in the experiment,
where the reference vocal and accompaniment (mixture minus vocal) signals served
as ground truth.  Correlations were performed for each of the 16 songs with the
reference and anchors excluded.  [@Fig:spearman] shows the correlations measured
using each predictor for the appropriate listening task. APS performed best for
the sound-quality task (median = 0.90), and SIR performed best for the
interference task (median = 1.00).  Although TPS and, to a lesser extent, SAR
show high agreement as to the ordering of the algorithms for a few songs, the
correlations are scattered over a wider region compared to those of APS. Such
inconsistencies are even more pronounced for ISR. IPS correlations were
generally strong (median: 0.80) for the interference task, but SIR performed
more consistently.

![[Linear-regression fitted APS and SAR ratings versus medians of the subjective
ratings for all test sounds.](https://github.com/CVSSP/perceptual-study-source-separation/blob/master/python/objective/regression_plot.py)
](./images/subjective_vs_sar_aps.pdf){#fig:scatter_plot}

Following Cartwright et al.\ [@Cartwright2016], a Pearson correlation
coefficient $r$ was calculated using the across-participant medians of all 80
test sounds (16 songs x 5 systems) and the measures of each metric. The
correlations obtained using the four sound-quality metrics were
$r_{\textrm{APS}} = 0.88$,
$r_{\textrm{TPS}} = 0.79$,
$r_{\textrm{SAR}} = 0.65$, and
$r_{\textrm{ISR}} = 0.28$.
These effect sizes indicate that APS yields the strongest relationship with the
subjective sound-quality ratings, with ISR performing the worst. Given that
previous studies have found associations between SAR and sound-quality
perception [@Cartwright2016; @Simpson2017], it is interesting to compare this
metric with APS.  [@Fig:scatter_plot] shows the regression-fitted measures of
both metrics versus the median subjective ratings, and indicates a stronger
monotonic upward trend when using APS, though marked deviations are observable
for both metrics. Indeed, the root-mean-square error (RMSE; computing with 2
degrees of freedom) between the fitted objective and subjective ratings was
11.9% for APS and 18.7% for SAR, both of practical significance when judged in
the context of the 100-point rating scale. The correlations measured using the
two interference-based metrics were: $r_{\textrm{SIR}} = 0.81$ and
$r_{\textrm{IPS}} = 0.81$. After fitting their measures to the subjective
ratings, both metrics had an RMSE of 15%, and so we may infer comparable
predictive capability. 

# Conclusions {#sec:conclusions}

The perception of sound quality and interference of 16 singing voices extracted
by a range of source separation algorithms was measured. By redefining the
sound-quality scale, these two perceptual attributes were measured independently
of one another. A correlation analysis was used to assess the predictive
capability of two objective toolkits for source separation performance
evaluation. The results show that the APS metric of the PEASS toolkit had the
strongest correlation with the subjective judgements of artifacts and
distortions and is therefore a useful metric for performance evaluation. Both
SIR of BSS Eval and IPS of PEASS showed comparable correlations with the
interference ratings, with the former predicting well the rank order of the
algorithms within song. In summary, we encourage researchers to make use of the
PEASS toolkit in their evaluations, rather than relying solely on energy-based
metrics.  Further refinement is, however, warranted to reduce prediction errors
to within tolerable limits.  Additional experiments are needed to assess these
metrics on different types of stimuli and also assess across-song prediction
given specific separation algorithms.
