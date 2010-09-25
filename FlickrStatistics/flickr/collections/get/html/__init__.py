"""
Usage:
    python flickr.collections.get.html [options]

Options:
    -i "FILE", --input="FILE"
        input pickle file
        
    --input=
        default '$HOME/Documents/Flickr/Collections.pickle'

    -f "FOLDER", --folder="FOLDER"
        output folder, where html files are stored;
        default is '$HOME/Documents/Flickr/Collections/'
        
    -o "FILE", --output="FILE"
        output html file; default '$HOME/Documents/Flickr/Collections.html'
        (ignored is --folder= was also used)
        
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
from flickr.collections.get.html.writerhdr import WriterWithHeader

# ---------------------------------------------------------------------
def usage():
    print __doc__

def main(*argv):
    
    api = API()

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
    sArgFolder = None
    bArgVerbose = False
    for o, a in opts:
        if o in ('-v', '--verbose'):
            bArgVerbose = True
        elif o in ('-h', '--help'):
            usage()
            return 0
        elif o in ('-V', '--version'):
            print "version: " + api.getProgramVersion()
            return 0
        elif o in ('-i', '--input'):
            if a != None and a != '':
                sArgInput = a
            else:
                sArgInput = api.getUserHome()
                sArgInput += '/Documents/Flickr/Collections.pickle'
        elif o in ('-f', '--folder'):
            sArgFolder = a
        elif o in ('-o', '--output'):
            if a != '':
                sArgOutput = a
        else:
            assert False, 'option not handled'

    if sArgFolder == None and sArgOutput == None:
        sArgFolder = api.getUserHome()
        sArgFolder += '/Documents/Flickr/Collections/'

    if sArgFolder != None:
        if not os.path.exists(sArgFolder):
            os.makedirs(sArgFolder)
        elif not os.path.isdir(sArgFolder):
            print 'not a folder'
            return 2
        if bArgVerbose:
            print sArgFolder
    else:
        # output default
        if sArgOutput == None:
            sArgOutput = api.getUserHome()
            sArgOutput += '/Documents/Flickr/Collections.html'

        sFolderName = os.path.dirname(sArgOutput)

        if not os.path.exists(sFolderName):
            os.makedirs(sFolderName)
        elif not os.path.isdir(sFolderName):
            print 'not a folder'
            return 2
        if bArgVerbose:
            print sArgOutput

    if sArgInput == None:
        fIn = None       
    else:
        fIn = open(sArgInput, 'rb')
        if bArgVerbose:
            print sArgInput

    nBeginSecs = time.time()

    # create worker objects
    oMainWriter = WriterWithHeader()
    oTOCWriter = TOCWriter()
    oWriters = [ oTOCWriter ]
    
    oRoot = None
    nMainRet = 0
    try:
        if fIn == None:
            flickr = api.authenticate()

            oTree = Tree(flickr, bArgVerbose)
            oRoot = oTree.build()  
        else:
            oTree = pickle.load(fIn)
            oRoot = oTree.getRoot()
                   
        oAgregate = Aggregate(oTree, oMainWriter, oWriters, bArgVerbose)
        if sArgFolder != None:
            nMainRet = oAgregate.runMulti(sArgFolder)
        else:
            
            oOutStream = open(sArgOutput, 'w')
            oAgregate.runSingleOutput(oTree.getRoot(), False, oOutStream)
            oOutStream.close()
            
    except flickrapi.exceptions.FlickrError as ex:
        print 'FlickrError', ex

    if bArgVerbose:
        nEndTime = time.time()
        nDuration = nEndTime-nBeginSecs
        if oRoot != None:
            print '[done, %d collection(s), %d set(s), %d photos, %d sec]' % (oRoot.nCollections, oRoot.nSets, oRoot.nPhotos, nDuration)
        else:
            print '[done, %d sec]' % (nDuration)

    return nMainRet

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

