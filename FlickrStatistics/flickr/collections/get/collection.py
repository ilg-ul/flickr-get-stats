'''
Created on Sep 4, 2010

@author: ilg
'''

class Collection(object):
    '''
    classdocs
    '''
    def __init__(self, sID, sTitle, sDescription, sIconSmallUrl, sIconLargeUrl):
        '''
        Constructor
        '''
        self.sID = sID
        self.sTitle = sTitle
        self.sDescription = sDescription
        self.sIconSmallUrl = sIconSmallUrl
        self.sIconLargeUrl = sIconLargeUrl
        self.oMembers = []
        self.nCollections = 0
        self.nSets = 0
        self.nPhotos = 0
        self.bHasChildCollections = False
        
    def setStatistics(self, nCollections, nSets, nPhotos):
        self.nCollections = nCollections
        self.nSets = nSets
        self.nPhotos = nPhotos

    def addMember(self, oMember):
        self.oMembers.append(oMember)
        
    def setHasChildCollections(self, bFlag):
        self.bHasChildCollections = bFlag

        