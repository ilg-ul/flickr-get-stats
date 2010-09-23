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

    def __init__(self):
        '''
        Constructor
        '''
        super(TOCWriter, self).__init__('TOC')

    def writeBegin(self):
        self.fOut.write('<table class="f_toc" summary="Contents"><tr><td><div class="f_toc_title"><h2>Contents</h2></div>\n')
        self.fOut.write('<ul class="f_toc_coll">\n')
        return
    
    def writeEnd(self):
        self.fOut.write('</ul>\n')
        self.fOut.write('</td></tr></table>\n')
        return
    
    def writeCollectionBegin(self):
        if self.bVerbose:
            print '%s%s Collection "%s"' % (self.sIndent, self.sHierarchicalDepth, self.sCollectionTitle)
        self.fOut.write('  <li class="f_toc_lvl%d"><a href="#C%s"><span class="f_toc_num">%s</span><span class="f_toc_txt">%s</span></a>\n' % (self.nDepth, self.sCollectionID, self.sHierarchicalDepth, self.sCollectionTitle))
        return

    def writePhotosetBegin(self):
        if self.bVerbose:
            print '%s%s Set "%s"' % (self.sIndent, self.sHierarchicalDepth, self.sPhotosetTitle)
        self.fOut.write('  <li class="f_toc_lvl%d"><a href="#A%s"><span class="f_toc_num">%s</span><span class="f_toc_txt">%s</span></a>\n' % (self.nDepth, self.sPhotosetID, self.sHierarchicalDepth, self.sPhotosetTitle))
        return

    def writeEmbeddedBegin(self):
        self.fOut.write('<ul class="f_coll">\n')
        return

    def writeEmbeddedEnd(self):
        self.fOut.write('</ul>\n')
        return

    def writeCollectionEnd(self):
        self.fOut.write('</li>\n')
        return
