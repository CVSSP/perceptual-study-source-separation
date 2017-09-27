'''
Script to update the submissions to conform to expected data keys used by
listen.
'''
import json
import os
import listen


def listFiles(directory):
    filenames = os.listdir(directory)
    return [os.path.abspath(os.path.join(directory, _)) for _ in filenames]

files = listFiles('./site/_data/results/interferer')
files += listFiles('./site/_data/results/quality')

for filename in files:

    parser = listen.parser.Parser(filename)
    out = parser.load(parser.path)

    out['data']['site_url'] = out['data'].pop('siteURL')
    out['data']['next_url'] = out['data'].pop('nextURL')

    changeTo = None
    for page in out['data']['pages']:

        if 'is_replicate' not in page:
            changeThis = 'None'
            if '-duplicate' in page['name']:
                changeFrom = page['name']
                changeTo = '-'.join(changeFrom.split('-')[:-1])
                page['name'] = changeTo
            else:
                page['is_replicate'] = False

    if changeTo:
        for page in out['data']['pages']:
            if changeTo in page['name']:
                page['is_replicate'] = True

    out['data'] = json.dumps(out['data'])

    with open(filename, 'w') as outfile:
        json.dump(out, outfile)
