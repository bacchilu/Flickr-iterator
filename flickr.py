# -*- encoding: utf-8 -*-

'''

Simple script to download a Flickr user photos.
run this:

python flickr_download.py winonaa

then select a set, between available sets.

The script should run the authentication process (a flickr page will be opened in your browser)

'''


import urllib2
import sys

import flickrapi


api_key = '1324954697192605e8b72e4d8511ab6a'


class FlickrPhoto(object):
    '''
    Incapsulates infos to access to a flickr photo
    '''

    def __init__(self, flickrToken, title, photo_id):
        self.flickrToken = flickrToken
        self.title = title
        self.photo_id = photo_id

    def _saveFromUrl(self, url, fileName):
        '''Utily method to save a url'''

        c = urllib2.urlopen(url)
        try:
            with open(fileName, 'wb') as fp:
                fp.write(c.read())
        finally:
            c.close()

    def save(self, size='Medium'):
        '''Download the for in the desired size'''

        sizes = self.flickrToken.photos_getSizes(photo_id=self.photo_id)
        for s in sizes.find('sizes').findall('size'):
            if s.attrib['label'] == size:
                url = s.attrib['source']
                ext = url.split('.')[-1]
                fileName = self.photo_id + '.' + ext
                self._saveFromUrl(url, fileName)
                return fileName


class FlickrHelper(object):
    '''
    Wrapper of some utility functions to access to Flickr
    '''

    def __init__(self, flickrToken):
        self.flickrToken = flickrToken

    def _getUserId(self, username):
        '''From username to user_id'''

        userInfo = self.flickrToken.people_findByUsername(username=username)
        user_id = userInfo.find('user').attrib['nsid']
        return user_id

    def iterPhotos(self, username):
        user_id = self._getUserId(username)
        page = 1
        while True:
            photos = self.flickrToken.photos_search(
                user_id=user_id, page=page, per_page=10
            )

            total = int(photos.find('photos').attrib['total'])
            photosElems = photos.find('photos').findall('photo')
            if len(photosElems) == 0:
                return
            for e in photosElems:
                title = e.attrib['title']
                photo_id = e.attrib['id']
                yield FlickrPhoto(self.flickrToken, title, photo_id)
            page += 1


#def getFlickrToken(api_key, authenticate=False):
def getFlickrToken(api_key, authenticate=True):
    '''Returns the flickrapi token'''

    if authenticate:
        #flickrToken = flickrapi.FlickrAPI(api_key, 'YOUR SECRET KEY HERE')
        flickrToken = flickrapi.FlickrAPI(api_key, 'a72ec5f4f9941511')
        token, frob = flickrToken.get_token_part_one(perms='read')
        if not token:
            raw_input('Press ENTER after you authorized this program')
        flickrToken.get_token_part_two((token, frob))
    else:
        flickrToken = flickrapi.FlickrAPI(api_key)
    return flickrToken


def flickrIterator(api_key, username):
    flickrToken = getFlickrToken(api_key)
    fh = FlickrHelper(flickrToken)
    return fh.iterPhotos(username)


if __name__ == '__main__':
    try:
        username = sys.argv[1]
    except IndexError:
        print 'usage: python flickr.py <username>'
        sys.exit(1)

    for i, fp in enumerate(flickrIterator(api_key, username)):
        print i#, fp.save()