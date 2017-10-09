import listen
import pandas as pd


frame = pd.read_csv('./data/ratings.csv')

times = listen.mushra.duration_stats(frame)

print(times)
