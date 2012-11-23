'''
Created on Sep 3, 2010

@author: ilg
'''
from flickr.collections.get.writerbase import WriterBase

bUseTables = True

class Writer(WriterBase):
    '''
    classdocs
    '''

    def __init__(self, sDescription='Main'):
        '''
        Constructor
        '''
        super(Writer, self).__init__(sDescription)

    def writeBegin(self, s):
        if s == None:
            s = 'Collections'
        self.oOutStream.write(u'<h3>%s</h3>\n' % s)
        return

    def writeEnd(self):
        return
  
    def _computeCollectionRef(self):
        if self.sLocalUrl != None:
            return '<a href="%s#C%s">' % (self.sLocalUrl, self.sCollectionID)
        else:
            return '<a href="%scollections/%s/">' % (self.sUserUrl, self.sCollectionID)
    
    def _computeCollectionImg(self):
        return '<img src="%s" width="91" height="68" alt="%s" />' % (self.sCollectionSmallIcon, self.sCollectionTitle)
    
    def _computeCollectionStats(self):
        s = ('%d album' % self.nSets)
        if self.nSets != 1:
            s += 's'
        s += (', %d photo' % self.nPhotos)
        if self.nPhotos != 1:
            s += 's'
        return s
        
    def writeCollectionBegin(self):
        if self.bVerbose:
            print '%s%d Collection "%s" "%s" %s %d %d %d' % (self.sIndent, self.nDepth, self.sCollectionTitle, self.sCollectionDescription, self.sCollectionSmallIcon, self.nCollections, self.nSets, self.nPhotos)
        if bUseTables:
            #self.oOutStream.write('<a name="C%s"> </a>' % (self.sCollectionID))
            self.oOutStream.write(u'<table class="f_coll">\n')
            self.oOutStream.write(u'  <tr class="f_coll_r1">\n')
            self.oOutStream.write(u'    <td class="f_coll_icon">\n')
            self.oOutStream.write(u'      <div class="f_coll_icon">%s%s</a></div>\n' % (self._computeCollectionRef(), self._computeCollectionImg()))
            self.oOutStream.write(u'    </td>\n')
            self.oOutStream.write(u'    <td class="f_coll_info">\n')
            self.oOutStream.write(u'      <div class="f_coll_info">\n')
            self.oOutStream.write(u'        <h4><a name="C%s">%s</a></h4>\n' % (self.sCollectionID, self.sCollectionTitle))
            self.oOutStream.write(u'        <div class="f_coll_stat">%s</div>\n' % (self._computeCollectionStats()))
            self.oOutStream.write(u'        <div class="f_coll_desc">%s</div>\n' % (self.sCollectionDescription))
            self.oOutStream.write(u'      </div>\n')
            self.oOutStream.write(u'    </td>\n')
            self.oOutStream.write(u'  </tr>\n')
        else:
            self.oOutStream.write('<div class="f_coll">\n')
            self.oOutStream.write('  <div class="f_coll_r1">\n')
            self.oOutStream.write('    <div class="f_coll_icon">\n')
            self.oOutStream.write('      <div class="f_coll_icon">%s%s</a></div>\n' % (self._computeCollectionRef(), self._computeCollectionImg()))
            self.oOutStream.write('    </div>\n')
            self.oOutStream.write('    <div class="f_coll_info">\n')
            self.oOutStream.write('      <h4>%s</h4>\n' % (self.sCollectionTitle))
            self.oOutStream.write('      <div class="f_coll_stat">%s</div>\n' % (self._computeCollectionStats()))
            self.oOutStream.write('      <div class="f_coll_desc">%s</div>\n' % (self.sCollectionDescription))
            self.oOutStream.write('    </div>\n')
            self.oOutStream.write('  </div>\n')
        return

    def writeEmbeddedBegin(self):
        if bUseTables:
            self.oOutStream.write(u'  <tr class="f_coll_r2">\n')
            self.oOutStream.write(u'    <td class="f_coll_space">\n')
            self.oOutStream.write(u'    </td>\n')
            self.oOutStream.write(u'    <td class="f_coll_content">\n')
        else:
            self.oOutStream.write('  <div class="f_coll_r2">\n')
            self.oOutStream.write('    <div class="f_coll_space">\n')
            self.oOutStream.write('    </div>\n')
            self.oOutStream.write('    <div class="f_coll_content">\n')
        return

    def writeEmbeddedEnd(self):
        if bUseTables:
            self.oOutStream.write(u'    </td>\n')
            self.oOutStream.write(u'  </tr>\n')
        else:
            self.oOutStream.write('    </div>\n')
            self.oOutStream.write('  </div>\n')
        return

    
    def writeCollectionEnd(self):
        if bUseTables:
            self.oOutStream.write(u'</table>\n')
        else:
            self.oOutStream.write('</div>\n')
        return

    def _computePhotosetRef(self, sType):
        s = sType
        if s == 'thumb':
            s = None
            
        sRet = '<a href="%ssets/%s/' % (self.sUserUrl, self.sPhotosetID)
        
        if s != None:
            sRet += '%s/' % s
        sRet += '">'
        return sRet
        
    def _computePhotosetImg(self):
        return '<img src="%s" width="75" height="75" alt="%s" />' % (self.sPhotosetIcon, self.sPhotosetTitle)
        
    def _computePhotosetLink(self, sText, sType):
        s = '<span class="f_set_link_%s">' % sType
        s += '%s%s</a>' % (self._computePhotosetRef(sType), sText)
        s += '</span>'
        return s

    def writePhotosetBegin(self):
        if self.bVerbose:
            print '%s\tSet "%s" "%s" %s %d' % (self.sIndent, self.sPhotosetTitle, self.sPhotosetDescription, self.sPhotosetIcon, self.nPhotosetPhotos)
        if bUseTables:
            #self.oOutStream.write('<a name="A%s"> </a>' % (self.sPhotosetID))
            self.oOutStream.write(u'<table class="f_set">\n')
            self.oOutStream.write(u'  <tr>\n')
            self.oOutStream.write(u'    <td class="f_set_icon">\n')
            self.oOutStream.write(u'      <div class="f_set_icon">%s%s</a></div>\n' % (self._computePhotosetRef('show'), self._computePhotosetImg()))
            self.oOutStream.write(u'    </td>\n')
            self.oOutStream.write(u'    <td class="f_set_info">\n')
            self.oOutStream.write(u'      <div class="f_set_info">\n')
            self.oOutStream.write(u'        <h4><a name="A%s">%s</a></h4>\n' % (self.sPhotosetID, self.sPhotosetTitle))
            self.oOutStream.write(u'        <div class="f_set_stat">%d photos</div>\n' % (self.nPhotosetPhotos))
            self.oOutStream.write(u'        <div class="f_set_links">')
            self.oOutStream.write(u'%s' % (self._computePhotosetLink('Slideshow', 'show')))
            self.oOutStream.write(u'%s' % (self._computePhotosetLink('Thumbnails', 'thumb')))
            self.oOutStream.write(u'%s' % (self._computePhotosetLink('Details', 'detail')))
            self.oOutStream.write(u'%s' % (self._computePhotosetLink('Map', 'map')))
            self.oOutStream.write(u'</div></div>\n')
            self.oOutStream.write(u'      <div class="f_set_desc">%s</div>\n' % (self.sPhotosetDescription))
            self.oOutStream.write(u'    </td>\n')
            self.oOutStream.write(u'  </tr>\n')
            self.oOutStream.write(u'</table>\n')
        else:
            self.oOutStream.write('<div class="f_set">\n')
            self.oOutStream.write('  <div class="f_set_icon">\n')
            self.oOutStream.write('    %s\n' % (self._computePhotosetRef(None)))
            self.oOutStream.write('    %s\n' % (self._computePhotosetImg()))
            self.oOutStream.write('    </a>\n')
            self.oOutStream.write('  </div>\n')
            self.oOutStream.write('  <div class="f_set_info">\n')
            self.oOutStream.write('    <p>%s (%s photos)</p>\n' % (self.sPhotosetTitle, self.sPhotosetPhotos))
            self.oOutStream.write('    <p>%sSlideshow</a> %sThumbnails</a> %sDetails</a> %sMap</a></p>\n' % (self._computePhotosetRef('show'), self._computePhotosetRef(None), self._computePhotosetRef('detail'), self._computePhotosetRef('map')))
            self.oOutStream.write('    <p>%s</p>\n' % (self.sPhotosetDescription))
            self.oOutStream.write('  </div>\n')
            self.oOutStream.write('</div>\n')
        return
    
    def writePhotosetEnd(self):
        return

