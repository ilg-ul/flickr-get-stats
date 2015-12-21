"""
Usage:
    python -m ilg.flickr.authenticate

Purpose:
    Authenticate and store the authentication token.
 
"""

import flickrapi
import sys

'''
The below key identifies this application only, for accessing Flickr.
It is not suitable for other purposes.
'''
api_key = '972a07f9991a94960fee5bde355b7191'
api_secret = '4573a0d92f02730b'

# ---------------------------------------------------------------------
def usage():
    print __doc__

def main(*argv):
       
    # authenticate
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    flickr.authenticate_via_browser(perms='read')
 
    for retry in range(10):
        try:
            eRsp = flickr.urls_getUserPhotos()
            break
        except Exception as ex:
            print '>>>>>>>>>> urls_getUserPhotos %s' % ex   

    eUser = eRsp.find('user')
    sUrl = eUser.attrib.get('url')
    print sUrl
    print '[done]'
    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

