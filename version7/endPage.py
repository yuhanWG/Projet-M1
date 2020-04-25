from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
import sys

C=7
class endpage(QMainWindow):
	"""docstring for endpage"""
	#04/25
	switch_page=pyqtSignal()
	def __init__(self,img,sol,info,cpt,label):
		super(endpage, self).__init__()
		self.resize(650,480)
		###################
		##layout
		###################
		self.widget=QWidget()
		self.vleft=QVBoxLayout()
		self.vright=QVBoxLayout()
		self.hbottom=QHBoxLayout()
		self.htout=QHBoxLayout()
		self.htout.setStretch(2,1)
		

		###################
		##btn
		###################
		self.btn=QToolButton()
		self.btnr=QPushButton("recommencer")
		self.btnq=QPushButton("quitter")

		self.img=img[sol]+".jpg"
		self.btn.setIconSize(QSize(200,200))
		self.btn.setIcon(QIcon('./image/'+self.img))

		self.label=QLabel()
		self.label.setText("Vous avez repondu "+str(cpt)+" questions. On vous propose la voiture ci-dessous")

		self.infos=self.initlist()
		if(label[sol]<9):
		#print("hello "+"a0"+str(self.label[id]))
			self.infos[0].setText("a0"+str(label[sol]))
		else:
			self.infos[0].setText("a"+str(label[sol]))
		
		self.infos[1].setText("marque: "+img[sol])
		self.infos[2].setText("cout: "+str(info[0])+"€")
		self.infos[3].setText("accel: "+str(info[1]))
		self.infos[4].setText("reprise: "+str(info[2]))
		self.infos[5].setText("freins: "+str(-info[3]))
		self.infos[6].setText("tenue de route: "+str(-info[4]))
		
		

		######################
		#layout
		######################
		self.vleft.addWidget(self.label)
		for i in range(C):
			self.vleft.addWidget(self.infos[i])
		self.vright.addWidget(self.btn)
		self.vright.setAlignment(self.btn,Qt.AlignHCenter)
		self.vright.setAlignment(self.btn,Qt.AlignVCenter)
		
		self.hbottom.addWidget(self.btnr)
		self.hbottom.addStretch()
		self.hbottom.addWidget(self.btnq)

		self.vright.addLayout(self.hbottom)
		self.htout.addLayout(self.vleft)
		self.htout.addLayout(self.vright)

		self.widget.setLayout(self.htout)
		self.setCentralWidget(self.widget)

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
		for i in range(C):
			l.append(QLabel())
		print(len(l))

		return l
	