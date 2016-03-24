# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\GitHub_PointShifter_repo\ui_pointShifter.ui'
#
# Created: Thu Mar 24 14:01:54 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_pointShifter(object):
    def setupUi(self, pointShifter):
        pointShifter.setObjectName(_fromUtf8("pointShifter"))
        pointShifter.resize(379, 294)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(pointShifter.sizePolicy().hasHeightForWidth())
        pointShifter.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/pointShifter/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pointShifter.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(pointShifter)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(pointShifter)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label)
        self.pointLayerCombo = QtGui.QComboBox(pointShifter)
        self.pointLayerCombo.setObjectName(_fromUtf8("pointLayerCombo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.SpanningRole, self.pointLayerCombo)
        self.label_2 = QtGui.QLabel(pointShifter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.label_2)
        self.lineLayerCombo = QtGui.QComboBox(pointShifter)
        self.lineLayerCombo.setObjectName(_fromUtf8("lineLayerCombo"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.lineLayerCombo)
        self.progressBar = QtGui.QProgressBar(pointShifter)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.formLayout.setWidget(14, QtGui.QFormLayout.SpanningRole, self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(pointShifter)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(15, QtGui.QFormLayout.SpanningRole, self.buttonBox)
        self.label_3 = QtGui.QLabel(pointShifter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(9, QtGui.QFormLayout.SpanningRole, self.label_3)
        self.outputLineEdit = QtGui.QLineEdit(pointShifter)
        self.outputLineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.outputLineEdit.setInputMask(_fromUtf8(""))
        self.outputLineEdit.setText(_fromUtf8(""))
        self.outputLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.outputLineEdit.setObjectName(_fromUtf8("outputLineEdit"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.LabelRole, self.outputLineEdit)
        self.lineEdit = QtGui.QLineEdit(pointShifter)
        self.lineEdit.setInputMask(_fromUtf8(""))
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.lineEdit)
        self.label_4 = QtGui.QLabel(pointShifter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.label_4)
        self.browsePushButton = QtGui.QPushButton(pointShifter)
        self.browsePushButton.setMinimumSize(QtCore.QSize(70, 20))
        self.browsePushButton.setObjectName(_fromUtf8("browsePushButton"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.FieldRole, self.browsePushButton)
        self.checkBox = QtGui.QCheckBox(pointShifter)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.checkBox)
        self.label_5 = QtGui.QLabel(pointShifter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_2 = QtGui.QLineEdit(pointShifter)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777214, 16777215))
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.SpanningRole, self.lineEdit_2)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(pointShifter)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), pointShifter.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), pointShifter.reject)
        QtCore.QMetaObject.connectSlotsByName(pointShifter)

    def retranslateUi(self, pointShifter):
        pointShifter.setWindowTitle(_translate("pointShifter", "pointShifter (aka Vzhik)", None))
        self.label.setText(_translate("pointShifter", "Points layer", None))
        self.label_2.setText(_translate("pointShifter", "Polyline layer", None))
        self.label_3.setText(_translate("pointShifter", "Output layer", None))
        self.lineEdit.setText(_translate("pointShifter", "0.000045", None))
        self.label_4.setText(_translate("pointShifter", "Distance from between point and line (Map Units)", None))
        self.browsePushButton.setText(_translate("pointShifter", "Browse...", None))
        self.checkBox.setText(_translate("pointShifter", "Use point side from attribute \"SIDE\" instead of reality", None))
        self.label_5.setText(_translate("pointShifter", "Maximum search distance between point and line", None))
        self.lineEdit_2.setText(_translate("pointShifter", "0.00045", None))

import resources_rc
