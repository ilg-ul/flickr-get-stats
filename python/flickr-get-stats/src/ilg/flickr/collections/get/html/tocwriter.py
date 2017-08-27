'''
Created on Sep 3, 2010

@author: ilg
'''
from flickr.collections.get.writerbase import WriterBase

bUseTables = True

class TOCWriter(WriterBase):
    '''
    classdocs
    '''

    def __init__(self, sDescription='TOC'):
        '''
        Constructor
        '''
        super(TOCWriter, self).__init__(sDescription)

    def writeBegin(self):
        self.oOutStream.write(u'<table class="f_toc" summary="Contents"><tr><td><div class="f_toc_title"><h2>Contents</h2></div>\n')
        self.oOutStream.write(u'<ul class="f_toc_coll">\n')
        return
    
    def writeEnd(self):
        self.oOutStream.write(u'</ul>\n')
        self.oOutStream.write(u'</td></tr></table>\n')
        return
    
    def writeCollectionBegin(self):
        if self.bVerbose:
            print '%s%s Collection "%s"' % (self.sIndent, self.sHierarchicalDepth, self.sCollectionTitle)
        self.oOutStream.write(u'  <li class="f_toc_lvl%d"><a href="#C%s"><span class="f_toc_num">%s</span><span class="f_toc_txt">%s</span></a>\n' % (self.nDepth, self.sCollectionID, self.sHierarchicalDepth, self.sCollectionTitle))
        return

    def writePhotosetBegin(self):
        if self.bVerbose:
            print '%s%s Set "%s"' % (self.sIndent, self.sHierarchicalDepth, self.sPhotosetTitle)
        self.oOutStream.write(u'  <li class="f_toc_lvl%d"><a href="#A%s"><span class="f_toc_num">%s</span><span class="f_toc_txt">%s</span></a>\n' % (self.nDepth, self.sPhotosetID, self.sHierarchicalDepth, self.sPhotosetTitle))
        return

    def writeEmbeddedBegin(self):
        self.oOutStream.write(u'<ul class="f_coll">\n')
        return

    def writeEmbeddedEnd(self):
        self.oOutStream.write(u'</ul>\n')
        return

    def writeCollectionEnd(self):
        self.oOutStream.write(u'</li>\n')
        return
