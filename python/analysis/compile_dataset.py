'''
Script to update the submissions to conform to expected data keys used by
listen.
'''
import pandas as pd
import listen

frame = listen.parser.MUSHRA('./site/_data/results/interferer').parse()

frame = frame.append(
    listen.parser.MUSHRA('./site/_data/results/quality').parse()
)

print(pd.unique(frame.subject))
