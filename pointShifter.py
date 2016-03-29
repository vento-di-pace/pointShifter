# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pointShifter
                                 A QGIS plugin
 pointShifter
                              -------------------
        begin                : 2016-01-21
        copyright            : (C) 2016 by Eugene Nazarenko
        email                : eugene.v.nazarenko@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.core import QgsRelation, QgsProject
from qgis.utils import plugins
from qgis.gui import QgsEncodingFileDialog
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from pointShifterdialog import pointShifterDialog
import os, os.path
import uuid
import math



class trace:
    """
    class for tracing debug infos
    """

    def __init__(self):
        self.trace = True

    def log(message = u'All is ok! :)', debug=False, severity = 0):
        from sys import argv
        from time import strftime
        from codecs import open

        mode='ab'
        log_file = open(argv[0]+'.log', mode, 'utf-8')
        if not debug:
            print unicode(strftime(u'[%Y-%m-%d] %H:%M:%S>> '))+message
        log_file.write((unicode(strftime(u'[%Y-%m-%d] %H:%M:%S>> '))+u'%s\r\n'%message))#.encode(curr_locale_cp))

        log_file.close()

    def ce(self,string):
        if self.trace:
            self.log(str(string))
            print string


class pointShifter():

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'pointShifter_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = pointShifterDialog()
        self.tra = trace()
        self.outFilePath = ''
        self.encoding = ''
        self.inprocess = False
        self.state = ''

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/pointShifter/icon.png"),
            u"pointShifter", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&pointShifter", self.action)
#        self.dlg.pointLayerCombo.activated.connect(self.browsePointInput)
#        self.dlg.lineLayerCombo.activated.connect(self.browseLineInput)

        self.dlg.browsePushButton.clicked.connect(self.browseOutputFC)
        self.dlg.buttonBox.accepted.connect(self.applyShift)
        self.dlg.buttonBox.rejected.connect(self.cancelProcess)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&pointShifter", self.action)
        self.iface.removeToolBarIcon(self.action)

    def populateComboBox(self,combo,list,predef = '',sort = True):
        #procedure to fill specified combobox with provided list
        combo.clear()
        model=QStandardItemModel(combo)
        for elem in list:
            try:
                item = QStandardItem(unicode(elem))
            except TypeError:
                item = QStandardItem(str(elem))
            model.appendRow(item)
        if sort:
            model.sort(0)

        combo.setModel(model)
        if predef != "":
            for row in range (0,combo.count()):
                if combo.itemText(row) == predef:
                    pos = row
            try:
                combo.setCurrentIndex(pos)
            except:
                combo.insertItem(0,predef)
                combo.setCurrentIndex(0)

    def browseOutputFC(self):
        filtering="Shapefiles (*.shp *.SHP)"
        settings = QSettings()
        dirName = settings.value("/UI/lastShapefileDir")
        encode = settings.value("/UI/encoding")
        fileDialog = QgsEncodingFileDialog(None, QCoreApplication.translate("fTools", "Save output shapefile"), dirName, filtering, encode)
        fileDialog.setDefaultSuffix("shp")
        fileDialog.setFileMode(QFileDialog.AnyFile)
        fileDialog.setAcceptMode(QFileDialog.AcceptSave)
        fileDialog.setConfirmOverwrite(True)
        if not fileDialog.exec_() == QDialog.Accepted:
            return None, None
        files = fileDialog.selectedFiles()
        settings.setValue("/UI/lastShapefileDir", QFileInfo(unicode(files[0])).absolutePath())

        #return (unicode(files[0]), unicode(fileDialog.encoding()))
        self.outFilePath = unicode(files[0])
        self.encoding = unicode(fileDialog.encoding())
        self.dlg.outputLineEdit.setText(self.outFilePath)




    # run method that performs all the real work
    def run(self):

