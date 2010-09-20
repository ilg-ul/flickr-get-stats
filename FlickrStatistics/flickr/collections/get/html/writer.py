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

    def __init__(self):
        '''
        Constructor
        '''
        super(Writer, self).__init__('Main')

    def writeHeaderBegin(self):
        self.fOut.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n')
        self.fOut.write('<html>\n')
        self.fOut.write('<head>\n')
        self.fOut.write('  <title>Flickr: ilg-ul Photos</title>\n')
        self.fOut.write('  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n')
        self.fOut.write('  <link type="text/css" rel="stylesheet" href="flickr.css">\n')
        self.fOut.write('</head>\n')
        self.fOut.write('<body>\n')
        return
    
    def writeHeaderEnd(self):
        self.fOut.write('</body>\n')
        self.fOut.write('</html>\n')
        return
    
    def writeBegin(self):
        self.fOut.write('<h3>Collections</h3>\n')
        return

    def writeEnd(self):
        return
  
    def _computeCollectionRef(self):
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
            self.fOut.write('<a name="%s"></a>\n' % (self.sCollectionID))
            self.fOut.write('<table class="f_coll">\n')
            self.fOut.write('  <tr class="f_coll_r1">\n')
            self.fOut.write('    <td class="f_coll_icon">\n')
            self.fOut.write('      <div class="f_coll_icon">%s%s</a></div>\n' % (self._computeCollectionRef(), self._computeCollectionImg()))
            self.fOut.write('    </td>\n')
            self.fOut.write('    <td class="f_coll_info">\n')
            self.fOut.write('      <div class="f_coll_info">\n')
            self.fOut.write('        <h4>%s</h4>\n' % (self.sCollectionTitle))
            self.fOut.write('        <div class="f_coll_stat">%s</div>\n' % (self._computeCollectionStats()))
            self.fOut.write('        <div class="f_coll_desc">%s</div>\n' % (self.sCollectionDescription))
            self.fOut.write('      </div>\n')
            self.fOut.write('    </td>\n')
            self.fOut.write('  </tr>\n')
        else:
            self.fOut.write('<div class="f_coll">\n')
            self.fOut.write('  <div class="f_coll_r1">\n')
            self.fOut.write('    <div class="f_coll_icon">\n')
            self.fOut.write('      <div class="f_coll_icon">%s%s</a></div>\n' % (self._computeCollectionRef(), self._computeCollectionImg()))
            self.fOut.write('    </div>\n')
            self.fOut.write('    <div class="f_coll_info">\n')
            self.fOut.write('      <h4>%s</h4>\n' % (self.sCollectionTitle))
            self.fOut.write('      <div class="f_coll_stat">%s</div>\n' % (self._computeCollectionStats()))
            self.fOut.write('      <div class="f_coll_desc">%s</div>\n' % (self.sCollectionDescription))
            self.fOut.write('    </div>\n')
            self.fOut.write('  </div>\n')
        return

    def writeEmbeddedBegin(self):
        if bUseTables:
            self.fOut.write('  <tr class="f_coll_r2">\n')
            self.fOut.write('    <td class="f_coll_space">\n')
            self.fOut.write('    </td>\n')
            self.fOut.write('    <td class="f_coll_content">\n')
        else:
            self.fOut.write('  <div class="f_coll_r2">\n')
            self.fOut.write('    <div class="f_coll_space">\n')
            self.fOut.write('    </div>\n')
            self.fOut.write('    <div class="f_coll_content">\n')
        return

    def writeEmbeddedEnd(self):
        if bUseTables:
            self.fOut.write('    </td>\n')
            self.fOut.write('  </tr>\n')
        else:
            self.fOut.write('    </div>\n')
            self.fOut.write('  </div>\n')
        return

    
    def writeCollectionEnd(self):
        if bUseTables:
            self.fOut.write('</table>\n')
        else:
            self.fOut.write('</div>\n')
        return

    def _computePhotosetRef(self, s):
        if s != None:
            return '<a href="%ssets/%s/%s/">' % (self.sUserUrl, self.sPhotosetID, s)
        else:
            return '<a href="%ssets/%s/">' % (self.sUserUrl, self.sPhotosetID)
        
    def _computePhotosetImg(self):
        return '<img src="%s" width="75" height="75" alt="%s" />' % (self.sPhotosetIcon, self.sPhotosetTitle)
        
    def writePhotosetBegin(self):
        if self.bVerbose:
            print '%s\tSet "%s" "%s" %s %d' % (self.sIndent, self.sPhotosetTitle, self.sPhotosetDescription, self.sPhotosetIcon, self.nPhotosetPhotos)
        if bUseTables:
            self.fOut.write('<table border="0">\n')
            self.fOut.write('  <tr>\n')
            self.fOut.write('    <td>\n')
            self.fOut.write('      %s\n' % (self._computePhotosetRef(None)))
            self.fOut.write('      %s\n' % (self._computePhotosetImg()))
            self.fOut.write('      </a>\n')
            self.fOut.write('    </td>\n')
            self.fOut.write('    <td>\n')
            self.fOut.write('      %s<br />\n' % (self.sPhotosetTitle))
            self.fOut.write('      %s photos<br />\n' % (self.sPhotosetPhotos))
            self.fOut.write('      %sSlideshow</a> %sThumbnails</a> %sDetails</a> %sMap</a><br />\n' % (self._computePhotosetRef('show'), self._computePhotosetRef(None), self._computePhotosetRef('detail'), self._computePhotosetRef('map')))
            self.fOut.write('      %s\n' % (self.sPhotosetDescription))
            self.fOut.write('    </td>\n')
            self.fOut.write('  </td>\n')
            self.fOut.write('</table>\n')
        else:
            self.fOut.write('<div class="f_set">\n')
            self.fOut.write('  <div class="f_set_icon">\n')
            self.fOut.write('    %s\n' % (self._computePhotosetRef(None)))
            self.fOut.write('    %s\n' % (self._computePhotosetImg()))
            self.fOut.write('    </a>\n')
            self.fOut.write('  </div>\n')
            self.fOut.write('  <div class="f_set_info">\n')
            self.fOut.write('    <p>%s (%s photos)</p>\n' % (self.sPhotosetTitle, self.sPhotosetPhotos))
            self.fOut.write('    <p>%sSlideshow</a> %sThumbnails</a> %sDetails</a> %sMap</a></p>\n' % (self._computePhotosetRef('show'), self._computePhotosetRef(None), self._computePhotosetRef('detail'), self._computePhotosetRef('map')))
            self.fOut.write('    <p>%s</p>\n' % (self.sPhotosetDescription))
            self.fOut.write('  </div>\n')
            self.fOut.write('</div>\n')

        return
    
    def writePhotosetEnd(self):
        return

