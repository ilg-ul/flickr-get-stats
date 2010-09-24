'''
Created on Sep 24, 2010

@author: ilg
'''
from flickr.collections.get.html.writer import Writer

class WriterWithHeader(Writer):
    '''
    classdocs
    '''

    def __init__(self, sDescription='Main With Headers'):
        '''
        Constructor
        '''
        super(WriterWithHeader, self).__init__(sDescription)

    def writeHeaderBegin(self):
        self.oOutStream.write(u'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
        self.oOutStream.write(u'<html>\n')
        self.oOutStream.write(u'<head>\n')
        self.oOutStream.write(u'  <title>Flickr: ilg-ul Photos</title>\n')
        self.oOutStream.write(u'  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n')
        self.oOutStream.write(u'  <link type="text/css" rel="stylesheet" href="flickr.css">\n')
        self.oOutStream.write(u'</head>\n')
        self.oOutStream.write(u'<body>\n')
        return
    
    def writeHeaderEnd(self):
        self.oOutStream.write(u'</body>\n')
        self.oOutStream.write(u'</html>\n')
        return
    
