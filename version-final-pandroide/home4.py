# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home4.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from color import *
import numpy as np
import sys
#from PyQt5 import QtCore, QtGui, QtWidgets

choice_list=["VOITURE","MAISON"]
class Ui_MainWindow(QMainWindow):
    switch_page=pyqtSignal(int)
    #def setupUi(self, MainWindow):
    def __init__(self,parent=None):
        super(Ui_MainWindow,self).__init__(parent)
        self.currentIndex=0
        #MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(922, 589)
        self.setObjectName("MainWindow")
        self.resize(900,580)


#######PARTIE LAYOUT###############
        #self.mainwidget=QtWidgets.QWidget(MainWindow)
        self.mainwidget=QtWidgets.QWidget(self)
        self.mainwidget.setGeometry(QtCore.QRect(0, 0, 931, 591))

        '''self.mainwidget.setStyleSheet("QWidget#mainwidget{\n"
"border-image:url(bg.png)\n"
"}\n"
"QPushButton{\n"
"font: 12pt \"Impact\";\n"
"}\n"
"QComboBox{\n"
"font: 12pt \"Impact\";\n"
"}\n"
"QLabel{\n"
"color:white;\n"
"font: 16pt \"Impact\";\n"
"}")'''
        self.mainwidget.setStyleSheet("QWidget#mainwidget{\n"
"border-image:url(1.jpg)\n"
"}\n"
"QPushButton{\n"
"font: 12pt \"Impact\";\n"
"}\n"
"QComboBox{\n"
"font: 12pt \"Impact\";\n"
"}\n"
"QLabel{\n"
"color:white;\n"
"font: 16pt \"Impact\";\n"
"}")
        self.mainwidget.setObjectName("mainwidget")
        self.widget = QtWidgets.QWidget(self.mainwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 921, 591))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(100, 200, 250, 200)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setObjectName("comboBox")
        #self.comboBox.addItem("")
        self.comboBox.addItems(choice_list)
        self.verticalLayout.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumWidth(200)
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMinimumWidth(200)
        self.verticalLayout.addWidget(self.pushButton_2)

        self.verticalLayout.setAlignment(Qt.AlignHCenter)

        self.horizontalLayout.addLayout(self.verticalLayout)
        #MainWindow.setCentralWidget(self.centralwidget)
        self.mainwidget.setLayout(self.horizontalLayout)
        #MainWindow.setCentralWidget(self.mainwidget)
        self.setCentralWidget(self.mainwidget)

        #self.retranslateUi(MainWindow)
        self.retranslateUi()
       # QtCore.QMetaObject.connectSlotsByName(MainWindow)
       #QtCore.QMetaObject.connectSlotsByName(self)


    ######SIGNAL ET SLOT
        self.pushButton_2.clicked.connect(self.quit)
        self.pushButton.clicked.connect(self.switch)
        self.comboBox.currentIndexChanged.connect(lambda:self.index(self.comboBox.currentIndex()))


    def index(self,currentIndex):
        self.currentIndex=currentIndex
        print(self.currentIndex)

    def switch(self):
        #pass
        self.switch_page.emit(self.currentIndex)


    def quit(self):
        reply=QMessageBox.question(self,"Warning","Voulez-vous vraiment quitter?",QMessageBox.Yes,QMessageBox.No)
        if reply==QMessageBox.Yes:
            quit()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        #modifier les titles
        self.setWindowTitle(_translate("MainWindow", "Interface web systeme de recommandation"))
        self.label.setText(_translate("MainWindow", "Votre solution optimale personnalisée, à partir d\'ici!"))
        #self.comboBox.setItemText(0, _translate("MainWindow", "VOITURE"))
        self.pushButton.setText(_translate("MainWindow", "Commencer"))
        self.pushButton_2.setText(_translate("MainWindow", "Annuler"))

    '''
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Votre solution optimale personnalisée, à partir d\'ici!"))
        #self.comboBox.setItemText(0, _translate("MainWindow", "VOITURE"))
        self.pushButton.setText(_translate("MainWindow", "Commencer"))
        self.pushButton_2.setText(_translate("MainWindow", "Annuler"))
        '''
#import source_rc

'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
'''
