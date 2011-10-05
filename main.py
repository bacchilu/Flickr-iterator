# -*- encoding: utf-8 -*-

'''

Simple script to download a Flickr user photos.
run this:

python flickr_download.py winonaa

then select a set, between available sets.

The script should run the authentication process (a flickr page will be opened in your browser)

'''

import sys


if __name__ == '__main__':
    try:
        username = sys.argv[1]
    except IndexError:
        print 'usage: python main.py <username>'
        sys.exit(1)

    import flickrgenerator
    for i, fp in enumerate(flickrgenerator.flickrGenerator(username)):
        print i#, fp.save()