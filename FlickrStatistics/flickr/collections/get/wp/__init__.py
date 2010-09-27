"""
Usage:
    python flickr.collections.get.wp [options]

Options:
    -i "FILE", --input="FILE"
        input pickle file
        
    --input=
        default '$HOME/Documents/Flickr/Collections.pickle'

    --wp_url="URL"
        URL of WordPress XMLRPC endpoint

    --wp_user="user"
        WordPress user name

    --wp_passwd="passorwd"
        WordPress user password

    --wp_key="key"
        WordPress blog key (from Users -> Personal Settings -> API Key)

    --wp_map="Flickr_id:WordPress_id:comment" (list)
        Map Flickr collection id to WordPress page id.
        Index page entered as 'index'.
        The comment can be used to store the collection title.

    --wp_out="WordPress_id" (list)
        WordPress page to be generated

    -v, --verbose
        print progress output

    -V, --version
        print program version

    -h, --help
        print this message

Purpose:
    Iterate all collections from a Flickr account, generate the 
    html pages and publish them on WordPress.
    
    If the input file is specified, the program will use the local serialised 
    file instead of Flickr (useful for testing).

---

This program will generate WordPress pages with a Table of Content and
a detailes tree of collections and albums.

The global index page will contain all collection in the Flickr account, 
but will not include albums.

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
from pyblog import WordPress

# ---------------------------------------------------------------------
def usage():
    print __doc__

def main(*argv):
    
    oApp = API()

    try:
        opts, args = getopt.getopt(argv[1:], 'hi:vV', ['help', 'input=', 'wp_url=', 'wp_user=', 'wp_passwd=', 'wp_key=', 'wp_map=', 'wp_out=', 'verbose', 'version'])
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
    bArgVerbose = False

    sWpUrl = None
    sWpUser = None
    sWpPasswd = None
    sWpKey = None
    dWpMapByCollectionId = {}   # mapping dictionary; key=colection_id; value=WP_id
    dWpMapByPageId = {}         # mapping dictionary; key=WP_id; value=colection_id
    aWpOut = []                 # list of WP_ids to generate
    
    for o, a in opts:
        if o in ('-v', '--verbose'):
            bArgVerbose = True
        elif o in ('-h', '--help'):
            usage()
            return 0
        elif o in ('-V', '--version'):
            print "version: " + oApp.getProgramVersion()
            return 0
        elif o in ('-i', '--input'):
            if a != None and a != '':
                sArgInput = a
            else:
                sArgInput = oApp.getUserHome()
                sArgInput += '/Documents/Flickr/Collections.pickle'
        elif o in ('--wp_url'):
            sWpUrl = a
        elif o in ('--wp_user'):
            sWpUser = a
        elif o in ('--wp_passwd'):
            sWpPasswd = a
        elif o in ('--wp_key'):
            sWpKey = a
        elif o in ('--wp_map'):
            aSub = a.split(':')
            if len(aSub) >= 2:
                sCollectionId = aSub[0]
                iWpPageId = int(aSub[1])
                dWpMapByCollectionId[sCollectionId] = iWpPageId
                dWpMapByPageId[iWpPageId] = sCollectionId
            else:
                print 'option "%s=%s" ignored' % (o, a)
        elif o in ('--wp_out'):
            # non numeric IDs are ignored
            if a.isdigit():
                aWpOut.append(int(a))
            else:
                print 'option "%s=%s" ignored' % (o, a)
        else:
            assert False, 'option not handled'

    if sWpUrl == None or sWpUser == None or sWpPasswd == None or sWpKey == None or len(dWpMapByCollectionId) == 0 or len(aWpOut) == 0:
        usage()
        return 2
        
    if sArgInput == None:
        oInStream = None       
    else:
        oInStream = open(sArgInput, 'rb')
        if bArgVerbose:
            print sArgInput

    nBeginSecs = time.time()

    # create worker objects
    oMainWriter = Writer()
    oTOCWriter = TOCWriter()
    oWriters = [ oTOCWriter ]
    
    oRoot = None
    nMainRet = 0
    try:
        dRemapUrl = {}
        for sCollectionId in dWpMapByCollectionId.keys():
            if sCollectionId.isdigit():
                dRemapUrl[sCollectionId] = '/?p=%d' % dWpMapByCollectionId[sCollectionId]

        oBlog = WordPress(sWpUrl, sWpUser, sWpPasswd)
        if False:
            aPageList = oBlog.get_page_list(sWpKey)
            dBlogPagesById = {}
            for dPage in aPageList:
                print dPage
                dBlogPagesById[int(dPage['page_id'])] = dPage
        
        if oInStream == None:
            flickr = oApp.authenticate()

            oTree = Tree(flickr, bArgVerbose)
            oRoot = oTree.build()  
        else:
            oTree = pickle.load(oInStream)
            oRoot = oTree.getRoot()

        oAgregate = Aggregate(oTree, oMainWriter, oWriters, bArgVerbose)
        
        iWpPages = 0
        for nPageId in aWpOut:
            sCollectionId = None
            
            # find the corresponding Flickr collection id            
            if nPageId in dWpMapByPageId:
                sCollectionId = dWpMapByPageId[nPageId]
            else:
                print 'Collection %s not found in --wp_map' % sCollectionId
                continue
            
            bOutputSets = True
            if sCollectionId == '*' or sCollectionId == 'index':
                oNode = oTree.getRoot()
                bOutputSets = False
            else:
                oNode = oTree.findCollection(sCollectionId)                
                if oNode == None:
                    print 'Collection %s not found in Flickr' % sCollectionId
                    continue
            
            oOutStream = io.StringIO()
            oAgregate.runSingleOutput(oNode, bOutputSets, dRemapUrl, oOutStream)
            sContent = oOutStream.getvalue()
            oOutStream.close()
    
            dPage = oBlog.get_page(nPageId, sWpKey)
            #print dPage['description']
            
            sTitle = dPage['title']  # mandatory
            sSlug = dPage['wp_slug'] # mandatory
            sDescription = dPage['description']
            #print sDescription
            print 'Page %d "%s" read in' % (nPageId, sTitle)
            
            sDescription = sContent
            dContent = {}
            dContent['description'] = sDescription
            dContent['title'] = sTitle
            dContent['wp_slug'] = sSlug
            
            oRet = oBlog.edit_page(nPageId, dContent, True, sWpKey)
            if oRet:
                print 'Page %d "%s" published' % (nPageId, sTitle)
                iWpPages += 1
            else:
                print 'Page %s not published' % iWpPages
        # end of for nPageId

    except flickrapi.exceptions.FlickrError as ex:
        print 'FlickrError', ex

    if bArgVerbose:
        nEndTime = time.time()
        nDuration = nEndTime-nBeginSecs
        if oRoot != None:
            print '[done, %d collection(s), %d set(s), %d photos, %d pages, %d sec]' % (oRoot.nCollections, oRoot.nSets, oRoot.nPhotos, iWpPages, nDuration)
        else:
            print '[done, %d sec]' % (nDuration)

    return nMainRet

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

