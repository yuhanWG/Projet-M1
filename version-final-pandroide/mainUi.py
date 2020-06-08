from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from color import *
import numpy as np
import sys
from gurobipy import * 
from fonctions2 import *
import endPage2

from PyQt5 import QtCore, QtGui, QtWidgets

####Voici des donnees des voitures qu'on va utiliser
'''
N=14
C=7
doc="Donnees/tabNDS_5_14_Voiture"
#enregistre les marques des voitures
img=["tipo","alfa","sunny","mazda","colt","corolla","civic","astra","escort","R19","P30916","P309","galant","R21t"]
'''
#05/04
choice_list=["voiture","maison"]


class MainUi(QMainWindow):
	#04/25
	#params acceptables pour pyqtSignal: str、int、list、object、float、tuple、dict
	#endpage(img,self.sol,self.matrice[self.sol,:],self.cpt,self.label)
	switch_page=pyqtSignal(list,int,list,int,list,list,str)

	def __init__(self,index):
		super(MainUi,self).__init__()
		#05/04
		self.path=choice_list[index]
		nom_file=self.path+'/donnees'+'.txt'
		nom_critere=self.path+'/critere'+'.txt'
		nom_img=self.path+'/img'+'.txt'

		#05/09
		#self.resize(900,580)

		self.matrice=readFile(nom_file)
		self.critere=readCritere(nom_critere)
		self.img=readCritere(nom_img)
		self.img_path=self.path+'/image/'
		
		self.l,self.c=self.matrice.shape

		#06/01
		#self.C=len(self.critere)
		self.C=len(self.critere)+2
		self.N=len(self.img)


		self.resize(700,350)

		#nouvelle
		self.labelleft=self.initlist()
		self.labelright=self.initlist()

		###########################
		#PARTIE DE GUROBI
		###########################
		self.m=Model("s0")
		self.m.Params.OutputFlag=0
		self.var=[]
		expr=LinExpr()
		for i in range(self.c):
			self.var.append(self.m.addVar(vtype=GRB.CONTINUOUS, name="w%d"%(i+1)))
			expr+=self.var[i]
		#premiere constreinte : le somme des poids=1
		self.m.addConstr(expr==1)
		self.pmr=pmr(self.matrice)
		self.label=list(range(1,self.l+1))
		
		self.matrice_mr,self.worst_ad=max_regret(self.pmr,self.label)
		self.regret=np.min(self.matrice_mr)
		print(self.regret)

		#05/25
		clear_file("note.txt")
		write_file("note.txt",str(self.regret))


		self.sol=np.argmin(self.matrice_mr)
		self.pire_ad=int(self.worst_ad[self.sol])
		
		self.cpt=0

		self.centralwidget=QtWidgets.QWidget(self)
		#self.widget=QtWidgets.QWidget(self)
		#05/09
		self.widget1=QtWidgets.QWidget(self.centralwidget)
		self.widget2=QtWidgets.QWidget(self.centralwidget)


		self.setObjectName("MainWindow")
		self.widget1.setObjectName("widget1")
		self.widget2.setObjectName("widget2")
		self.centralwidget.setObjectName("central")
		
		#self.setStyleSheet('QMainWindow#MainWindow{border-image:url(bg.png)}')
		#self.setStyleSheet('QWidget#widget{background-color:rgb(255,0,0)}')
		#
		#self.setStyleSheet('QWidget#widget{border-image:url(bg.png)}')
		#self.centralwidget.setStyleSheet("QWidget#central{border-image:url(bg2.png)}")
		self.centralwidget.setStyleSheet("QWidget#central{border-image:url(1.jpg)}")
		#self.widget1.setStyleSheet("background-color:white;")
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
			"QWidget#widget1{\n"
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

		
		self.vleft=QVBoxLayout()
		self.vright=QVBoxLayout()
		if(self.sol!=self.pire_ad):
			self.btn1=QToolButton()
			self.btn2=QToolButton()
			self.btn1.setObjectName("left")
			self.btn2.setObjectName("right")
			self.img1=self.img[self.sol]+".jpg"
			self.img2=self.img[self.pire_ad]+".jpg"
			
			#self.btn1.setIcon(QIcon('./image/'+self.img1))
			#self.btn2.setIcon(QIcon('./image/'+self.img2))
			#05/04
			self.btn1.setIcon(QIcon(self.img_path+self.img1))
			self.btn2.setIcon(QIcon(self.img_path+self.img2))
			self.btn1.setIconSize(QSize(200,150))
			self.btn2.setIconSize(QSize(200,150))

			
			self.initInfos("sol",self.sol,self.matrice[self.sol],self.critere)
			self.initInfos("pire_ad",self.pire_ad,self.matrice[self.pire_ad],self.critere)

			####partie layout####
			
			self.hbox=QHBoxLayout()

			#05/08
			self.vleft.addWidget(self.btn1,Qt.AlignHCenter)
			
			self.vright.addWidget(self.btn2,Qt.AlignHCenter)

			for i in range(self.C):
				self.vleft.addWidget(self.labelleft[i])
				self.vright.addWidget(self.labelright[i])

			
			self.widget1.setLayout(self.vleft)
			self.widget2.setLayout(self.vright)


			#05/12
			self.label_regret=QLabel()
			self.label_regret.setText("Minimax Regret:"+str(self.regret))
			self.label_regret.setStyleSheet(
			"QLabel{\n"
				"color:white;\n"
				"font: 16pt \"Impact\";\n"
			"}")


			self.hbox.addWidget(self.label_regret)
			self.hbox.addWidget(self.widget1)
			self.hbox.addWidget(self.widget2)
			#05/09
			self.hbox.setContentsMargins(50, 50, 10, 50)
			#self.hbox.setSpacing(50)
			#self.hbox.addStretch(10)
			self.setWindowTitle("Quiz Time")
			#self.widget.setLayout(self.hbox)
			#self.setCentralWidget(self.widget)
			self.centralwidget.setLayout(self.hbox)
			self.setCentralWidget(self.centralwidget)



			####partie signal et slot####
			self.btn1.clicked.connect(lambda:self.optimiser("sol",self.sol,self.pire_ad))
			self.btn2.clicked.connect(lambda:self.optimiser("pire_ad",self.pire_ad,self.sol))
			QGuiApplication.processEvents()


		#self.setCentralWidget(self.widget)

	#05/09
	def layout(self):
		pass

	def optimiser(self,label,prefere,delete):
		expr1=expression(self.var,self.matrice[prefere,:])
		expr2=expression(self.var,self.matrice[delete,:])
		self.m.addConstr(expr1<=expr2)
		self.matrice,self.pmr=newPMR(self.m,self.matrice,self.pmr,delete,self.var)
		#print("shape",self.matrice.shape,self.pmr.shape)
		self.matrice_mr,self.worst_ad=max_regret(self.pmr,self.label)
		self.regret=np.min(self.matrice_mr)
		print(self.regret)
		write_file("note.txt",str(self.regret))

		self.label.pop(delete)
		self.img.pop(delete)
		self.sol=np.argmin(self.matrice_mr)
		self.pire_ad=int(self.worst_ad[self.sol])
		if(self.sol!=self.pire_ad):
			
			#mettre a jour les informations
			self.img1=self.img[self.sol]+".jpg"
			self.img2=self.img[self.pire_ad]+".jpg"

			#self.btn1.setIcon(QIcon('./image/'+self.img1))
			#self.btn2.setIcon(QIcon('./image/'+self.img2))
			self.btn1.setIcon(QIcon(self.img_path+self.img1))
			self.btn2.setIcon(QIcon(self.img_path+self.img2))

			self.initInfos("sol",self.sol,self.matrice[self.sol,:],self.critere)
			self.initInfos("pire_ad",self.pire_ad,self.matrice[self.pire_ad,:],self.critere)

			QGuiApplication.processEvents()
			self.widget1.update()
			self.widget2.update()
			self.label_regret.setText("Minimax Regret: "+str(self.regret))
			self.label_regret.update()
			self.centralwidget.update()
			#self.widget.repaint()

			self.cpt+=1
		else:
			self.cpt+=1
			print("quiz end: best car for you is: "+str(self.sol))
			write_file("note.txt","quiz end: best car for you is: "+str(self.sol))
			write_file("note.txt","nb questions repondus "+str(self.cpt))
			#print("size:",self.matrice.shape)
			'''
			print(self.pmr[self.sol,self.sol])
			self.hide()
			self.ui=endPage.endpage(img,self.sol,self.matrice[self.sol,:],self.cpt,self.label)
			self.ui.show()
			'''
			#04/25
			#print(type(self.matrice[self.sol,:]))
			matrice=list(self.matrice[self.sol,:])
			#print(type(matrice))
			self.switch_page.emit(self.img,self.sol,matrice,self.cpt,self.label,self.critere,self.path)

		
	'''
	def initInfos(self,label,id,infos,critere):
		print(critere)
		if(label=="sol"):
			if(self.label[id]<9):
				print("hello "+"a0"+str(self.label[id]))
				self.labelleft[0].setText("a0"+str(self.label[id]))
			else:
				self.labelleft[0].setText("a"+str(self.label[id]))
			self.labelleft[1].setText("marque: "+img[id])
			self.labelleft[2].setText("cout: "+str(infos[0])+"€")
			self.labelleft[3].setText("accel: "+str(infos[1]))
			self.labelleft[4].setText("reprise: "+str(infos[2]))
			self.labelleft[5].setText("freins: "+str(-infos[3]))
			self.labelleft[6].setText("tenue de route: "+str(-infos[4]))
		else:
			if(self.label[id]<9):
				print("hello "+"a0"+str(self.label[id]))
				self.labelright[0].setText("a0"+str(self.label[id]))
			else:
				self.labelright[0].setText("a"+str(self.label[id]))
			self.labelright[1].setText("marque: "+img[id])
			self.labelright[2].setText("cout: "+str(infos[0])+"€")
			self.labelright[3].setText("accel: "+str(infos[1]))
			self.labelright[4].setText("reprise: "+str(infos[2]))
			self.labelright[5].setText("freins: "+str(-infos[3]))
			self.labelright[6].setText("tenue de route: "+str(-infos[4]))
	'''
	#05/04
	def initInfos(self,label,id,infos,critere):
		if(label=="sol"):
			if(self.label[id]<9):
				#print("hello "+"a0"+str(self.label[id]))
				self.labelleft[0].setText("a0"+str(self.label[id]))
			else:
				self.labelleft[0].setText("a"+str(self.label[id]))
			
			self.labelleft[1].setText("marque: "+self.img[id])
			'''
			self.labelleft[2].setText("cout: "+str(infos[0])+"€")
			self.labelleft[3].setText("accel: "+str(infos[1]))
			self.labelleft[4].setText("reprise: "+str(infos[2]))
			self.labelleft[5].setText("freins: "+str(-infos[3]))
			self.labelleft[6].setText("tenue de route: "+str(-infos[4]))
			'''
			#06/01
			#for i in range(self.c)
			for i in range(self.c):
				if(infos[i]>=0):
					self.labelleft[i+2].setText(critere[i]+": "+str(infos[i]))
				else:
					self.labelleft[i+2].setText(critere[i]+": "+str(-infos[i]))
		else:
			if(self.label[id]<9):
				#print("hello "+"a0"+str(self.label[id]))
				self.labelright[0].setText("a0"+str(self.label[id]))
			else:
				self.labelright[0].setText("a"+str(self.label[id]))
			self.labelright[1].setText("marque: "+self.img[id])
			
			#06/01
			#for i in range(self.c)
			for i in range(self.c):
				if(infos[i]>=0):
					self.labelright[i+2].setText(critere[i]+": "+str(infos[i]))
				else:
					self.labelright[i+2].setText(critere[i]+": "+str(-infos[i]))



	
	#def retranslateUi(self):
        #_translate = QtCore.QCoreApplication.translate
        #self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.label.setText(_translate("MainWindow", "Votre solution optimale personnalisée, à partir d\'ici!"))
        #self.comboBox.setItemText(0, _translate("MainWindow", "VOITURE"))
        #self.pushButton.setText(_translate("MainWindow", "Commencer"))
        #self.pushButton_2.setText(_translate("MainWindow", "Annuler"))



	def initlist(self):
		l=[]
		for i in range(self.C):
			l.append(QLabel())
		#print(len(l))

		return l







