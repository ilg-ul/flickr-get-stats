"""
Usage:
    python flickr.collections.get.html [options]

Options:
    -i "FILE", --input="FILE"
        input pickle file
        
    --input=
        default '$HOME/Documents/Flickr/Collections.pickle'

    -o "FILE", --output="FILE"
        output html file; default '$HOME/Documents/Flickr/Collections.html'
        
    -v, --verbose
        print progress output

    -V, --version
        print program version

    -h, --help
        print this message

Purpose:
    Iterate all collections from a Flickr account and generate a 
    html page.
    
    If the input file is specified, the program will use the local serialised 
    file instead of Flickr (useful for testing).

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
from flickr.collections.get.tree import Tree
from flickr.collections.get.html.tocwriter import TOCWriter
import pickle

myProgramVersion = '1.1.20100904'
# ---------------------------------------------------------------------
def usage():
    print __doc__

def main(*argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hi:o:vV', ['help', 'input=','output=', 'verbose', 'version'])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        return 2

    if len(args) > 0:
        print 'unused arguments: ', args
        usage()
        return 2

    sArgInput = None
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
        elif o in ('-i', '--input'):
            if a != None and a != '':
                sArgInput = a
            else:
                sArgInput = os.environ['HOME']
                sArgInput += '/Documents/Flickr/Collections.pickle'
        elif o in ('-o', '--output'):
            sArgOutput = a
        else:
            assert False, 'option not handled'

    # output default
    if sArgOutput == None:
        sArgOutput = os.environ['HOME']
        sArgOutput += '/Documents/Flickr/Collections.html'

    sFolderName = os.path.dirname(sArgOutput)
    
    if not os.path.exists(sFolderName):
        os.makedirs(sFolderName)
    elif not os.path.isdir(sFolderName):
        print 'not a folder'
        return 2

    fOut = open(sArgOutput, 'w')

    if sArgInput != None:
        fIn = open(sArgInput, 'rb')
    else:
        fIn = None       

    api = API()
    flickr = api.authenticate()

    nBeginSecs = time.time()

    eRsp = flickr.urls_getUserPhotos()
    eUser = eRsp.find('user')
    sUrl = eUser.attrib.get('url')
    if bArgVerbose:
        print sArgInput
        print sArgOutput
        print sUrl

    # create worker objects
    oMainWriter = Writer()
    oMainWriter.setWriter(fOut)
    oMainWriter.setUserUrl(sUrl)
    oMainWriter.setVerbose(bArgVerbose)

    oTOCWriter = TOCWriter()
    oTOCWriter.setWriter(fOut)
    oTOCWriter.setUserUrl(sUrl)
    oTOCWriter.setVerbose(bArgVerbose)

    oWriters = [ oTOCWriter ]
    
    oTree = Tree(flickr, sUrl, bArgVerbose)
    oRoot = None
    try:
        if fIn == None:
            oRoot = oTree.build()  
        else:
            oRoot = pickle.load(fIn)       
        oAgregate = Aggregate(oRoot, oMainWriter, oWriters, bArgVerbose)
        oAgregate.run()
    except flickrapi.exceptions.FlickrError as ex:
        print 'FlickrError', ex

    fOut.close()
        
    if bArgVerbose:
        nEndTime = time.time()
        nDuration = nEndTime-nBeginSecs
        if oRoot != None:
            print '[done, %d collection(s), %d set(s), %d photos, %d sec]' % (oRoot.nCollections, oRoot.nSets, oRoot.nPhotos, nDuration)
        else:
            print '[done, %d sec]' % (nDuration)

    return 0

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

