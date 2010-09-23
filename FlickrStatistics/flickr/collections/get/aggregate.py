'''
Created on Sep 3, 2010

@author: ilg
'''
import os

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

    def runSingle(self, sFileName):
        if self.bVerbose:
            print '----- Aggregate -----'
        
        self.oMainWriter.setUserUrl(self.oTree.getUserUrl())
        self.oMainWriter.setVerbose(self.bVerbose)

        for oWr in self.oWriters:
            oWr.setUserUrl(self.oTree.getUserUrl())
            oWr.setVerbose(self.bVerbose)

        fOut = open(sFileName, 'w')

        self._oneFile(self.oTree.getRoot(), fOut)

        fOut.close()

        return

    def runMulti(self, sFolderName):
        if self.bVerbose:
            print '----- Aggregate index -----'
        
        self.oMainWriter.setUserUrl(self.oTree.getUserUrl())
        self.oMainWriter.setVerbose(self.bVerbose)

        for oWr in self.oWriters:
            oWr.setUserUrl(self.oTree.getUserUrl())
            oWr.setVerbose(self.bVerbose)

        oRoot = self.oTree.getRoot()
        
        sFileName = sFolderName+'index.html'
        fOut = open(sFileName, 'w')
        # do not output sets for index page
        self._oneFile(oRoot, False, fOut)   
        fOut.close()
        
        for oCol in oRoot.oMembers:
            print '----- Aggregate %s -----' % oCol.sTitle
            print oCol.sTitle

            sN = 'year-'+oCol.sTitle
            sFN = sFolderName + sN
            if not os.path.exists(sFN):
                os.makedirs(sFN)
            elif not os.path.isdir(sFN):
                print '%s not a folder' % sFN
                return 2
            
            sFileName = sFN+'/index.html'
            fOut = open(sFileName, 'w')
            # called for each first level collection
            # output sets for all other detail pages
            self._oneFile(oCol, True, fOut)
            fOut.close()

        return 0

    def _oneFile(self, oRoot, bOutputSets, fOut):
        self.oMainWriter.setWriter(fOut)
        self.oMainWriter.writeHeaderBegin()

        # currently only one writer, for TOC
        if self.oWriters != None:
            for oWr in self.oWriters:
                if self.bVerbose:
                    print '----- %s -----' % (oWr.sName)
                oWr.setWriter(fOut)
                oWr.writeBegin()
                oWr.setDepth(0)
                self._recurse(oRoot, '', bOutputSets, oWr)
                oWr.writeEnd()                

        if self.bVerbose:
            print '----- %s -----' % (self.oMainWriter.sName)
        sBeg = 'Collections'
        if bOutputSets:
            sBeg += ' and Albums'
        self.oMainWriter.writeBegin(sBeg)
        self.oMainWriter.setDepth(0)
        self._recurse(oRoot, '', bOutputSets, self.oMainWriter)
        self.oMainWriter.writeEnd()

        self.oMainWriter.writeHeaderEnd()
        return
        
    def _recurse(self, oCollection, sHierarchicalDepth, bOutputSets, oWriter):
        # first compute if we need to output root node
        bOutputRootCollection = True
        if oCollection.sID == None or oWriter.nDepth == 0:
                bOutputRootCollection = False                
        # skip root node
        if bOutputRootCollection:
            sCollectionID = oCollection.sID
            sTitle = oCollection.sTitle
            sDescription = oCollection.sDescription
            sIconSmall = oCollection.sIconSmallUrl
            sIconLarge = oCollection.sIconLargeUrl
            oWriter.setCollection(sCollectionID, sTitle, sDescription, sIconSmall, sIconLarge)
            oWriter.setHierarchicalDepth(sHierarchicalDepth)

            nCollections = oCollection.nCollections
            nSets = oCollection.nSets
            nPhotos = oCollection.nPhotos
            oWriter.setStatistics(nCollections, nSets, nPhotos)
            oWriter.writeCollectionBegin()

        if len(oCollection.oMembers) > 0:
            if oCollection.bHasChildCollections:
                if bOutputRootCollection:
                    oWriter.writeEmbeddedBegin()
                i = 0
                for oColl in oCollection.oMembers:
                    oWriter.incDepth()
                    i += 1
                    if sHierarchicalDepth == '':
                        sH = '%d' % i
                    else:
                        sH = '%s.%d' % (sHierarchicalDepth, i)
                    self._recurse(oColl, sH, bOutputSets, oWriter)
                    oWriter.decDepth()
                if bOutputRootCollection:
                    oWriter.writeEmbeddedEnd()
            elif bOutputSets and len(oCollection.oMembers) > 0:
                oWriter.writeEmbeddedBegin()
                i = 0
                for oSet in oCollection.oMembers:
                    i += 1
                    if sHierarchicalDepth == '':
                        sH = '%d' % i
                    else:
                        sH = '%s.%d' % (sHierarchicalDepth, i)
                    oWriter.setHierarchicalDepth(sH)
                    
                    sPhotosetID = oSet.sID
                    sTitle = oSet.sTitle
                    sDescription = oSet.sDescription
                    sIcon = oSet.sIconUrl
                    nPhotos = oSet.nPhotos

                    oWriter.setPhotoset(sPhotosetID, sTitle, sDescription, nPhotos, sIcon)
                    oWriter.writePhotosetBegin()
                    oWriter.writePhotosetEnd()
                # end of for
                oWriter.writeEmbeddedEnd()
            # end of if
        # end of if len()
        if bOutputRootCollection:
            oWriter.writeCollectionEnd()

        return

