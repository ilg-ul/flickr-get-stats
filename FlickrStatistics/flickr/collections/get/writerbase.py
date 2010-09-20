'''
Created on Sep 3, 2010

@author: ilg
'''

class WriterBase(object):
    '''
    classdocs
    '''

    def __init__(self, sName):
        '''
        Constructor
        '''
        self.bVerbose = False
        self.sName = sName
        pass

    def setVerbose(self, bVerbose):
        self.bVerbose = bVerbose
    
    def setUserUrl(self, sUserUrl):
        self.sUserUrl = sUserUrl

    def setWriter(self, fOut):
        self.fOut = fOut

    def setHierarchicalDepth(self, s):
        self.sHierarchicalDepth = s

    def setCollection(self, sID, sTitle, sDescription, sSmallIcon, sLargeIcon):
        self.sCollectionID = sID
        self.sCollectionTitle = sTitle
        self.sCollectionDescription = sDescription
        self.sCollectionSmallIcon = sSmallIcon
        self.sCollectionLargeIcon = sLargeIcon

    def setStatistics(self, nCollections, nSets, nPhotos):
        self.nCollections = nCollections
        self.nSets = nSets
        self.nPhotos = nPhotos

    def setPhotoset(self, sID, sTitle, sDescription, nPhotos, sIcon):
        self.sPhotosetID = sID
        self.sPhotosetTitle = sTitle
        self.sPhotosetDescription = sDescription
        self.nPhotosetPhotos = nPhotos
        self.sPhotosetIcon = sIcon

    def setDepth(self, nDepth):
        self.nDepth = nDepth
        self.sIndent = ''
        for i in range(1, self.nDepth): #@UnusedVariable
            self.sIndent += '\t'

    def incDepth(self):
        self.setDepth(self.nDepth+1)
        
    def decDepth(self):
        self.setDepth(self.nDepth-1)
        
    def writeBegin(self):
        return

    def writeEnd(self):
        return

    def writeCollectionBegin(self):
        return

    def writeEmbeddedBegin(self):
        return

    def writeEmbeddedEnd(self):
        return

    def writeCollectionEnd(self):
        return

    def writePhotosetBegin(self):
        return

    def writePhotosetEnd(self):
        return
