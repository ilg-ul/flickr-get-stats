"""
Usage:
    python -m ilg.flickr.statistics.get.csv [options]

Options:
    -f "FOLDER", --folder="FOLDER"
        destination folder where CSV files are stored; 
        default is '$HOME/Documents/Flickr/Statistics'

    -d "DAY", --day="DAY"
        the day to get statistics for; the format is 
        quite strict, and should look like "2010-06-30"
     
    -v, --verbose
        print progress output

    -V, --version
        print program version

    -h, --help
        print this message

Purpose:
    Retrieve daily CSV statistic files for a Flickr account.

---

This program will generate one CSV file per day. The file format is 
exactly the same as used by Flickr in the past, when they provided 
aggregated statistics.

The output files contain the date in the file name, like:
    2010-06-30-flickr.csv
    
The files already present in the destination folder are not 
fetched again.

The program will try to go back in time and fetch as much 
statistics as possible, about one month (according to Flickr, 
at least 28 days are stored). 

If the --day option is used, only one day of statistics is fetched.

The authentication is done only once, and the Flickr authentication 
token is stored in the user home directory.
 
"""

import flickrapi
import sys
import time
import getopt
import os

from ilg.flickr.statistics.get.aggregate import Aggregate
from ilg.flickr.statistics.get.csv.writer import Writer


'''
The below key identifies this application only, for accessing Flickr.
It is not suitable for other purposes.
'''
api_key = '972a07f9991a94960fee5bde355b7191'
api_secret = '4573a0d92f02730b'

# ---------------------------------------------------------------------
myMaxDay = 38   # Flickr says they keep 28 days, but I noticed to be longer
myMinDay = 2    # at least 1, better 2

myProgramVersion = '1.1.20100807'
# ---------------------------------------------------------------------
def usage():
    print __doc__

def main(*argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hf:d:vV', ['help', 'folder=', 'day=', 'verbose', 'version'])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        return 2
    #
    if len(args) > 0:
        print 'unused arguments: ', args
        usage()
        return 2
    #
    sArgFolder = None
    bArgVerbose = False
    sArgDay = None
    for o, a in opts:
        if o in ('-v', '--verbose'):
            bArgVerbose = True
        elif o in ('-h', '--help'):
            usage()
            return 0
        elif o in ('-V', '--version'):
            print "version: " + myProgramVersion
            return 0
        elif o in ('-f', '--folder'):
            sArgFolder = a
        elif o in ('-d', '--day'):
            sArgDay = a
        else:
            assert False, 'option not handled'
    # validate day argument
    if sArgDay != None:
        try:
            time.strptime(sArgDay, '%Y-%m-%d')
        except ValueError as ex:
            print 'Illegal date "%s"' % sArgDay
            return 2
    # folder defaults
    if sArgFolder == None:
        sArgFolder = os.environ['HOME']
        sArgFolder += '/Documents/Flickr/Statistics'
    # be sure the folder exists
    if not os.path.exists(sArgFolder):
        os.makedirs(sArgFolder)
    elif not os.path.isdir(sArgFolder):
        print 'not a folder'
        return 2
    # authenticate
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    (token, frob) = flickr.get_token_part_one(perms='read')
    if not token: 
        raw_input('Press ENTER after you authorized this program')
    flickr.get_token_part_two((token, frob))
    #
    eRsp = flickr.urls_getUserPhotos()
    eUser = eRsp.find('user')
    sUrl = eUser.attrib.get('url')
    if bArgVerbose:
        print sUrl
    # create worker objects
    writer = Writer()
    writer.setVerbose(bArgVerbose)
    aggregate = Aggregate(flickr, sUrl, writer, bArgVerbose)
    try:
        if sArgDay != None:
            aggregate.oneDay(sArgDay, sArgFolder)
        else:
            nNowSecs = time.time()
            # iterate from the earliest possible day
            for i in range(myMaxDay, myMinDay, -1):
                nSecs = nNowSecs - i*24*60*60
                oDate = time.gmtime(nSecs)
                sDay = time.strftime('%Y-%m-%d', oDate)
                aggregate.oneDay(sDay, sArgFolder)         
    except flickrapi.exceptions.FlickrError as ex:
        print 'FlickrError', ex
    except:
        print 'Other Exception', sys.exc_info()
    #        
    if bArgVerbose:
        print '[done]'
    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

