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


    def _initWriters(self):

        self.oMainWriter.setUserUrl(self.oTree.getUserUrl())
        self.oMainWriter.setVerbose(self.bVerbose)

        for oWr in self.oWriters:
            oWr.setUserUrl(self.oTree.getUserUrl())
            oWr.setVerbose(self.bVerbose)

        return


    def runSingleOutput(self, oRoot, bOutputSets, dRemapUrl, oOutStream):

        self._initWriters()
        self._oneRun(oRoot, bOutputSets, dRemapUrl, oOutStream)

        return


    def _runSingleFile(self, oNode, bOutputSets, sFolderName, sSubFolder, dRemapUrl):
        
        sN = sSubFolder + '/'
        sFN = sFolderName + sN
        if not os.path.exists(sFN):
            os.makedirs(sFN)
        elif not os.path.isdir(sFN):
            print '%s not a folder' % sFN
            return 2
            
        sFileName = sFN + 'index.html'
        oOutStream = open(sFileName, 'w')
        # do not output sets for index page
        self._oneRun(oNode, bOutputSets, dRemapUrl, oOutStream)   
        oOutStream.close()
        
        return 0
        

    def runMultiFolder(self, sFolderName):

        self._initWriters()
        
        oRoot = self.oTree.getRoot()
        oRoot.sTitle = 'index'

        dRemapUrl = {}
        for oNode in oRoot.oMembers:
            dRemapUrl[oNode.sID] = '../%s/index.html' % oNode.sTitle
        
        iRet = self._runSingleFile(oRoot, False, sFolderName, 'index', dRemapUrl)
        if iRet != 0:
            return iRet
        
        for oCol in oRoot.oMembers:
            self._runSingleFile(oCol, True, sFolderName, oCol.sTitle, dRemapUrl)
            if iRet != 0:
                return iRet

        return 0


    def _oneRun(self, oRoot, bOutputSets, dRemapUrl, oOutStream):

        if self.bVerbose:
            print '--- Aggregate %s ---' % oRoot.sTitle
        
        self.oMainWriter.setOutputStream(oOutStream)
        self.oMainWriter.writeHeaderBegin()

        # currently only one writer, for TOC
        if self.oWriters != None:
            for oWr in self.oWriters:
                if self.bVerbose:
                    print '----- %s -----' % (oWr.sName)
                oWr.setOutputStream(oOutStream)
                oWr.writeBegin()
                oWr.setDepth(0)
                self._recurseOneRun(oRoot, '', bOutputSets, dRemapUrl, oWr)
                oWr.writeEnd()                

        if self.bVerbose:
            print '----- %s -----' % (self.oMainWriter.sName)
        sBeg = 'Collections'
        if bOutputSets:
            sBeg += ' and Albums'
        self.oMainWriter.writeBegin(sBeg)
        self.oMainWriter.setDepth(0)
        self._recurseOneRun(oRoot, '', bOutputSets, dRemapUrl, self.oMainWriter)
        self.oMainWriter.writeEnd()

        self.oMainWriter.writeHeaderEnd()

        return

        
    def _recurseOneRun(self, oCollection, sHierarchicalDepth, bOutputSets, dRemapUrl, oWriter):
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
            if oCollection.bHasChildrenCollections:
                if bOutputRootCollection:
                    oWriter.writeEmbeddedBegin()
                i = 0
                for oColl in oCollection.oMembers:
                    sRemapUrl = None

                    # save Local Url
                    sSaveLocalUrl = oWriter.sLocalUrl
                    
                    sCollectionId = oColl.sID
                    if dRemapUrl != None and sCollectionId in dRemapUrl:
                        # if defined, remap to local Url
                        sRemapUrl = dRemapUrl[sCollectionId]
                        oWriter.setLocalUrl(sRemapUrl)
                    
                    oWriter.incDepth()
                    i += 1
                    if sHierarchicalDepth == '':
                        sH = '%d' % i
                    else:
                        sH = '%s.%d' % (sHierarchicalDepth, i)
                    self._recurseOneRun(oColl, sH, bOutputSets, dRemapUrl, oWriter)
                    oWriter.decDepth()
                    
                    # restore Local Url
                    oWriter.setLocalUrl(sSaveLocalUrl)
                        
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

