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

#04/25
#05/04
#maintenant ce signal doit comprendre index de donnees l'user a choisit
	switch_page=pyqtSignal(int)

	def __init__(self,parent=None):
		super(Home,self).__init__(parent)
		#05/04
		self.currentIndex=0
		self.choice_list=["voiture","maison"]

		self.resize(300,400)
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


		####partie menubar#####
		self.menu=QComboBox(self)
		self.menu.addItems(self.choice_list)
		
		#####partie layout#######
		#self.label.setAlignment(Qt.AlignVCenter)
		self.label.setAlignment(Qt.AlignHCenter)
		self.vbox.addWidget(self.label)

		#05/04
		self.vbox.addWidget(self.menu)

		self.hbox.addStretch(1)
		self.hbox.addWidget(self.btn)
		self.hbox.addWidget(self.btnquit)
		self.hbox.addStretch(1)
		self.vbox.addLayout(self.hbox)
		self.widget.setLayout(self.vbox)
		self.setCentralWidget(self.widget)


		####partie signal-slot#####
		self.btnquit.clicked.connect(self.quitClicked)
		self.btn.clicked.connect(self.switch)
		self.menu.currentIndexChanged.connect(lambda:self.index(self.menu.currentIndex()))


		


	#modification 05/04
	def index(self,currentIndex):
		self.currentIndex=currentIndex
		#print(type(self.currentIndex)) type int


	def quitClicked(self):
		reply=QMessageBox.question(self,"Warning","Voulez-vous vraiment quitter?",QMessageBox.Yes,QMessageBox.No)
		if reply==QMessageBox.Yes:
			quit()

	def switch(self):
		self.switch_page.emit(self.currentIndex)



	'''
	#modificatioin 04/25
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
'''