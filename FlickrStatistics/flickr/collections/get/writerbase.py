'''
Created on Sep 3, 2010

@author: ilg
'''

class WriterBase(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.bVerbose = False
        pass
        
    def setVerbose(self, bVerbose):
        self.bVerbose = bVerbose
        
    def setUserUrl(self, sUserUrl):
        self.sUserUrl = sUserUrl
        
    def setCollection(self, sID, sTitle, sDescription, sSmallIcon, sLargeIcon):
        self.sCollectionID = sID
        self.sCollectionTitle = sTitle
        self.sCollectionDescription = sDescription
        self.sCollectionSmallIcon = sSmallIcon
        self.sCollectionLargeIcon = sLargeIcon
        
    def setPhotoset(self, sID, sTitle, sDescription, nPhotos, sIcon):
        self.sPhotosetID = sID
        self.sPhotosetTitle = sTitle
        self.sPhotosetDescription = sDescription
        self.nPhotosetPhotos = nPhotos
        self.sPhotosetIcon = sIcon
        