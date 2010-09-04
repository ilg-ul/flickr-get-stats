'''
Created on Sep 3, 2010

@author: ilg
'''

class Aggregate(object):
    '''
    classdocs
    '''
    def __init__(self, flickr, sUrl, oWriter, bVerbose):
        '''
        Constructor
        '''
        self.flickr = flickr
        self.sUrl = sUrl
        self.fout = None
        self.writer = oWriter
        self.writer.setUserUrl(sUrl)
        self.bVerbose = bVerbose

    def run(self, sArgOutput):
        self.writer.writeBegin()
        eRsp = self.flickr.collections_getTree()
        eCollections = eRsp.find('collections')
        nCollectionsSum = 0
        nPhotosetsSum = 0
        nPhotosSum = 0
        for eCollection in eCollections.findall('collection'):
            (nC, nS, nP) = self._recurse(eCollection, 1)
            nCollectionsSum += nC
            nPhotosetsSum += nS
            nPhotosSum += nP
        self.writer.writeEnd()
        return (nCollectionsSum, nPhotosetsSum, nPhotosSum)

    def _recurse(self, eCollections, depth):
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
            self.writer.setCollection(sCollectionID, sTitle, sDescription, sIconSmall, sIconLarge)
            self.writer.writeCollectionBegin()
            nCollectionsRunningSum += 1
            #
            if self.bVerbose:
                print '%s%d Collection "%s" "%s" %s' % (sIndent, depth, sTitle, sDescription, sIconSmall)

            if eCollections.find('collection') != None:
                self.writer.writeEmbeddedBegin()
                for eCollection in eCollections.findall('collection'):
                    (nC, nS, nP) = self._recurse(eCollection, depth+1)
                    nCollectionsRunningSum += nC
                    nPhotosetsRunningSum += nS
                    nPhotosRunningSum += nP
                    if nPhotosetsRunningSum > 5:
                        break
                self.writer.writeEmbeddedEnd()
            else:
                if eCollections.find('xset') != None:
                    self.writer.writeEmbeddedBegin()
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
                        self.writer.setPhotoset(sPhotosetID, sTitle, sDescription, nPhotos, sIcon)
                        self.writer.writePhotosetBegin()
                        self.writer.writePhotosetEnd()
                        nPhotosetsRunningSum += 1
                        nPhotosRunningSum += nPhotos
                        #
                        if self.bVerbose:
                            print '%s\tSet "%s" "%s" %s %s' % (sIndent, sTitle, sDescription, sPhotos, sIcon)
                    # end of for
                    self.writer.writeEmbeddedBegin()
                # end of if
            self.writer.writeCollectionEnd()

        return (nCollectionsRunningSum, nPhotosetsRunningSum, nPhotosRunningSum)
    
