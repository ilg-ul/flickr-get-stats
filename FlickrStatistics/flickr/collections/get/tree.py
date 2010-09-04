'''
Created on Sep 3, 2010

@author: ilg
'''
from flickr.collections.get.collection import Collection

class Tree(object):
    '''
    classdocs
    '''
    def __init__(self, flickr, sUrl, bVerbose):
        '''
        Constructor
        '''
        self.flickr = flickr
        self.sUrl = sUrl
        self.bVerbose = bVerbose
        self.oRoot = Collection(None, None, None, None, None)

    def getRoot(self):
        return self.oRoot
    
    def build(self):
        eRsp = self.flickr.collections_getTree()
        eCollections = eRsp.find('collections')
        nCollectionsSum = 0
        nPhotosetsSum = 0
        nPhotosSum = 0
        for eCollection in eCollections.findall('collection'):
            (nC, nS, nP) = self._recurse(eCollection, 1, self.oRoot)
            nCollectionsSum += nC
            nPhotosetsSum += nS
            nPhotosSum += nP
        self.oRoot.setStatistics(nCollectionsSum, nPhotosetsSum, nPhotosSum)
        return self.oRoot

    def _recurse(self, eCollections, depth, oCollection):
        nCollectionsRunningSum = 0
        nPhotosetsRunningSum = 0
        nPhotosRunningSum = 0
        sIndent = ''
        for i in range(1, depth): #@UnusedVariable
            sIndent += '\t'
        
        if eCollections.tag == 'collection':
            sCollectionID = eCollections.attrib.get('id')
            sCollectionID = sCollectionID.split('-')[1] # skip user ID part
            #self.writer.clearAll()
            sTitle = eCollections.attrib.get('title')
            sDescription = eCollections.attrib.get('description')
            sIconSmall = eCollections.attrib.get('iconsmall')
            sIconLarge = eCollections.attrib.get('iconlarge')
            oNewCollection = Collection(sCollectionID, sTitle, sDescription, sIconSmall, sIconLarge)
            oCollection.addMember(oNewCollection)
            nCollectionsRunningSum += 1
            #
            if self.bVerbose:
                print '%s%d Collection "%s" "%s" %s' % (sIndent, depth, sTitle, sDescription, sIconSmall)

            if eCollections.find('collection') != None:
                for eCollection in eCollections.findall('collection'):
                    (nC, nS, nP) = self._recurse(eCollection, depth+1, oNewCollection)
                    nCollectionsRunningSum += nC
                    nPhotosetsRunningSum += nS
                    nPhotosRunningSum += nP
            else:
                if eCollections.find('set') != None:
                    for ePhotoset in eCollections.findall('set'):
                        sPhotosetID = ePhotoset.attrib.get('id')
                        sTitle = ePhotoset.attrib.get('title')
                        sDescription = ePhotoset.attrib.get('description')
                        #
                        eRsp = self.flickr.photosets_getInfo(photoset_id=sPhotosetID);
                        ePhotosetInfo = eRsp.find('photoset')
                        sPrimaryPhotoID = ePhotosetInfo.attrib.get('primary')
                        sPhotos = ePhotosetInfo.attrib.get('photos')
                        nPhotos = int(sPhotos)
                        #
                        eRsp = self.flickr.photos_getSizes(photo_id=sPrimaryPhotoID);
                        eSizes = eRsp.find('sizes')
                        sIcon = None
                        for eSize in eSizes.findall('size'):
                            sLabel = eSize.attrib.get('label')
                            if sLabel == 'Square':
                                sIcon = eSize.attrib.get('source')
                                break
                        if sIcon == None:
                            print 'No icon found for photo %s' % sPhotosetID
                        #
                        #self.writer.setPhotoset(sPhotosetID, sTitle, sDescription, nPhotos, sIcon)
                        nPhotosetsRunningSum += 1
                        nPhotosRunningSum += nPhotos
                        #
                        if self.bVerbose:
                            print '%s\tSet "%s" "%s" %s %s' % (sIndent, sTitle, sDescription, sIcon, sPhotos)
                    # end of for
                # end of if
        oNewCollection.setStatistics(nCollectionsRunningSum, nPhotosetsRunningSum, nPhotosRunningSum)
        return (nCollectionsRunningSum, nPhotosetsRunningSum, nPhotosRunningSum)
    
