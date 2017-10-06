'''
Script to update the submissions to conform to expected data keys used by
listen.

Note, I later renamed (untracked script) some subjects in attempt to preserve
their anonymity from the online submissions.
'''
import pandas as pd
import listen


def main():

    frame = listen.parser.MUSHRA('./site/_data/results/interferer').parse()

    frame = frame.append(
        listen.parser.MUSHRA('./site/_data/results/quality').parse()
    )

    # Drop these submissions as we have resubmissions for them:
    frame = frame.query("~subject.isin(['JF-WEB', 'SE-WEB'])").reset_index()

    listen.mushra.normalise_ratings(frame, True)

    try:
        from rename_subjects import rename
        rename(frame)
    except:
        pass

    # Remove these subjects completely based on post-screening:
    frame = frame.qurty("~subjects.isin(['D', 'J'])")

    for g in frame.groupby('experiment'):

        print('Subjects: ', pd.unique(g[1].subject))

        print('You have {0} subjects in experiment: {1}'.format(
            len(pd.unique(g[1].subject)), g[0]),
        )

    frame.to_csv('./data/ratings.csv', index=None)


if __name__ == '__main__':

    main()
