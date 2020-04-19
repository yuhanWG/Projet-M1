#from fonctions2 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from color import *
import numpy as np
import sys
#from gurobipy import * 
import mainUi

class Home(QMainWindow):

	def __init__(self,parent=None):
		super(Home,self).__init__(parent)
		self.resize(650,480)
		self.setWindowTitle("choix de voiture")
		#set the color of background
		self.setStyleSheet('QMainWindow{background-color:rgb(145,152,159)}')
		self.label=QLabel()
		self.label.setText("En vous posant une suite des questions, on vous recommande une voiture perfaite!")
		self.btn=QPushButton("commencer")
		self.btnquit=QPushButton("annuler")
		self.widget=QWidget()
		self.vbox=QVBoxLayout()
		self.hbox=QHBoxLayout()
		
		#####partie layout#######
		self.vbox.addWidget(self.label)
		self.hbox.addWidget(self.btn)
		self.hbox.addWidget(self.btnquit)
		self.vbox.addLayout(self.hbox)
		self.widget.setLayout(self.vbox)
		self.setCentralWidget(self.widget)


		####partie signal-slot#####
		self.btnquit.clicked.connect(self.quitClicked)
		self.btn.clicked.connect(self.startClicked)

	def quitClicked(self):
		reply=QMessageBox.question(self,"Warning","Voulez-vous vraiment quitter?",QMessageBox.Yes,QMessageBox.No)
		if reply==QMessageBox.Yes:
			quit()


	def startClicked(self):
		#ici je cree une deuxieme fenetre et fait la premiere invisible
		print("test commence")
		self.hide()
		self.ui=mainUi.MainUi()
		self.ui.show()

if __name__=='__main__':
	app=QApplication(sys.argv)
	home=Home()
	home.show()
	sys.exit(app.exec_())