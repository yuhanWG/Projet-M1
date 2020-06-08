from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import sys

#C=7
class endpage(QMainWindow):
	"""docstring for endpage"""
	#04/25
	switch_page=pyqtSignal()
	def __init__(self,img,sol,info,cpt,label,critere,path):
		super(endpage, self).__init__()
		print(cpt,"cpt")
		self.resize(750,400)

		#05/09
		self.critere=critere
		self.centralwidget=QWidget(self)
		self.widget=QWidget(self.centralwidget)
		self.widget1=QWidget(self.widget)
		self.widget2=QWidget(self.widget)
		self.widget1.setObjectName("widget1")
		self.widget2.setObjectName("widget2")
		self.centralwidget.setObjectName("central")

		self.grid=QGridLayout()

		self.vleft=QVBoxLayout()
		self.vright=QVBoxLayout()
		self.hbottom=QHBoxLayout()

		self.label=QLabel()
		self.label.setText("Vous avez repondu "+str(cpt)+" questions. On vous propose la voiture ci-dessous")

		###################
		##btn
		###################
		print("len",len(critere))
		self.btn=QToolButton()
		self.btnr=QPushButton("recommencer")
		self.btnq=QPushButton("quitter")

		self.img=img[sol]+".jpg"
		self.btn.setIconSize(QSize(200,200))
		#self.btn.setIcon(QIcon('./image/'+self.img))
		self.btn.setIcon(QIcon(path+'/image/'+self.img))

		
		self.infos=self.initlist()
		if(label[sol]<9):
		#print("hello "+"a0"+str(self.label[id]))
			self.infos[0].setText("a0"+str(label[sol]))
		else:
			self.infos[0].setText("a"+str(label[sol]))
		
		self.infos[1].setText("marque: "+img[sol])
		
		
		for i in range(len(self.critere)):
			if(info[i]>=0):
				self.infos[i+2].setText(self.critere[i]+": "+str(info[i]))
			else:
				self.infos[i+2].setText(self.critere[i]+": "+str(-info[i]))
		
		######################
		#layout
		######################
		for i in range(len(critere)+2):
			self.vleft.addWidget(self.infos[i])
		self.vright.addWidget(self.btn)
		self.vright.setAlignment(self.btn,Qt.AlignHCenter)
		self.vright.setAlignment(self.btn,Qt.AlignVCenter)
		
		self.hbottom.addWidget(self.btnr)
		self.hbottom.addStretch()
		self.hbottom.addWidget(self.btnq)
		self.vright.addLayout(self.hbottom)
		
		
		self.widget1.setLayout(self.vleft)
		self.widget2.setLayout(self.vright)

		self.grid.addWidget(self.widget1,1,1)
		self.grid.addWidget(self.widget2,1,2)
		self.widget.setLayout(self.grid)
		self.setCentralWidget(self.centralwidget)


		self.grid.addWidget(self.label,0,1,Qt.AlignHCenter)
		self.centralwidget.setStyleSheet("QWidget#central{border-image:url(1.jpg)}")

		self.widget.setStyleSheet(
			"QLabel{\n"
				"color:white;\n"
				"font: 16pt \"Impact\";\n"
			"}"
			)
		self.widget2.setStyleSheet(
			"QWidget#widget2{\n"
			"background-color:black\n"
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
			"}"
			)

		self.widget1.setStyleSheet(
			"QPushButton{\n"
				"font: 12pt \"Impact\";\n"
			"}\n"
			"QLabel{\n"
				"color:white;\n"
				"font: 16pt \"Impact\";\n"
			"}"
			)

		self.setWindowTitle("Solution optimale")
		####################
		#signal et slot
		####################
		self.btnr.clicked.connect(self.recommencerClicked)
		self.btnq.clicked.connect(self.quitClicked)

	def recommencerClicked(self):
		#self.close()
		self.switch_page.emit()

	def quitClicked(self):
		reply=QMessageBox.question(self,"Warning","Voulez-vous vraiment quitter?",QMessageBox.Yes,QMessageBox.No)
		if reply==QMessageBox.Yes:
			quit()


	def initlist(self):
		l=[]
		for i in range(len(self.critere)+2):
			l.append(QLabel())
		return l
	