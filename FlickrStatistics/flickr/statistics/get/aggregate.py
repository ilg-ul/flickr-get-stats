'''
Created on Jun 10, 2010

@author: ilg
'''
import tempfile

class Aggregate(object):
    '''
    classdocs
    '''
    def __init__(self, flickr, sUrl, oWriter):
        '''
        Constructor
        '''
        self.flickr = flickr
        self.sUrl = sUrl
        self.fout = None
        self.writer = oWriter
        self.writer.setUserUrl(sUrl)

    def _photos(self, nPhotosViews):
        iPhotosPage = 0
        nPhotosViewsSum = 0
        self.writer.setKind('photos')
        while True:
            eRsp = self.flickr.stats_getPopularPhotos(page=iPhotosPage, date=self.day)
            ePhotos = eRsp.find('photos')
            #ntotal = int(ePhotos.attrib['total'])
            nPhotosPage = int(ePhotos.attrib['page'])
            nPhotosPages = int(ePhotos.attrib['pages'])
            if nPhotosPages == 0:
                break
            #nperpage = int(ePhotos.attrib['perpage'])
            for ePhoto in ePhotos.findall('photo'):
                eStats = ePhoto.find('stats')
                nPhotoViews = int(eStats.attrib['views'])
                sPhotoID = ePhoto.attrib['id']
                self.writer.clearAll()
                self.writer.setID(sPhotoID, ePhoto.attrib['title'], nPhotoViews)
                nPhotosViewsSum += nPhotoViews
                #
                iDomainsPage = 0
                nPhotoViewsSum = 0
                while True:
                    eRsp = self.flickr.stats_getPhotoDomains(photo_id=sPhotoID, page=iDomainsPage, date=self.day)
                    eDomains = eRsp.find('domains')
                    nDomainsPage = int(eDomains.attrib['page'])
                    nDomainsPages = int(eDomains.attrib['pages'])
                    if nDomainsPages == 0:
                        break   #catch abnormal cases
                    for eDomain in eDomains.findall('domain'):
                        sDomainName = eDomain.attrib['name']
                        nDomainViews = int(eDomain.attrib['views'])
                        self.writer.setReferrerDomain(sDomainName, nDomainViews)
                        nPhotoViewsSum += nDomainViews
                        iReferrersPage = 0
                        nDomainViewsSum = 0
                        while True:
                            eRsp = self.flickr.stats_getPhotoReferrers(photo_id=sPhotoID, domain=sDomainName, page=iReferrersPage, date=self.day)
                            eReferrers = eRsp.find('domain')
                            nReferrersPage = int(eReferrers.attrib['page'])
                            nReferrersPages = int(eReferrers.attrib['pages'])
                            if nReferrersPages == 0:
                                break   #catch abnormal cases
                            for eReferrer in eReferrers.findall('referrer'):
                                sReferrerURL = eReferrer.attrib['url']
                                nReferrerViews = int(eReferrer.attrib['views'])
                                sReferrerSearch = eReferrer.get('searchterm', '')
                                self.writer.setReferrer(sReferrerURL, sReferrerSearch, nReferrerViews)
                                self.writer.flush()
                                self.writer.clearReferrer()
                                nDomainViewsSum += nReferrerViews
                            if nReferrersPage == nReferrersPages:
                                break
                            iReferrersPage = nReferrersPage + 1    
                        if nDomainViews != nDomainViewsSum:
                            if nDomainViews > nDomainViewsSum:
                                self.writer.setAnonymousReferrerCount(nDomainViews - nDomainViewsSum)
                                self.writer.flush()
                                self.writer.clearReferrer()
                            else:
                                print '\t\tdifferent photos domain views exp %d sum %d' % (nDomainViews, nDomainViewsSum)
                    if nDomainsPage == nDomainsPages:
                        break
                    iDomainsPage = nDomainsPage + 1
                if nPhotoViews != nPhotoViewsSum:
                    if nPhotoViews > nPhotoViewsSum:
                        self.writer.setAnonymousReferrerCount(nPhotoViews - nPhotoViewsSum)
                        self.writer.flush()
                        self.writer.clearReferrer()
                    else:
                        print '\tdifferent photos views exp %d sum %d' % (nPhotoViews, nPhotoViewsSum)
            if nPhotosPage == nPhotosPages:
                break
            iPhotosPage = nPhotosPage + 1
        if nPhotosViews != nPhotosViewsSum:
            print 'different photos total views exp %d sum %d' % (nPhotosViews, nPhotosViewsSum)
        return
    
    def _photostream(self, nPhotostreamViews):
        iDomainsPage = 0
        nPhotostreamViewsSum = 0
        self.writer.setKind('photostream')
        while True:
            eRsp = self.flickr.stats_getPhotostreamDomains(page=iDomainsPage, date=self.day)
            eDomains = eRsp.find('domains')
            nDomainsPage = int(eDomains.attrib['page'])
            nDomainsPages = int(eDomains.attrib['pages'])
            if nDomainsPages == 0:
                break   #catch abnormal cases
            for eDomain in eDomains.findall('domain'):
                sDomainName = eDomain.attrib['name']
                nDomainViews = int(eDomain.attrib['views'])
                self.writer.clearAll()
                self.writer.setReferrerDomain(sDomainName, nDomainViews)
                #print '\t%s %d' % (sDomainName, nDomainViews)
                nPhotostreamViewsSum += nDomainViews
                iReferrersPage = 0
                nDomainViewsSum = 0
                while True:
                    eRsp = self.flickr.stats_getPhotostreamReferrers(domain=sDomainName, page=iReferrersPage, date=self.day)
                    eReferrers = eRsp.find('domain')
                    nReferrersPage = int(eReferrers.attrib['page'])
                    nReferrersPages = int(eReferrers.attrib['pages'])
                    if nReferrersPages == 0:
                        break   #catch abnormal cases
                    for eReferrer in eReferrers.findall('referrer'):
                        sReferrerURL = eReferrer.attrib['url']
                        nReferrerViews = int(eReferrer.attrib['views'])
                        sReferrerSearch = eReferrer.attrib.get('searchterm', '')
                        #print '\t\t%s "%s" %d' % (sReferrerURL, sReferrerSearch.encode('utf-8'), nReferrerViews)
                        self.writer.setReferrer(sReferrerURL, sReferrerSearch, nReferrerViews)
                        self.writer.flush()
                        self.writer.clearReferrer()
                        nDomainViewsSum += nReferrerViews
                    if nReferrersPage == nReferrersPages:
                        break
                    iReferrersPage = nReferrersPage + 1    
                if nDomainViews != nDomainViewsSum:
                    print '\t\tdifferent photostream domain views exp %d sum %d' % (nDomainViews, nDomainViewsSum)
            if nDomainsPage == nDomainsPages:
                break
            iDomainsPage = nDomainsPage + 1
        if nPhotostreamViews != nPhotostreamViewsSum:
            if nPhotostreamViews > nPhotostreamViewsSum:
                self.writer.setAnonymousReferrerCount(nPhotostreamViews - nPhotostreamViewsSum)
                self.writer.flush()
                self.writer.clearReferrer()
            else:
                print 'different photostream total views exp %d sum %d' % (nPhotostreamViews, nPhotostreamViewsSum)
        return    
    
    def _photoset(self, nPhotosetsViews):
        nPhotosetsViewsSum = 0
        eRsp = self.flickr.photosets_getList()
        ePhotosets = eRsp.find('photosets')
        self.writer.setKind('sets')
        for ePhotoset in ePhotosets.findall('photoset'):
            sPhotosetID = ePhotoset.attrib['id']
            self.writer.clearAll()
            eRsp = self.flickr.stats_getPhotosetStats(photoset_id=sPhotosetID, date=self.day)
            eStats = eRsp.find('stats')
            sPhotosetViews = eStats.attrib.get('views', '')
            if sPhotosetViews == '':
                continue
            nPhotosetViews = int(sPhotosetViews)
            if nPhotosetViews == 0:
                continue
            sTitle = ePhotoset.find('title').text
            self.writer.setID(sPhotosetID, sTitle, nPhotosetViews)
            #print '%s "%s" %d' % (self.writer.getKindFullUrl(), sTitle.encode('utf-8'), nPhotosetViews)
            nPhotosetsViewsSum += nPhotosetViews
            #
            iDomainsPage = 0
            nPhotosetViewsSum = 0
            while True:
                eRsp = self.flickr.stats_getPhotosetDomains(photoset_id=sPhotosetID, page=iDomainsPage, date=self.day)
                eDomains = eRsp.find('domains')
                nDomainsPage = int(eDomains.attrib['page'])
                nDomainsPages = int(eDomains.attrib['pages'])
                if nDomainsPages == 0:
                    break   #catch abnormal cases
                for eDomain in eDomains.findall('domain'):
                    sDomainName = eDomain.attrib['name']
                    nDomainViews = int(eDomain.attrib['views'])
                    self.writer.setReferrerDomain(sDomainName, nDomainViews)
                    #print '\t%s %d' % (sDomainName, nDomainViews)
                    nPhotosetViewsSum += nDomainViews
                    iReferrersPage = 0
                    nDomainViewsSum = 0
                    while True:
                        eRsp = self.flickr.stats_getPhotosetReferrers(photoset_id=sPhotosetID, domain=sDomainName, page=iReferrersPage, date=self.day)
                        eReferrers = eRsp.find('domain')
                        nReferrersPage = int(eReferrers.attrib['page'])
                        nReferrersPages = int(eReferrers.attrib['pages'])
                        if nReferrersPages == 0:
                            break   #catch abnormal cases
                        for eReferrer in eReferrers.findall('referrer'):
                            sReferrerURL = eReferrer.attrib['url']
                            nReferrerViews = int(eReferrer.attrib['views'])
                            sReferrerSearch = eReferrer.attrib.get('searchterm', '')
                            #print '\t\t%s "%s" %d' % (sReferrerURL, sReferrerSearch.encode('utf-8'), nReferrerViews)
                            self.writer.setReferrer(sReferrerURL, sReferrerSearch, nReferrerViews)
                            self.writer.flush()
                            self.writer.clearReferrer()
                            nDomainViewsSum += nReferrerViews
                        if nReferrersPage == nReferrersPages:
                            break
                        iReferrersPage = nReferrersPage + 1    
                    if nDomainViews != nDomainViewsSum:
                        if nDomainViews > nDomainViewsSum:
                            self.writer.setAnonymousReferrerCount(nDomainViews - nDomainViewsSum)
                            self.writer.flush()
                            self.writer.clearReferrer()
                        else:
                            print '\t\tdifferent photoset domain views exp %d sum %d' % (nDomainViews, nDomainViewsSum)
                if nDomainsPage == nDomainsPages:
                    break
                iDomainsPage = nDomainsPage + 1
            if nPhotosetViews != nPhotosetViewsSum:
                if nPhotosetViews > nPhotosetViewsSum:
                    self.writer.setAnonymousReferrerCount(nPhotosetViews - nPhotosetViewsSum)
                    self.writer.flush()
                    self.writer.clearReferrer()
                else:
                    print '\t\tdifferent photoset views exp %d sum %d' % (nPhotosetViews, nPhotosetViewsSum)
        if nPhotosetsViews != nPhotosetsViewsSum:
            print 'different photosets total views exp %d sum %d' % (nPhotosetsViews, nPhotosetsViewsSum)
        return 
    
    def _collection_recurse(self, eCollections):
        nRunningSum = 0
        if eCollections.tag == 'collection':
            sCollectionID = eCollections.attrib.get('id')
            sCollectionID = sCollectionID.split('-')[1] # skip user ID part
            self.writer.clearAll()
            sTitle = eCollections.attrib.get('title')
            #print sTitle.encode('utf-8')
            eRsp = self.flickr.stats_getCollectionStats(collection_id=sCollectionID, date=self.day)
            eStats = eRsp.find('stats')
            sCollectionViews = eStats.attrib.get('views', '')
            if sCollectionViews != '':
                nCollectionViews = int(sCollectionViews)
                if nCollectionViews != 0:
                    nRunningSum = nCollectionViews
                    self.writer.setID(sCollectionID, sTitle, nCollectionViews)
                    #print '%sTitle "%sTitle" %d' % (self.writer.getKindFullUrl(), sTitle.encode('utf-8'), nRunningSum)
                    iDomainsPage = 0
                    #nDomainsViewsSum = 0
                    nCollectionViewsSum = 0
                    while True:
                        eRsp = self.flickr.stats_getCollectionDomains(collection_id=sCollectionID, page=iDomainsPage, date=self.day)
                        eDomains = eRsp.find('domains')
                        nDomainsPage = int(eDomains.attrib['page'])
                        nDomainsPages = int(eDomains.attrib['pages'])
                        if nDomainsPages == 0:
                            break   #catch abnormal cases
                        for eDomain in eDomains.findall('domain'):
                            sDomainName = eDomain.attrib['name']
                            nDomainViews = int(eDomain.attrib['views'])
                            self.writer.setReferrerDomain(sDomainName, nDomainViews)
                            #print '\t%sTitle %d' % (sDomainName, nDomainViews)
                            #nDomainsViewsSum += nDomainViews
                            nCollectionViewsSum += nDomainViews
                            iReferrersPage = 0
                            nDomainViewsSum = 0
                            while True:
                                eRsp = self.flickr.stats_getCollectionReferrers(collection_id=sCollectionID, domain=sDomainName, page=iReferrersPage, date=self.day)
                                eReferrers = eRsp.find('domain')
                                nReferrersPage = int(eReferrers.attrib['page'])
                                nReferrersPages = int(eReferrers.attrib['pages'])
                                if nReferrersPages == 0:
                                    break   #catch abnormal cases
                                for eReferrer in eReferrers.findall('referrer'):
                                    sReferrerURL = eReferrer.attrib['url']
                                    nReferrerViews = int(eReferrer.attrib['views'])
                                    sReferrerSearch = eReferrer.attrib.get('searchterm', '')
                                    #print '\t\t%sTitle "%sTitle" %d' % (sReferrerURL, sReferrerSearch.encode('utf-8'), nReferrerViews)
                                    self.writer.setReferrer(sReferrerURL, sReferrerSearch, nReferrerViews)
                                    self.writer.flush()
                                    self.writer.clearReferrer()
                                    nDomainViewsSum += nReferrerViews
                                if nReferrersPage == nReferrersPages:
                                    break
                                iReferrersPage = nReferrersPage + 1    
                            if nDomainViews != nDomainViewsSum:
                                if nDomainViews > nDomainViewsSum:
                                    self.writer.setAnonymousReferrerCount(nDomainViews - nDomainViewsSum)
                                    self.writer.flush()
                                    self.writer.clearReferrer()
                                else:
                                    print '\t\tdifferent collection domain views exp %d sum %d' % (nDomainViews, nDomainViewsSum)
                        if nDomainsPage == nDomainsPages:
                            break
                        iDomainsPage = nDomainsPage + 1
                    #
                    if nCollectionViews != nCollectionViewsSum:
                        if nCollectionViews > nCollectionViewsSum:
                            self.writer.setAnonymousReferrerCount(nCollectionViews - nCollectionViewsSum)
                            self.writer.flush()
                            self.writer.clearReferrer()
                        else:
                            print '\tdifferent collection views exp %d sum %d' % (nCollectionViews, nCollectionViewsSum)
        if eCollections.find('collection') != None:
            for eCollection in eCollections.findall('collection'):
                nRunningSum += self._collection_recurse(eCollection)
        return nRunningSum
    
    def _collection(self, nCollectionsViews):
        """Aggregate collections"""
        eRsp = self.flickr.collections_getTree()
        eCollections = eRsp.find('collections')
        self.writer.setKind('collections')
        nCollectionsViewsSum = self._collection_recurse(eCollections)
        if nCollectionsViews != nCollectionsViewsSum:
            print 'different collections total views exp %d sum %d' % (nCollectionsViews, nCollectionsViewsSum)
        return 
    
    def oneDay(self, sDay, sDir):
        """Aggregate one day of statistics"""
        # may trigger exceptions
        self.day = sDay
        self.writer.setDate(sDay)
        # start with totals for the day
        eRsp = self.flickr.stats_getTotalViews(date=sDay)
        eStats = eRsp.find('stats')
        nViewsTotal = int(eStats.find('total').attrib['views'])
        nViewsPhotos = int(eStats.find('photos').attrib['views'])
        nViewsPhotostream = int(eStats.find('photostream').attrib['views'])
        nViewsSets = int(eStats.find('sets').attrib['views'])
        nViewsCollections = int(eStats.find('collections').attrib['views'])
        self.writer.setDateStats(nViewsTotal, nViewsPhotos, nViewsPhotostream, nViewsSets, nViewsCollections)
        print '[%s total %d]' % (self.day, nViewsTotal)
        if nViewsTotal == 0:
            return  #no views for this day
        # create output file only if there is content
        fout = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', prefix=sDay + '-flickr-', dir=sDir, delete=False)
        print fout.name
        self.writer.setWriter(fout)
        #nViewsPhotos = 0
        if nViewsPhotos != 0:
            print '[%s photos %d]' % (sDay, nViewsPhotos)
            self._photos(nViewsPhotos)
        #nViewsPhotostream = 0
        if nViewsPhotostream != 0:
            print '[%s photostream %d]' % (sDay, nViewsPhotostream)
            self._photostream(nViewsPhotostream)
        #nViewsSets = 0
        if nViewsSets != 0:
            print '[%s sets %d]' % (sDay, nViewsSets)
            self._photoset(nViewsSets)
        #nViewsCollections = 0
        if nViewsCollections != 0:
            print '[%s collections %d]' % (sDay, nViewsCollections)
            self._collection(nViewsCollections)
        print fout.name
        fout.close()
        return
    
     

