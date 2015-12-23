"""
Usage:
    python -m ilg.flickr.test.echo

Purpose:
    Test the SSL spurious exceptions.
 
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
 
    eRsp = flickr.urls_getUserPhotos()
    eUser = eRsp.find('user')
    sUrl = eUser.attrib.get('url')
    print sUrl


    success = 0
    failure = 0
    
    print 'testing...'
  
    max=1000  
    for count in range(1000):
        try:
            eRsp = flickr.test_echo()
            success = success + 1
            print '%d/%d ok' % (count, max)
        except Exception as ex:
            print '>>>>>>>>>> test_echo %s' % ex  
            failure = failure + 1 
            print '%d err' % count
            
    print '[done, success=%d, failure=%d]' % (success, failure)
    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

