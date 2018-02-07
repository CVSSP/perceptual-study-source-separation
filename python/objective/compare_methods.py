import numpy as np
from scipy.stats import pearsonr
import pandas as pd

df_accomp = pd.read_csv('./data/bss_eval_and_peass.csv')
df_stems = pd.read_csv('./data/bss_eval_and_peass_all_stems.csv')

print(df_accomp.head(2), df_stems.head(2))

print('~~~ BSS Eval ~~~')

metrics = ['SAR', 'SIR', 'ISR']

print([
    '{} r: {}'.format(_, pearsonr(df_accomp[_], df_stems[_]))
    for _ in metrics
])

print([
    '{} mean error: {}'.format(_, np.mean(np.abs(df_accomp[_] - df_stems[_])))
    for _ in metrics
])

print('~~~ PEASS ~~~')

metrics = ['APS', 'IPS', 'TPS']

print([
    '{} r: {}'.format(_, pearsonr(df_accomp[_], df_stems[_]))
    for _ in metrics
])

print([
    '{} mean error: {}'.format(_, np.mean(np.abs(df_accomp[_] - df_stems[_])))
    for _ in metrics
])