##        if not 'refFunctions' in plugins:
##            QMessageBox.critical(None, "Plugin Dependency:", "Plugin 'refFunctions' is needed.\nInstall it from Qgis repository before performing spatial joins")
##            return

        self.pointLayerSet = {}
        for layer in self.iface.legendInterface().layers():
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point:
                self.pointLayerSet[layer.name()]=layer

        self.lineLayerSet = {}
        for layer in self.iface.legendInterface().layers():
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Line:
                self.lineLayerSet[layer.name()]=layer


        self.dlg.progressBar.reset()

        cPointLayerName = "Please add point layer to map"
        if self.iface.legendInterface().currentLayer():
            if self.iface.legendInterface().currentLayer().geometryType() == QGis.Point:
                cPointLayerName = self.iface.legendInterface().currentLayer().name()
            else:
                cPointLayerName = self.pointLayerSet.keys()[0]


        cLineLayerName = "Please add line layer to map"
        if self.iface.legendInterface().currentLayer():
            if self.iface.legendInterface().currentLayer().geometryType() == QGis.Line:
                cLineLayerName = self.iface.legendInterface().currentLayer().name()
            else:
                cLineLayerName = self.lineLayerSet.keys()[0]


        self.populateComboBox(self.dlg.pointLayerCombo,self.pointLayerSet.keys(),cPointLayerName)
        self.populateComboBox(self.dlg.lineLayerCombo,self.lineLayerSet.keys(),cLineLayerName)
        # show the dialog
        self.dlg.show()


    def start_is_ref(self, start_x, start_y, end_x, end_y):
        self.tra.ce('Start coords X:%s, Y:%s'%(start_x, start_y))
        self.tra.ce('End coords X:%s, Y:%s'%(end_x, end_y))
        if start_y <> end_y and start_y < end_y:
            return True
        elif start_y <> end_y and start_y > end_y:
            return False
        elif start_y == end_y and start_x > end_y:
            return True
        elif start_y == end_y and start_x <= end_y:
            return False

    def get_moved_point(self, x1, y1, x2, y2, ref_side, start_is_ref_node, l=0.00000900):
        from math import sqrt
        #l = 0.0000090 #0.5 meters
        len_current_vector = sqrt(pow(x2-x1, 2)+pow(y2-y1, 2))
        coeff = l/len_current_vector
        x3 = y3 = 0.00000000

        side = 'R'
        if start_is_ref_node:
            side = ref_side
        else:
            if ref_side == 'R':
                side = 'L'
            elif ref_side =='L':
                side = 'R'


        if side == 'R':
            x3 =  x2 - (y1-y2)
            y3 =  y2 + (x1-x2)
        elif side == 'L':
            x3 =  x2 + (y1-y2)
            y3 =  y2 - (x1-x2)
        outX = x2 - coeff*(x2 - x3)
        outY = y2 - coeff*(y2 - y3)
        return outX, outY

    def get_point_side_from_link (self, startX, startY, pointX, pointY, endX, endY):
        return (pointX-startX)*(pointY-endY)-(pointY-startY)*(pointX-endX)

    def get_point_on_link (self, x1, y1, x2, y2, px, py):
        from math import sqrt
        class Vector:
            def __init__(self, xcoord = 0.0, ycoord =0.0):
                self.x = xcoord
                self.y = ycoord

        def VDot(v1,v2): #Vector
            return (v1.x*v2.x+v1.y*v2.y)


        def VMul(v1, A): #Vector
            return Vector(v1.x*A, v1.y*A)



        def VSub(v1,v2): #Vector;
            return Vector(v1.x-v2.x, v1.y-v2.y)

        def VLength(V):
            return sqrt(V.x ** 2 + V.y ** 2)

        def VNorm(V): #Vector;
            #vl = 0.0
            vl = VLength(V)
            if vl == 0:
                return Vector(0, 0)
            else:
                return Vector(V.x/vl, V.y/vl)

        def VProject(A,B): #Vector;
            An = VNorm(A)
            return VMul(An,VDot(An,B))

        def Perpendicular(A,B,C): #Vector;
            CA = Vector()
            CA=VSub(C,A)
            return VProject(VSub(B,A),CA)

        result = Perpendicular (Vector(x1, y1), Vector(x2, y2), Vector(px, py))

        # here is check if result point places on line segment
        B = Vector(x2, y2)
        A = Vector(x1, y1)
        C_norm = VNorm(result)
        if VLength(C_norm) == 0:
            C_norm = VNorm(VSub(B,A))
        C_norm_rev = VMul(C_norm, -1)

        AC_length = VLength(result)
        AB_length = VLength(VSub(B, A))
        BC_length = VLength(VSub(VSub(B, A), result))

        self.tra.ce(str(AB_length))
        self.tra.ce(str(BC_length))
        self.tra.ce(str(AC_length))

        one_pecent_length = AB_length*0.01
        C_rev = VMul(C_norm_rev, one_pecent_length)


        if AB_length > BC_length and AB_length > AC_length:
            self.state += ' onlink'
            return x1 + result.x, y1 + result.y
        else:
            # todo - find point before end.
            if AC_length > BC_length and AC_length > AB_length:
                result = VSub(B, C_rev)
                self.state += ' outsidelink from B'
                self.tra.ce(str(result))
                return result.x, result.y
            elif AC_length < BC_length and AC_length < AB_length:
                result = VSub(A, C_rev)
                self.state += ' outsidelink from A'
                self.tra.ce(str(result))
                return result.x, result.y

