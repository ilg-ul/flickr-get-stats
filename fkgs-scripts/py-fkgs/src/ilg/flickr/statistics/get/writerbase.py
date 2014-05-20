'''
Created on Jun 10, 2010

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
        
    def setDate(self, sDate):
        self.sDate = sDate
        
    def setDateStats(self, nTotal, nPhotos, nPhotoset, nSets, nCollections):
        '''store values in class variables'''
        self.nTotal = nTotal
        self.nPhotos = nPhotos
        self.nPhotoset = nPhotoset
        self.nSets = nSets
        self.nCollections = nCollections
        pass
    
    def clearAll(self):
        self.sID = None
        self.clearReferrerDomain()
        self.clearReferrer()
        
    def setKind(self, sKind):
        self.sKind = sKind
        
    def setID(self, sID, sTitle, nCount):
        self.sID = sID
        if self.bVerbose:
            print '%s "%s" %d' % (self.getKindFullUrl(), sTitle.encode('utf-8'), nCount)
        
    def setReferrerDomain(self, sDomain, nCount):
        self.sReferrerDomain = sDomain
        self.nReferrerDomainCount = nCount
        if self.bVerbose:
            print '\t"%s" %d' % (self.sReferrerDomain.encode('utf-8'), self.nReferrerDomainCount)

    def clearReferrerDomain(self):
        self.sReferrerDomain = None
        self.nReferrerDomainCount = None
        
    def setReferrer(self, sUrl, sSearchTerm, nCount):
        self.sFullReferrerUrl = sUrl
        self.sSearchTerm = sSearchTerm
        self.nReferrerCount = nCount
        if self.bVerbose:
            print '\t\t"%s" "%s" %d' % (self.sFullReferrerUrl.encode('utf-8'), self.sSearchTerm.encode('utf-8'), self.nReferrerCount)

    def clearReferrer(self):
        self.sFullReferrerUrl = None
        self.sSearchTerm = None
        self.nReferrerCount = None
                
    def setFullReferrerUrl(self, sUrl):
        self.sFullReferrerUrl = sUrl
        
    def setSearchTerm(self, sSearchTerm):
        self.sSearchTerm = sSearchTerm
        
    def setReferrerCount(self, nCount):
        self.nReferrerCount = nCount
        
    def setAnonymousReferrerCount(self, nCount):
        self.clearReferrerDomain()
        self.clearReferrer()
        self.nReferrerCount = nCount
        if self.bVerbose:
            print '\t"" %d (anon)' % self.nReferrerCount
        
    def getKindFullUrl(self):
        if self.sKind == 'photos':
            sUrl = self.sUserUrl + self.sID + '/'
        elif self.sKind == 'photostream':
            sUrl = self.sUserUrl
        elif self.sKind == 'sets' or self.sKind == 'collections':
            sUrl = self.sUserUrl + self.sKind + '/' + self.sID + '/'
        return sUrl

    def toUTF8(self, s):
        if s == None:
            return None
        return s.encode('utf-8')

    def flush(self):
        raise "Abstract, must be implemented in derived class!"

