import sys
import flickrapi
from flickr.statistics.get.aggregate import Aggregate
from flickr.statistics.get.csv.writer import Writer

# The below key identifies this application only.
# It is not suitable for other purposes.
api_key = '972a07f9991a94960fee5bde355b7191'
api_secret = '4573a0d92f02730b'

# ---------------------------------------------------------------------
# --- Until this will get parametrised, change it for your needs ------
myDate = '2010-06-'
myDayFrom = 26
myDayTo = 28

myDir='/Users/ilg/My Files/MacMini Library/Photos/Flickr/Statistics'
# ---------------------------------------------------------------------

def main(*argv):
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    (token, frob) = flickr.get_token_part_one(perms='read')
    if not token: 
        raw_input("Press ENTER after you authorized this program")
    flickr.get_token_part_two((token, frob))
    eRsp = flickr.urls_getUserPhotos()
    eUser = eRsp.find('user')
    global sUrl
    sUrl = eUser.attrib.get('url')
    print sUrl
    #
    writer = Writer()
    aggregate = Aggregate(flickr, sUrl, writer)
    try:
        for iDay in range(myDayFrom, myDayTo+1): 
            aggregate.oneDay('%s%02d' % (myDate, iDay), myDir)         
    except flickrapi.exceptions.FlickrError as e:
        print 'FlickrError', e
    except:
        print 'Other Exception', sys.exc_info()
        
    print '[done]'

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

