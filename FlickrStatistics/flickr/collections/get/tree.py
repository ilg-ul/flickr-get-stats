'''
Created on Sep 3, 2010

@author: ilg
'''
from flickr.collections.get.collection import Collection
from flickr.collections.get.set import Set

class Tree(object):
    '''
    classdocs
    '''
    def __init__(self, bVerbose):
        '''
        Constructor
        '''
        self.bVerbose = bVerbose
        self.oRoot = Collection(None, None, None, None, None)

    def getRoot(self):
        return self.oRoot
    
    def getUserUrl(self):
        return self.sUrl
    
    def build(self, flickr):
        eRsp = flickr.urls_getUserPhotos()
        eUser = eRsp.find('user')
        self.sUrl = eUser.attrib.get('url')
        if self.bVerbose:
            print self.sUrl

        eRsp = flickr.collections_getTree()
        eCollections = eRsp.find('collections')
        nCollectionsSum = 0
        nPhotosetsSum = 0
        nPhotosSum = 0
        for eCollection in eCollections.findall('collection'):
            (nC, nS, nP) = self._recurseBuild(flickr, eCollection, 1, self.oRoot)
            nCollectionsSum += nC
            nPhotosetsSum += nS
            nPhotosSum += nP
        self.oRoot.setStatistics(nCollectionsSum, nPhotosetsSum, nPhotosSum)
        return self.oRoot

    def _recurseBuild(self, flickr, eCollections, depth, oCollection):
        nCollectionsRunningSum = 0
        nPhotosetsRunningSum = 0
        nPhotosRunningSum = 0
        sIndent = ''
        for i in range(1, depth): #@UnusedVariable
            sIndent += '\t'

        if eCollections.tag == 'collection':
            oCollection.setHasChildrenCollections(True)
            sCollectionId = eCollections.attrib.get('id')
            sCollectionId = sCollectionId.split('-')[1] # skip user ID part
            #self.writer.clearAll()
            sTitle = eCollections.attrib.get('title')
            sDescription = eCollections.attrib.get('description')
            sIconSmall = eCollections.attrib.get('iconsmall')
            sIconLarge = eCollections.attrib.get('iconlarge')

            oNewCollection = Collection(sCollectionId, sTitle, sDescription, sIconSmall, sIconLarge)
            oCollection.addMember(oNewCollection)
            nCollectionsRunningSum += 1

            if self.bVerbose:
                print '%s%d Collection "%s" "%s" %s' % (sIndent, depth, sTitle, sDescription, sIconSmall)

            if eCollections.find('collection') != None:
                for eCollection in eCollections.findall('collection'):
                    (nC, nS, nP) = self._recurseBuild(flickr, eCollection, depth+1, oNewCollection)
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
                        eRsp = flickr.photosets_getInfo(photoset_id=sPhotosetID);
                        ePhotosetInfo = eRsp.find('photoset')
                        sPrimaryPhotoID = ePhotosetInfo.attrib.get('primary')
                        sPhotos = ePhotosetInfo.attrib.get('photos')
                        nPhotos = int(sPhotos)
                        #
                        eRsp = flickr.photos_getSizes(photo_id=sPrimaryPhotoID);
                        eSizes = eRsp.find('sizes')
                        sIcon = None
                        for eSize in eSizes.findall('size'):
                            sLabel = eSize.attrib.get('label')
                            if sLabel == 'Square':
                                sIcon = eSize.attrib.get('source')
                                break
                        if sIcon == None:
                            print 'No icon found for photo %s' % sPhotosetID

                        nPhotosetsRunningSum += 1
                        nPhotosRunningSum += nPhotos

                        oNewSet = Set(sPhotosetID, sTitle, sDescription, sIcon)
                        oNewSet.setStatistics(nPhotos)
                        oNewCollection.addMember(oNewSet)
                        
                        if self.bVerbose:
                            print '%s\tSet "%s" "%s" %s %s' % (sIndent, sTitle, sDescription, sIcon, sPhotos)
                    # end of for
                # end of if
        oNewCollection.setStatistics(nCollectionsRunningSum, nPhotosetsRunningSum, nPhotosRunningSum)
        return (nCollectionsRunningSum, nPhotosetsRunningSum, nPhotosRunningSum)

    def findCollection(self, sCollectionId):
        return self._recurseFind(self.oRoot, sCollectionId)

    def _recurseFind(self, oNode, sCollectionId):
        if oNode.sID == sCollectionId:
            return oNode

        if oNode.bHasChildrenCollections and len(oNode.oMembers) > 0:
            for oN in oNode.oMembers:
                sId = self._recurseFind(oN, sCollectionId)
                if sId != None:
                    return sId
        
        return None