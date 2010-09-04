'''
Created on Sep 3, 2010

@author: ilg
'''

import flickrapi

'''
The below key identifies this application only, for accessing Flickr.
It is not suitable for other purposes.
'''
api_key = '972a07f9991a94960fee5bde355b7191'
api_secret = '4573a0d92f02730b'

class API(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def getKey(self):
        return api_key
    
    def getSecret(self):
        return api_secret

    def authenticate(self):
        flickr = flickrapi.FlickrAPI(api_key, api_secret)
        (token, frob) = flickr.get_token_part_one(perms='read')
        if not token: 
            raw_input('Press ENTER after you authorized this program')
        flickr.get_token_part_two((token, frob))
        return flickr
