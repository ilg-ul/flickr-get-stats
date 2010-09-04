'''
Created on Sep 4, 2010

@author: ilg
'''

class Collection(object):
    '''
    classdocs
    '''
    def __init__(self, sID, sTitle, sDescription, sSmallIcon, sLargeIcon):
        '''
        Constructor
        '''
        self.sID = sID
        self.sTitle = sTitle
        self.sDescription = sDescription
        self.sIconSmall = sSmallIcon
        self.sIconLarge = sLargeIcon
        self.oMembers = []
        self.nCollections = 0
        self.nSets = 0
        self.nPhotos = 0
        self.bChildCollections = True
        
    def setStatistics(self, nCollections, nSets, nPhotos):
        self.nCollections = nCollections
        self.nSets = nSets
        self.nPhotos = nPhotos

    def addMember(self, oMember):
        self.oMembers.append(oMember)
        