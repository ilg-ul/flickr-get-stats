'''
Created on Sep 3, 2010

@author: ilg
'''

class Aggregate(object):
    '''
    classdocs
    '''
    def __init__(self, oTree, oWriter, bVerbose):
        '''
        Constructor
        '''
        self.oTree = oTree
        self.writer = oWriter
        self.bVerbose = bVerbose

    def run(self):
        if self.bVerbose:
            print '----------'
        self.writer.writeBegin()
        self._recurse(self.oTree, 0)
        self.writer.writeEnd()
        return

    def _recurse(self, oCollection, depth):
        sIndent = ''
        for i in range(1, depth): #@UnusedVariable
            sIndent += '\t'
        
        if oCollection.sID != None:
            sCollectionID = oCollection.sID
            sTitle = oCollection.sTitle
            sDescription = oCollection.sDescription
            sIconSmall = oCollection.sIconSmall
            sIconLarge = oCollection.sIconLarge
            self.writer.setCollection(sCollectionID, sTitle, sDescription, sIconSmall, sIconLarge)
            #
            nCollections = oCollection.nCollections
            nSets = oCollection.nSets
            nPhotos = oCollection.nPhotos
            self.writer.setStatistics(nCollections, nSets, nPhotos)
            self.writer.writeCollectionBegin()
            #
            if self.bVerbose:
                print '%s%d Collection "%s" "%s" %s %d %d %d' % (sIndent, depth, sTitle, sDescription, sIconSmall, nCollections, nSets, nPhotos)
        #
        if len(oCollection.oMembers) > 0:
            if oCollection.sID != None:
                self.writer.writeEmbeddedBegin()
            if oCollection.bChildCollections:
                for oColl in oCollection.oMembers:
                    self._recurse(oColl, depth+1)
            else:
                for oSet in oCollection.oMembers:
                    sPhotosetID = oSet.sID
                    sTitle = oSet.sTitle
                    sDescription = oSet.sDescription
                    sIcon = oSet.sIcon
                    nPhotos = oSet.nPhotos
                    #
                    self.writer.setPhotoset(sPhotosetID, sTitle, sDescription, nPhotos, sIcon)
                    self.writer.writePhotosetBegin()
                    self.writer.writePhotosetEnd()
                    #
                    if self.bVerbose:
                        print '%s\tSet "%s" "%s" %s %d' % (sIndent, sTitle, sDescription, sIcon, nPhotos)
                # end of for
            # end of if
            if oCollection.sID != None:
                self.writer.writeEmbeddedEnd()
        # end of if len()
        if oCollection.sID != None:
            self.writer.writeCollectionEnd()

        return
    
