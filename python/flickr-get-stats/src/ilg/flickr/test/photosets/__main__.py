"""
Usage:
    python -m ilg.flickr.test.photosets

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
    
    iPhotosPage = 1
    while True:
        try:
            eRsp = flickr.photosets_getList(per_page=1)
            success = success + 1
            ePhotos = eRsp.find('photosets')
            nPhotosPage = int(ePhotos.attrib['page'])
            nPhotosPages = int(ePhotos.attrib['pages'])
            print '%d/%d ok' % (nPhotosPage, nPhotosPages)
            
            for ePhotoset in ePhotos.findall('photoset'):
                nPhotosetId = ePhotoset.attrib['id']
                print nPhotosetId
                eRsp = flickr.photosets_getInfo(photoset_id=nPhotosetId)
                
            if nPhotosPages == 0:
                break
            if nPhotosPage == nPhotosPages:
                break
            iPhotosPage = nPhotosPage + 1
        except Exception as ex:
            print '>>>>>>>>>> stats_getPopularPhotos %s' % ex   
            failure = failure + 1 
            print '%d err' % iPhotosPage
            
    print '[done, success=%d, failure=%d]' % (success, failure)
    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

