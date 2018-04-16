---
layout: poster
title:  "My Poster"
permalink: /poster/
---

<div id='title'>

<h1>BSS EVAL OR PEASS? <span style='color: #1b656d'>PREDICTING THE PERCEPTION OF SINGING-VOICE SEPARATION</span></h1>

<div style='width: 65%; float: left' markdown="1">
<h2>Dominic Ward, Hagen Wierstorf, Russell D. Mason, Emad M. Grais, Mark D. Plumbley</h2><h3>Centre for Vision, Speech and Signal Processing | Institute of Sound Recording | University of Surrey, Guildford, UK </h3>
</div>

<div style='width: 35%; float: right' markdown="1">
<h2 style='color: #502382'> Audio Examples { <a href='https://bit.ly/2GutUKR'>bit.ly/2GutUKR</a> }</h2>
</div>

</div>

<div id='title-info'>

<div>
<img style='width: 45%; margin: 0; padding: 25px; float: left' src="{{ site.url }}/images/uos.png">
<img style='width: 45%; margin: 0; padding: 25px; float: left' src="{{ site.url }}/images/epsrc.png">
</div>

</div>

<div class='panel' id='intro' markdown="1">

# Objective Evaluation of Audio Source Separation

- Separating the singing-voice from music is a difficult task, however,
    deep-learning methods show significant improvements over traditional
    techniques such as NMF and ICA

- Source separation introduces distortions and artifacts, which degrades the
    perceived sound quality

- There is a trade-off between the degree of separation and sound quality

## How to evaluate separation performance?

Few researchers conduct listening assessments, but instead resort to objective toolkits:

- <span style='color: #1b656d'>BSS Eval</span><sup>1</sup>: Blind Source Separation Evaluation
- <span style='color: #1b656d'>PEASS</span><sup>2</sup>: Perceptual Evaluation methods for Audio Source Separation

Both approaches based on distortion decomposition between estimated source
$$\hat{S}$$ and target source $$S$$:

$$\hat{S} - S = e_{\text{target}} + e_{\text{interference}} + e_{\text{artifacts}}$$

Error components estimated through least-squares projections of estimated and
true sources

![]({{ site.url }}/images/bss_eval.png)

<div class='refs' markdown="1">
- Vincent et al. (2006) { [10.1109/tsa.2005.858005](https://doi.org/10.1109/TSA.2005.858005) }
- Emiya et al. (2012) { [10.1109/tasl.2011.2109381](https://doi.org/10.1109/tasl.2011.2109381) }
</div>

</div>


<div class='panel-emph' id='intro2' markdown="1">

# Subjective Listening Assessment

Can these toolkits be used to predict the perception of singing-voices extracted
by modern source separation systems?

- Need more evidence to address suitability of BSS Eval

- Few studies have investigated generalization of PEASS

</div>


<div class='panel' id='method' markdown="1">

# Methodology


<h2>Task 1: <span style='color: #1b656d'>Sound Quality</span></h2>

> Sound quality relates to the amount of artifacts or distortions that you can
> perceive. These can be heard as tone-like additions, abrupt changes in
> loudness, or missing parts of the audio.

<h2>Task 2: <span style='color: #1b656d'>Interference</span></h2>

> Interference describes the loudness of the instruments compared to the
> loudness of the vocals. For example, ‘strong interference’ indicates a strong
> contribution from other instruments, whereas ‘no interference’ means that you
> can only hear the vocals. Interference does not include artifacts or
> distortions that you may perceive.

- 24 Listeners performed a MUSHRA-style experiment
- 16 songs, using *singing-voice* as the target source
- **Listeners compared 5 algorithms** selected pseudorandomly from 21 systems for each song <sup>3</sup>
- Hidden reference and hidden sound quality and interference anchors included

![]({{ site.url }}/images/interface.png)
*Interface for Task 1. Examples at { [bit.ly/2GutUKR](https://bit.ly/2GutUKR) }*

<div class='refs' markdown='1'>
- SiSEC 2016 { <a href='http://sisec17.audiolabs-erlangen.de'>http://sisec17.audiolabs-erlangen.de </a>}
</div>

</div>

<div class='panel' id='results' markdown="1">

# Results

## Song-Wise Spearman Correlations

<div class='nested-1-2-split'>
<div markdown="1">

- Measures rank-order relationship between objective measures and medians of subjective ratings
- Performed on a per-song basis involving 5 algorithms
- 16 song-wise correlations per metric
</div>

<div markdown="1">
![]({{ site.url }}/images/spearman_boxplot.png)
</div>

</div>

## Linear-Fitted Objective Measures vs Subjective Medians

<div class='nested-1-1-split'>
<div markdown="1">
![]({{ site.url }}/images/subjective_vs_APS_SAR.png)
</div>

<div markdown="1">
![]({{ site.url }}/images/subjective_vs_IPS_SIR.png)
</div>

</div>
</div>

<div class='panel-emph' id='conclusions' markdown="1">

# Conclusions and Reflections

<div class='nested-1-1-split'>

<div markdown="1">
- Important to reinforce attribute definitions with audio examples
- APS of the PEASS toolkit showed the strongest predictive ability
- IPS (PEASS) and SIR (BSS Eval) were comparable in performance
- Metrics far from perfect (large RMSE) when considering the 100-point scale
</div>

<div markdown="1">
- Remapping of features necessary to better predict the perceptual scales used here
- Need to assess metrics on other sources
- Next time, emphasize **overall sound quality** as some listeners focused
    only on the singing-voice
- We are currently running **similarity** experiments for assessing SDR and OPS
</div>
</div>

</div>
 
