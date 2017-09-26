'''
Script to update the submissions to conform to expected data keys used by
listen.
'''

import os
import json
import listen

directories = ['./site/_data/results/interferer',
               './site/_data/results/quality']

filenames = os.listdir(directories[0]) + os.listdir(directories[1])

for filename in filenames:

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
                print(page)

    with open(filename, 'w') as outfile:
        json.dump(out, outfile)
