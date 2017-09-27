'''
Script to update the submissions to conform to expected data keys used by
listen.
'''
import os
import listen
import pandas


parser = listen.parser.MUSHRA('./site/_data/results/interferer')
frame = parser.parse()
#frame = pd.DataFrame('./site/_data/results/quality')