# main algorithm
    def applyShift(self):
        self.dlg.show()
        self.inprocess = True

        if self.dlg.pointLayerCombo.currentText()[:10] != 'Please add' and self.dlg.lineLayerCombo.currentText()[:10] != 'Please add':
            #prepare input layers
            pointLayer = self.pointLayerSet[self.dlg.pointLayerCombo.currentText()]
            lineLayer = self.lineLayerSet[self.dlg.lineLayerCombo.currentText()]
            self.dlg.progressBar.setMinimum(0)
            self.dlg.progressBar.setMaximum(pointLayer.featureCount())

            #prepare output layer

##            outputPointsShapeLyr.startEditing()
##            outputPointsShape = outputPointsShapeLyr.dataProvider()

##            for pntField in pointLayer.fields():
##                self.tra.ce(str(type(pntField)))
##                outputPointsShape.addAttribute(pntField)
##            outputPointsShape.addAttribute(QgsField('lat_f', QVariant.Double, 'double'))
##            outputPointsShape.addAttribute(QgsField('lon_f', QVariant.Double, 'double'))
##            outputPointsShape.addAttribute(QgsField('LINKPVID', QVariant.Int, 'integer'))
##            #outputPointsShape.addAttribute(QgsField('side', QVariant.String, 'text'))
##            outputPointsShape.addAttribute(QgsField('pfrn_d', QVariant.Double, 'double'))
##            outputPointsShape.addAttribute(QgsField('pfrn', QVariant.Int, 'integer'))
            sRs = pointLayer.crs()
            outFields = QgsFields()
            for pntField in pointLayer.fields():
                #self.tra.ce(str(type(pntField)))
                outFields.append(pntField)

            outFields.append(QgsField(u'lat_f', QVariant.Double))
            outFields.append(QgsField(u'lon_f', QVariant.Double))
            outFields.append(QgsField(u'LINKPVID', QVariant.Int))
            outFields.append(QgsField(u'REF_IN_ID', QVariant.Int))
            outFields.append(QgsField('NEW_SIDE', QVariant.String))
            outFields.append(QgsField(u'pfrn_d', QVariant.Double))
            outFields.append(QgsField(u'pfrn', QVariant.Int))
            outFields.append(QgsField(u'status', QVariant.String))

            outputPointsShape = QgsVectorFileWriter(self.outFilePath, self.encoding, outFields, QGis.WKBPoint, sRs)

            #self.tra.ce(str(type(outputPointsShape)))


            #targetLayerFields = [field.name() for field in targetLayer.pendingFields()]
            try:
                self.tra.ce('setup layers for processing.')
                pointFeatures = pointLayer.getFeatures()
                lineFeatures = lineLayer.getFeatures()
                # go through all points
                sindex = QgsSpatialIndex()
                inFeat = QgsFeature()
                self.tra.ce('create Spatial Index object and fill it')
                while lineFeatures.nextFeature(inFeat):
                    sindex.insertFeature(inFeat)
                pntIndex = -1
                self.dlg.progressBar.reset()

                self.tra.ce('start processing')
                for pnt in pointFeatures:
                    self.state = 'OK'
                    try:
                        pntIndex=+1
                        if not self.inprocess:break
                        #get point geometry object
                        pntGeom = pnt.geometry()
                        pnt_xy = pntGeom.asPoint() #QgsPoint type
                        #find nearest 5 links to it (5 cause this is not a fact that one link will be closest)
                        lineID_list = sindex.nearestNeighbor(pnt_xy,5)
                        self.tra.ce('nearest line id %s'%lineID_list)
                        linesRequest = QgsFeatureRequest()
                        linesRequest.setFilterFids(lineID_list)

                        lineFeatIter = lineLayer.getFeatures(linesRequest)

                        lineFeat = QgsFeature()
                        # find closests link to point
                        min_dist = 181.0
                        min_dist = float(self.dlg.lineEdit_2.text())
                        lineID=None
                        while lineFeatIter.nextFeature(lineFeat):
                            self.tra.ce(lineFeat.id())
                            self.tra.ce(lineFeat.geometry().distance(pntGeom))
                            if lineFeat.geometry().distance(pntGeom) < min_dist:
                                min_dist = lineFeat.geometry().distance(pntGeom)
                                lineID = lineFeat.id()
                        if lineID:
                            lineFeatIter = lineLayer.getFeatures(QgsFeatureRequest(lineID))
                            lineFeatIter.nextFeature(lineFeat)

                            #OUTPUT
                            linkPVID = lineFeat.attribute('LINK_ID')
                            self.tra.ce('LINK_ID: %s'%linkPVID)

                            Ref_In_Id = -1
                            try:
                                Ref_In_Id = lineFeat.attribute('REF_IN_ID')
                            except:
                                Ref_In_Id = -1

                            self.tra.ce('REF_IN_ID: %s'%Ref_In_Id)


                            #continue calculation
                            lineGeom = lineFeat.geometry()
                            pntOnLine = QgsPoint(0,0) # future point on line
                            afterVertex = 0
                            pntTrueSide = 0
                            closeSegResult = lineGeom.closestSegmentWithContext(pnt_xy) #, pntOnLine, afterVertex, pntTrueSide values go to the closeSegResult
                            self.tra.ce('Input point coordinates\n%s'%str(pnt_xy))
                            self.tra.ce('closestSegment.. method result\n%s'%str(closeSegResult))

                            #pntOnLine = closeSegResult[1]
                            afterVertex = closeSegResult[2]
                            #pntTrueSide = closeSegResult[3]

                            #    def get_point_on_link (x1, y1, x2, y2, px, py):
                            x,y = self.get_point_on_link(lineGeom.vertexAt(afterVertex-1).x(), lineGeom.vertexAt(afterVertex-1).y(), lineGeom.vertexAt(afterVertex).x(), lineGeom.vertexAt(afterVertex).y(), pnt_xy.x(), pnt_xy.y())
                            pntOnLine = QgsPoint(x, y)



                            vertexIndex = 0
                            lineLength2Point = 0.0
                            self.tra.ce('after vertex index %s'%afterVertex)
                            while lineGeom.vertexAt(vertexIndex) <> QgsPoint(0,0):
                                self.tra.ce('vertex index %s'%vertexIndex)
                                vertexIndex+=1
                                if vertexIndex < afterVertex:
                                    lineLength2Point += math.sqrt(math.pow((lineGeom.vertexAt(vertexIndex).y()-lineGeom.vertexAt(vertexIndex-1).y()), 2)+pow((lineGeom.vertexAt(vertexIndex).x()-lineGeom.vertexAt(vertexIndex-1).x()), 2))
                            vertexIndex = vertexIndex-1
                            self.tra.ce('Segment length is %s map units'%lineLength2Point)

                            startLinePnt = lineGeom.vertexAt(0)
                            endLinePoint = lineGeom.vertexAt(vertexIndex)
                            self.tra.ce('Last vertex index %s'%vertexIndex)
                            #remark: code for define ref point of link
                            self.tra.ce('origin point %s, %s'%(pntOnLine.x(),pntOnLine.y()))

                            start_point_is_refnode = self.start_is_ref(startLinePnt.x(), startLinePnt.y(), endLinePoint.x(), endLinePoint.y())



                            self.tra.ce('Start point is ref node: %s'%start_point_is_refnode)
                            stSide=''
                            #define side from street
                            if self.dlg.checkBox.isChecked():
                                #from attribute value of point layer
                                self.tra.ce('SIDE taken from attribute')

                                stSide = pnt.attribute('SIDE')
                                self.tra.ce('SIDE should be %s'%stSide)
                            else:
                                self.tra.ce('SIDE taken from real point position')
                                #or from reality
                                street_side_code =  self.get_point_side_from_link(lineGeom.vertexAt(afterVertex-1).x(), lineGeom.vertexAt(afterVertex-1).y(), pnt_xy.x(), pnt_xy.y(), lineGeom.vertexAt(afterVertex).x(), lineGeom.vertexAt(afterVertex).y())
                                if start_point_is_refnode:
                                    if street_side_code >= 0:
                                        stSide = 'L'
                                    elif street_side_code < 0:
                                        stSide = 'R'
                                else:
                                    if street_side_code >= 0:
                                        stSide = 'R'
                                    elif street_side_code < 0:
                                        stSide = 'L'
                                self.tra.ce('SIDE should be %s'%stSide)


                            #calc shifted point
                            self.tra.ce('point is shifting to %s map units'% float(self.dlg.lineEdit.text()))
                            #x,y = self.get_moved_point(lineGeom.vertexAt(afterVertex-1).x(), lineGeom.vertexAt(afterVertex-1).y(), pntOnLine.x(), pntOnLine.y(), stSide, float(self.dlg.lineEdit.text()))

                            self.tra.ce(lineGeom.vertexAt(afterVertex-1).x())
                            self.tra.ce(lineGeom.vertexAt(afterVertex-1).y())
                            self.tra.ce(pntOnLine.x())
                            self.tra.ce(pntOnLine.y())

                            x,y = self.get_moved_point(lineGeom.vertexAt(afterVertex-1).x(), lineGeom.vertexAt(afterVertex-1).y(), pntOnLine.x(), pntOnLine.y(), stSide, start_point_is_refnode, float(self.dlg.lineEdit.text()))

                            self.tra.ce('origin point %s, %s'%(x,y))
                            #OUTPUT
                            shiftedPoint = QgsPoint(x,y)

                            #calc percent from refnode
                            lastSegPartialLen = math.sqrt(math.pow((lineGeom.vertexAt(afterVertex-1).y()-pntOnLine.y()), 2)+pow((lineGeom.vertexAt(afterVertex-1).x()-pntOnLine.x()), 2))
                            percentFromStart = ((lineLength2Point+lastSegPartialLen)*100)/lineGeom.length()

                            self.tra.ce('Percent from ref node: %s'%percentFromStart)
                            if not start_point_is_refnode:
                                #OUTPUT
                                percentFromStart = 100 - percentFromStart
                            if percentFromStart < 1:
                                percentFromStart = 1
                            if percentFromStart > 99:
                                percentFromStart = 99









                    except Exception as e:
                        self.tra.ce(e.message)
                        self.state += e.message


                    self.tra.ce(str(pointLayer.fields().allAttributesList()))
                    #store procedure
                    currentFeature = QgsFeature(outFields)
                    currentFeature.initAttributes(outFields.count())

                    self.tra.ce(outFields.count())
                    self.tra.ce(currentFeature.fields().count())

                    attributes = pnt.attributes()

                    attributes += [shiftedPoint.y(), shiftedPoint.x(), linkPVID, Ref_In_Id, stSide, percentFromStart, int(percentFromStart), self.state]

                    self.tra.ce(attributes)

                    currentFeature.setGeometry(QgsGeometry.fromPoint(shiftedPoint))
                    #currentFeature.setGeometry(QgsGeometry.fromPoint(pntOnLine))
                    currentFeature.setAttributes(attributes)

                    self.tra.ce(currentFeature.attributes())

                    outputPointsShape.addFeature(currentFeature)

                    del currentFeature

                #update progressBar
                self.dlg.progressBar.setValue(pntIndex)
                self.dlg.update()
            finally:
                del outputPointsShape



            outputPointsShapeLyr = QgsVectorLayer(self.outFilePath, u'ShiftedPoints', 'ogr')  #add sRs here (it is from point layer)
            QgsMapLayerRegistry.instance().addMapLayers([outputPointsShapeLyr])

            self.dlg.hide()


    def cancelProcess(self):
        self.inprocess = False