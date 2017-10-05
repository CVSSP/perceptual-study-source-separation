import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
import listen as ln


frame = pd.read_csv('./data/ratings.csv')

corr_data = ln.mushra.between_subject_agreement(frame)

print('~~~ Median correlation ~~~')
print(corr_data.median)

print('~~~ Spearman CI95 ~~~')
print(corr_data.spearman_ci)

print('~~~ Pearson CI95 ~~~')
print(corr_data.pearson_ci)
