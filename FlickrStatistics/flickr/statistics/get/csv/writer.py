'''
Created on Jun 10, 2010

@author: ilg
'''
from flickr.statistics.get.writerbase import WriterBase

class Writer(WriterBase):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def setWriter(self, fOut):
        self.fOut = fOut
        fOut.write('date,flickr page,full referrer,referrer domain,search term,count\n')
    
    def flush(self):
        sUrl = self.getKindFullUrl();            
        sRef = self.sFullReferrerUrl
        self.fOut.write('%s,%s,"%s","%s","%s",%d\n' % (self.sDate, sUrl, sRef, self.toUTF8(self.sReferrerDomain), self.toUTF8(self.sSearchTerm), self.nReferrerCount))


