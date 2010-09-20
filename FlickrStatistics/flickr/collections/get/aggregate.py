'''
Created on Sep 3, 2010

@author: ilg
'''

class Aggregate(object):
    '''
    classdocs
    '''
    def __init__(self, oTree, oMainWriter, oWriters, bVerbose):
        '''
        Constructor
        '''
        self.oTree = oTree
        self.oMainWriter = oMainWriter
        self.oWriters = oWriters
        self.bVerbose = bVerbose

    def run(self):
        if self.bVerbose:
            print '----- Aggregate -----'
        self.oMainWriter.writeHeaderBegin()
        if self.oWriters != None:
            for oWr in self.oWriters:
                if self.bVerbose:
                    print '----- %s -----' % (oWr.sName)
                oWr.writeBegin()
                oWr.setDepth(0)
                self._recurse(self.oTree, oWr, '')
                oWr.writeEnd()                

        if self.bVerbose:
            print '----- %s -----' % (self.oMainWriter.sName)
        self.oMainWriter.writeBegin()
        self.oMainWriter.setDepth(0)
        self._recurse(self.oTree, self.oMainWriter, '')
        self.oMainWriter.writeEnd()

        self.oMainWriter.writeHeaderEnd()
        return

    def _recurse(self, oCollection, oWriter, sHierarchicalDepth):
        # skip special root note, used only for grouping
        if oCollection.sID != None:
            sCollectionID = oCollection.sID
            sTitle = oCollection.sTitle
            sDescription = oCollection.sDescription
            sIconSmall = oCollection.sIconSmall
            sIconLarge = oCollection.sIconLarge
            oWriter.setCollection(sCollectionID, sTitle, sDescription, sIconSmall, sIconLarge)
            oWriter.setHierarchicalDepth(sHierarchicalDepth)

            nCollections = oCollection.nCollections
            nSets = oCollection.nSets
            nPhotos = oCollection.nPhotos
            oWriter.setStatistics(nCollections, nSets, nPhotos)
            oWriter.writeCollectionBegin()

        if len(oCollection.oMembers) > 0:
            if oCollection.sID != None:
                oWriter.writeEmbeddedBegin()
            if oCollection.bChildCollections:
                i = 0
                for oColl in oCollection.oMembers:
                    oWriter.incDepth()
                    i += 1
                    if sHierarchicalDepth == '':
                        sH = '%d' % i
                    else:
                        sH = '%s.%d' % (sHierarchicalDepth, i)
                    self._recurse(oColl, oWriter, sH)
                    oWriter.decDepth()
            else:
                for oSet in oCollection.oMembers:
                    sPhotosetID = oSet.sID
                    sTitle = oSet.sTitle
                    sDescription = oSet.sDescription
                    sIcon = oSet.sIcon
                    nPhotos = oSet.nPhotos
                    #
                    oWriter.setPhotoset(sPhotosetID, sTitle, sDescription, nPhotos, sIcon)
                    oWriter.writePhotosetBegin()
                    oWriter.writePhotosetEnd()
                # end of for
            # end of if
            if oCollection.sID != None:
                oWriter.writeEmbeddedEnd()
        # end of if len()
        if oCollection.sID != None:
            oWriter.writeCollectionEnd()

        return

