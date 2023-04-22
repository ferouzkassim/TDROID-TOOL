# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newpycuteg.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName("main")
        main.setEnabled(True)
        main.resize(1857, 1468)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(219, 219, 219))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        main.setPalette(palette)
        main.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main.setWindowIcon(icon)
        main.setWindowOpacity(1.0)
        main.setToolTip("")
        main.setToolTipDuration(0)
        main.setStatusTip("")
        main.setWhatsThis("")
        main.setAccessibleName("")
        main.setAccessibleDescription("")
        main.setLayoutDirection(QtCore.Qt.LeftToRight)
        main.setAutoFillBackground(False)
        main.setStyleSheet("background-color: rgb(219, 219, 219);")
        main.setWindowFilePath("")
        self.verticalLayout = QtWidgets.QVBoxLayout(main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tablet = QtWidgets.QTabWidget(main)
        self.tablet.setEnabled(True)
        self.tablet.setStyleSheet("font: 12pt \"Segoe MDL2 Assets\";\n"
"background-color: rgb(255, 255, 255);\n"
"")
        self.tablet.setTabPosition(QtWidgets.QTabWidget.South)
        self.tablet.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tablet.setIconSize(QtCore.QSize(38, 38))
        self.tablet.setMovable(True)
        self.tablet.setObjectName("tablet")
        self.samsungtab = QtWidgets.QWidget()
        self.samsungtab.setObjectName("samsungtab")
        self.groupBox = QtWidgets.QGroupBox(self.samsungtab)
        self.groupBox.setGeometry(QtCore.QRect(-10, 0, 991, 711))
        self.groupBox.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(80, 50, 311, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(670, 50, 311, 41))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(570, 50, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("font: 6pt \"Segoe MDL2 Assets\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setPointSize(6)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("font: 6pt \"Segoe MDL2 Assets\";")
        self.label_3.setObjectName("label_3")
        self.modelselector = QtWidgets.QComboBox(self.groupBox)
        self.modelselector.setGeometry(QtCore.QRect(360, 110, 311, 41))
        self.modelselector.setMaxVisibleItems(10)
        self.modelselector.setObjectName("modelselector")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 100, 981, 611))
        self.widget.setStyleSheet("background-color: rgb(255, 189, 0);")
        self.widget.setObjectName("widget")
        self.write_security = QtWidgets.QPushButton(self.widget)
        self.write_security.setGeometry(QtCore.QRect(770, 520, 221, 53))
        self.write_security.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.write_security.setAutoDefault(True)
        self.write_security.setFlat(False)
        self.write_security.setObjectName("write_security")
        self.Fixbaseband = QtWidgets.QPushButton(self.widget)
        self.Fixbaseband.setGeometry(QtCore.QRect(0, 430, 221, 53))
        self.Fixbaseband.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.Fixbaseband.setAutoDefault(True)
        self.Fixbaseband.setFlat(False)
        self.Fixbaseband.setObjectName("Fixbaseband")
        self.reset_frp = QtWidgets.QPushButton(self.widget)
        self.reset_frp.setGeometry(QtCore.QRect(-10, 330, 221, 46))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.reset_frp.setPalette(palette)
        self.reset_frp.setFocusPolicy(QtCore.Qt.NoFocus)
        self.reset_frp.setStatusTip("")
        self.reset_frp.setWhatsThis("")
        self.reset_frp.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.reset_frp.setAutoFillBackground(False)
        self.reset_frp.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.reset_frp.setCheckable(False)
        self.reset_frp.setAutoDefault(False)
        self.reset_frp.setDefault(True)
        self.reset_frp.setFlat(False)
        self.reset_frp.setObjectName("reset_frp")
        self.Read_security = QtWidgets.QPushButton(self.widget)
        self.Read_security.setGeometry(QtCore.QRect(770, 400, 221, 53))
        self.Read_security.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.Read_security.setAutoDefault(True)
        self.Read_security.setFlat(False)
        self.Read_security.setObjectName("Read_security")
        self.Read_info_cp = QtWidgets.QPushButton(self.widget)
        self.Read_info_cp.setGeometry(QtCore.QRect(0, 240, 211, 46))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.Read_info_cp.setPalette(palette)
        self.Read_info_cp.setFocusPolicy(QtCore.Qt.NoFocus)
        self.Read_info_cp.setStatusTip("")
        self.Read_info_cp.setWhatsThis("")
        self.Read_info_cp.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Read_info_cp.setAutoFillBackground(False)
        self.Read_info_cp.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.Read_info_cp.setCheckable(False)
        self.Read_info_cp.setAutoDefault(False)
        self.Read_info_cp.setDefault(True)
        self.Read_info_cp.setFlat(False)
        self.Read_info_cp.setObjectName("Read_info_cp")
        self.MountNetwork = QtWidgets.QPushButton(self.widget)
        self.MountNetwork.setGeometry(QtCore.QRect(0, 530, 216, 53))
        self.MountNetwork.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.MountNetwork.setAutoDefault(True)
        self.MountNetwork.setFlat(False)
        self.MountNetwork.setObjectName("MountNetwork")
        self.Write_Efs = QtWidgets.QPushButton(self.widget)
        self.Write_Efs.setGeometry(QtCore.QRect(770, 290, 221, 53))
        self.Write_Efs.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.Write_Efs.setObjectName("Write_Efs")
        self.Read_Efs = QtWidgets.QPushButton(self.widget)
        self.Read_Efs.setGeometry(QtCore.QRect(770, 180, 221, 53))
        self.Read_Efs.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.Read_Efs.setObjectName("Read_Efs")
        self.Read_info_adb = QtWidgets.QPushButton(self.widget)
        self.Read_info_adb.setGeometry(QtCore.QRect(0, 150, 211, 46))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.Read_info_adb.setPalette(palette)
        self.Read_info_adb.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.Read_info_adb.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Read_info_adb.setStatusTip("")
        self.Read_info_adb.setWhatsThis("")
        self.Read_info_adb.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Read_info_adb.setAutoFillBackground(False)
        self.Read_info_adb.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(85, 170, 0);")
        self.Read_info_adb.setCheckable(False)
        self.Read_info_adb.setChecked(False)
        self.Read_info_adb.setAutoDefault(False)
        self.Read_info_adb.setDefault(True)
        self.Read_info_adb.setFlat(False)
        self.Read_info_adb.setObjectName("Read_info_adb")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(70, 20, 241, 31))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.write_security.raise_()
        self.Fixbaseband.raise_()
        self.Read_security.raise_()
        self.MountNetwork.raise_()
        self.Write_Efs.raise_()
        self.Read_Efs.raise_()
        self.Read_info_adb.raise_()
        self.Read_info_cp.raise_()
        self.reset_frp.raise_()
        self.label.raise_()
        self.widget.raise_()
        self.comboBox.raise_()
        self.comboBox_2.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.modelselector.raise_()
        self.groupBox_2 = QtWidgets.QGroupBox(self.samsungtab)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 690, 991, 651))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.groupBox_2.setObjectName("groupBox_2")
        self.frame = QtWidgets.QFrame(self.groupBox_2)
        self.frame.setGeometry(QtCore.QRect(0, 60, 981, 591))
        self.frame.setStyleSheet("font: 75 8pt \"Sitka Small\";\n"
"border-color: rgb(41, 91, 255);\n"
"gridline-color: rgb(0, 0, 127);\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(218, 218, 218);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.readd = QtWidgets.QPushButton(self.frame)
        self.readd.setGeometry(QtCore.QRect(820, 530, 150, 46))
        self.readd.setAutoFillBackground(False)
        self.readd.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(85, 170, 0);")
        self.readd.setDefault(True)
        self.readd.setFlat(False)
        self.readd.setObjectName("readd")
        self.flashsmsng = QtWidgets.QPushButton(self.frame)
        self.flashsmsng.setGeometry(QtCore.QRect(10, 530, 150, 46))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.flashsmsng.sizePolicy().hasHeightForWidth())
        self.flashsmsng.setSizePolicy(sizePolicy)
        self.flashsmsng.setBaseSize(QtCore.QSize(1, 1))
        self.flashsmsng.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.flashsmsng.setAutoFillBackground(False)
        self.flashsmsng.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(85, 170, 0);")
        self.flashsmsng.setInputMethodHints(QtCore.Qt.ImhNone)
        self.flashsmsng.setAutoDefault(False)
        self.flashsmsng.setDefault(False)
        self.flashsmsng.setFlat(False)
        self.flashsmsng.setObjectName("flashsmsng")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(210, 80, 771, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 220, 771, 41))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(210, 150, 771, 41))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_4.setGeometry(QtCore.QRect(210, 290, 771, 41))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_5.setGeometry(QtCore.QRect(210, 360, 771, 41))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_6.setGeometry(QtCore.QRect(210, 440, 771, 41))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setGeometry(QtCore.QRect(0, 80, 132, 29))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_2.setGeometry(QtCore.QRect(0, 240, 132, 29))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_3.setGeometry(QtCore.QRect(0, 310, 132, 29))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_4.setGeometry(QtCore.QRect(0, 450, 181, 31))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_5.setGeometry(QtCore.QRect(0, 380, 132, 29))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_6.setGeometry(QtCore.QRect(0, 160, 132, 29))
        self.checkBox_6.setObjectName("checkBox_6")
        self.radioButton = QtWidgets.QRadioButton(self.frame)
        self.radioButton.setGeometry(QtCore.QRect(190, 540, 156, 29))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.frame)
        self.radioButton_2.setGeometry(QtCore.QRect(610, 540, 156, 29))
        self.radioButton_2.setObjectName("radioButton_2")
        self.checkBox_7 = QtWidgets.QCheckBox(self.frame)
        self.checkBox_7.setGeometry(QtCore.QRect(10, 10, 132, 29))
        self.checkBox_7.setObjectName("checkBox_7")
        self.rebootdload = QtWidgets.QPushButton(self.frame)
        self.rebootdload.setGeometry(QtCore.QRect(360, 530, 231, 46))
        self.rebootdload.setAutoFillBackground(False)
        self.rebootdload.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(85, 170, 0);")
        self.rebootdload.setDefault(True)
        self.rebootdload.setFlat(False)
        self.rebootdload.setObjectName("rebootdload")
        self.logfield = QtWidgets.QTextEdit(self.samsungtab)
        self.logfield.setGeometry(QtCore.QRect(990, 0, 831, 1341))
        self.logfield.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.logfield.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logfield.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logfield.setLineWidth(7)
        self.logfield.setObjectName("logfield")
        self.logfield.raise_()
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.tablet.addTab(self.samsungtab, "")
        self.adbtab = QtWidgets.QWidget()
        self.adbtab.setObjectName("adbtab")
        self.logfield_2 = QtWidgets.QTextEdit(self.adbtab)
        self.logfield_2.setGeometry(QtCore.QRect(980, 0, 831, 1341))
        self.logfield_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.logfield_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logfield_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logfield_2.setLineWidth(7)
        self.logfield_2.setObjectName("logfield_2")
        self.tablet.addTab(self.adbtab, "")
        self.fatsboottab = QtWidgets.QWidget()
        self.fatsboottab.setObjectName("fatsboottab")
        self.typeselection = QtWidgets.QComboBox(self.fatsboottab)
        self.typeselection.setGeometry(QtCore.QRect(0, 0, 331, 31))
        self.typeselection.setCurrentText("")
        self.typeselection.setObjectName("typeselection")
        self.logfield_3 = QtWidgets.QTextEdit(self.fatsboottab)
        self.logfield_3.setGeometry(QtCore.QRect(990, 0, 831, 1341))
        self.logfield_3.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.logfield_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logfield_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logfield_3.setLineWidth(7)
        self.logfield_3.setObjectName("logfield_3")
        self.tablet.addTab(self.fatsboottab, "")
        self.mtktab = QtWidgets.QWidget()
        self.mtktab.setObjectName("mtktab")
        self.logfield_4 = QtWidgets.QTextEdit(self.mtktab)
        self.logfield_4.setGeometry(QtCore.QRect(990, 0, 831, 1341))
        self.logfield_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.logfield_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logfield_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logfield_4.setLineWidth(7)
        self.logfield_4.setObjectName("logfield_4")
        self.tablet.addTab(self.mtktab, "")
        self.qualcomtab = QtWidgets.QWidget()
        self.qualcomtab.setObjectName("qualcomtab")
        self.logfield_5 = QtWidgets.QTextEdit(self.qualcomtab)
        self.logfield_5.setGeometry(QtCore.QRect(990, 0, 831, 1341))
        self.logfield_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.logfield_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logfield_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logfield_5.setLineWidth(7)
        self.logfield_5.setObjectName("logfield_5")
        self.tablet.addTab(self.qualcomtab, "")
        self.spdtab = QtWidgets.QWidget()
        self.spdtab.setObjectName("spdtab")
        self.logfield_6 = QtWidgets.QTextEdit(self.spdtab)
        self.logfield_6.setGeometry(QtCore.QRect(990, 0, 831, 1341))
        self.logfield_6.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.logfield_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.logfield_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.logfield_6.setLineWidth(7)
        self.logfield_6.setObjectName("logfield_6")
        self.tablet.addTab(self.spdtab, "")
        self.verticalLayout.addWidget(self.tablet)
        self.progressBar = QtWidgets.QProgressBar(main)
        self.progressBar.setEnabled(True)
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(main)
        self.tablet.setCurrentIndex(0)
        self.typeselection.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "tDroid_Tool"))
        self.groupBox.setTitle(_translate("main", "Repair"))
        self.label_2.setText(_translate("main", "AdbPort"))
        self.label_3.setText(_translate("main", "ComPort"))
        self.write_security.setText(_translate("main", "Write Security"))
        self.Fixbaseband.setText(_translate("main", "Fix Baseband"))
        self.reset_frp.setText(_translate("main", "Reset Frp"))
        self.Read_security.setText(_translate("main", "Read Security"))
        self.Read_info_cp.setText(_translate("main", "Read Modem"))
        self.MountNetwork.setText(_translate("main", "Mount Modem"))
        self.Write_Efs.setText(_translate("main", "Write Efs"))
        self.Read_Efs.setText(_translate("main", "Read EFS"))
        self.Read_info_adb.setText(_translate("main", "Read Adb"))
        self.label.setText(_translate("main", "Samsung Model"))
        self.groupBox_2.setTitle(_translate("main", "Flash"))
        self.readd.setText(_translate("main", "Read info"))
        self.flashsmsng.setText(_translate("main", "Flash"))
        self.checkBox.setText(_translate("main", "Pit"))
        self.checkBox_2.setText(_translate("main", "AP"))
        self.checkBox_3.setText(_translate("main", "CP"))
        self.checkBox_4.setText(_translate("main", "USERDATA"))
        self.checkBox_5.setText(_translate("main", "CSC"))
        self.checkBox_6.setText(_translate("main", "BL"))
        self.radioButton.setText(_translate("main", "No Reboot"))
        self.radioButton_2.setText(_translate("main", "ClearEfs"))
        self.checkBox_7.setText(_translate("main", "ALL"))
        self.rebootdload.setText(_translate("main", "Reboot D/load"))
        self.tablet.setTabText(self.tablet.indexOf(self.samsungtab), _translate("main", "Samsung "))
        self.tablet.setTabText(self.tablet.indexOf(self.adbtab), _translate("main", "Adb Tools"))
        self.tablet.setTabText(self.tablet.indexOf(self.fatsboottab), _translate("main", "Fastboot Tool"))
        self.tablet.setTabText(self.tablet.indexOf(self.mtktab), _translate("main", "Mediatek_Util"))
        self.tablet.setTabText(self.tablet.indexOf(self.qualcomtab), _translate("main", "Qualcom"))
        self.tablet.setTabText(self.tablet.indexOf(self.spdtab), _translate("main", "Spd/Unisoc"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QDialog()
    ui = Ui_main()
    ui.setupUi(main)
    main.show()
    sys.exit(app.exec_())
