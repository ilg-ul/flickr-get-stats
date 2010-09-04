"""
Usage:
    python flickr.collections.get.html [options]

Options:
    -o "FILE", --output="FILE"
        output file; default '$HOME/Documents/Flickr/Collections.html'
        
    -v, --verbose
        print progress output

    -V, --version
        print program version

    -h, --help
        print this message

Purpose:
    Iterate all collections from a Flickr account and generate a 
    html page.

---

This program will generate one .html file with several embedded 
div sections. 

The authentication is done only once, and the Flickr authentication 
token is stored in the user home directory.
 
"""

import getopt
import os
import sys
import flickrapi
import time
import io
from flickr.application.api import API
from flickr.collections.get.html.writer import Writer
from flickr.collections.get.aggregate import Aggregate

myProgramVersion = '1.1.20100904'
# ---------------------------------------------------------------------
def usage():
    print __doc__

def main(*argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'ho:vV', ['help', 'output=', 'verbose', 'version'])
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
    sArgOutput = None
    bArgVerbose = False
    for o, a in opts:
        if o in ('-v', '--verbose'):
            bArgVerbose = True
        elif o in ('-h', '--help'):
            usage()
            return 0
        elif o in ('-V', '--version'):
            print "version: " + myProgramVersion
            return 0
        elif o in ('-o', '--output'):
            sArgOutput = a
        else:
            assert False, 'option not handled'
    # output default
    if sArgOutput == None:
        sArgOutput = os.environ['HOME']
        sArgOutput += '/Documents/Flickr/Collections.html'
    #
    sFolderName = os.path.dirname(sArgOutput)
    
    if not os.path.exists(sFolderName):
        os.makedirs(sFolderName)
    elif not os.path.isdir(sFolderName):
        print 'not a folder'
        return 2

    fOut = open(sArgOutput, 'w')
    #
    api = API()
    flickr = api.authenticate()
    #
    nBeginSecs = time.time()
    #
    eRsp = flickr.urls_getUserPhotos()
    eUser = eRsp.find('user')
    sUrl = eUser.attrib.get('url')
    if bArgVerbose:
        print sUrl
    # create worker objects
    writer = Writer()
    writer.setWriter(fOut)
    writer.setVerbose(bArgVerbose)
    #aggregate = Aggregate(flickr, sUrl, writer, bArgVerbose)
    aggregate = Aggregate(flickr, sUrl, writer, bArgVerbose)
    nCollections = 0
    nSets = 0
    try:
        (nCollections, nSets, nPhotos) = aggregate.run(sArgOutput)         
    except flickrapi.exceptions.FlickrError as ex:
        print 'FlickrError', ex
    except:
        print 'Other Exception', sys.exc_info()
    #
    fOut.close()
    #        
    if bArgVerbose:
        nEndTime = time.time()
        nDuration = nEndTime-nBeginSecs
        print '[done, %d collection(s), %d set(s), %d photos, %d sec]' % (nCollections, nSets, nPhotos, nDuration)
    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

