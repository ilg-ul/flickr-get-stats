'''
Created on Jun 10, 2010

@author: ilg
'''
from ilg.flickr.statistics.get.writerbase import WriterBase

class Writer(WriterBase):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def setOutputStream(self, oOutStream):
        self.oOutStream = oOutStream
        oOutStream.write('date,flickr page,full referrer,referrer domain,search term,count\n')
    
    def flush(self):
        sUrl = self.getKindFullUrl();            
        sRef = self.sFullReferrerUrl
        self.oOutStream.write('%s,%s,"%s","%s","%s",%d\n' % (self.sDate, sUrl, sRef, self.toUTF8(self.sReferrerDomain), self.toUTF8(self.sSearchTerm), self.nReferrerCount))


