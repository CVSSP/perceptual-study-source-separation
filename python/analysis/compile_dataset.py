'''
Script to update the submissions to conform to expected data keys used by
listen.
'''
import pandas as pd
import listen


def main():

    frame = listen.parser.MUSHRA('./site/_data/results/interferer').parse()

    frame = frame.append(
        listen.parser.MUSHRA('./site/_data/results/quality').parse()
    )

    subjects = pd.unique(frame.subject)

    print('You have {} subjects: '.format(len(subjects)), subjects)

    frame.to_csv('./data/ratings.csv', index=None)


if __name__ == '__main__':

    main()
