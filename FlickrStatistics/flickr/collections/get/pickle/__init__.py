"""
Usage:
    python flickr.collections.get.html [options]

Options:
    -o "FILE", --output="FILE"
        output file; default '$HOME/Documents/Flickr/Collections.pickle'
        
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

This program will serialise the entire Flickr collections/sets tree.
It'll generate one single pickle file. 

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
        opts, args = getopt.getopt(argv[1:], 'ho:vV', ['help', 'output=', 'verbose', 'version'])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        return 2

    if len(args) > 0:
        print 'unused arguments: ', args
        usage()
        return 2

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
        sArgOutput += '/Documents/Flickr/Collections.pickle'

    sFolderName = os.path.dirname(sArgOutput)
    
    if not os.path.exists(sFolderName):
        os.makedirs(sFolderName)
    elif not os.path.isdir(sFolderName):
        print 'not a folder'
        return 2

    fOut = open(sArgOutput, 'wb')

    api = API()
    flickr = api.authenticate()

    nBeginSecs = time.time()

    if bArgVerbose:
        print sArgOutput
    # create worker objects    
    oTree = Tree(bArgVerbose)
    oRoot = None
    try:
        oRoot = oTree.build(flickr)
        if bArgVerbose:
            print 'serialising... '
        pickle.dump(oTree, fOut, pickle.HIGHEST_PROTOCOL)
        if bArgVerbose:
            print 'done'
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

