'''
Created on Sep 23, 2010

@author: ilg
'''
class Set(object):
    '''
    classdocs
    '''
    def __init__(self, sID, sTitle, sDescription, sIconUrl):
        '''
        Constructor
        '''
        self.sID = sID
        self.sTitle = sTitle
        self.sDescription = sDescription
        self.sIconUrl = sIconUrl
        self.nCollections = 0
        self.nPhotos = 0

    def setStatistics(self, nPhotos):
        self.nPhotos = nPhotos
