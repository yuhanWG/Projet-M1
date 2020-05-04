from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from color import *
import numpy as np
import sys
from gurobipy import * 
from fonctions2 import *
import endPage

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

		self.matrice=readFile(nom_file)
		self.critere=readCritere(nom_critere)
		self.img=readCritere(nom_img)
		self.img_path=self.path+'/image/'
		
		self.l,self.c=self.matrice.shape
		#self.C=self.c+2
		self.C=len(self.critere)+1
		self.N=len(self.img)


		self.resize(650,480)
		self.setStyleSheet('QMainWindow{background-color:rgb(244,167,185)}')

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
		self.sol=np.argmin(self.matrice_mr)
		self.pire_ad=int(self.worst_ad[self.sol])
		
		self.cpt=0

		self.widget=QWidget()
		
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
			self.btn1.setIconSize(QSize(200,200))
			self.btn2.setIconSize(QSize(200,200))

			
			self.initInfos("sol",self.sol,self.matrice[self.sol],self.critere)
			self.initInfos("pire_ad",self.pire_ad,self.matrice[self.pire_ad],self.critere)

			####partie layout####
			
			self.hbox=QHBoxLayout()

			self.vleft.addWidget(self.btn1)
			
			self.vright.addWidget(self.btn2)

			for i in range(self.C):
				self.vleft.addWidget(self.labelleft[i])
				self.vright.addWidget(self.labelright[i])

			self.hbox.addLayout(self.vleft)
			self.hbox.addLayout(self.vright)


			self.widget.setLayout(self.hbox)
			self.setCentralWidget(self.widget)
			####partie signal et slot####
			self.btn1.clicked.connect(lambda:self.optimiser("sol",self.sol,self.pire_ad))
			self.btn2.clicked.connect(lambda:self.optimiser("pire_ad",self.pire_ad,self.sol))
			QGuiApplication.processEvents()


		self.setCentralWidget(self.widget)

	def optimiser(self,label,prefere,delete):
		print(prefere,delete)
		print("prefere "+str(self.label[prefere])+" que "+str(self.label[delete]))
		expr1=expression(self.var,self.matrice[prefere,:])
		expr2=expression(self.var,self.matrice[delete,:])
		self.m.addConstr(expr1<=expr2)
		self.matrice,self.pmr=newPMR(self.m,self.matrice,self.pmr,delete,self.var)
		#print("shape",self.matrice.shape,self.pmr.shape)
		self.matrice_mr,self.worst_ad=max_regret(self.pmr,self.label)

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
			self.widget.update()
			self.widget.repaint()

			self.cpt+=1
		else:
			self.cpt+=1
			print("quiz end: best car for you is: "+str(self.sol))
			print("size:",self.matrice.shape)
			'''
			print(self.pmr[self.sol,self.sol])
			self.hide()
			self.ui=endPage.endpage(img,self.sol,self.matrice[self.sol,:],self.cpt,self.label)
			self.ui.show()
			'''
			#04/25
			print(type(self.matrice[self.sol,:]))
			matrice=list(self.matrice[self.sol,:])
			print(type(matrice))
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
				print("hello "+"a0"+str(self.label[id]))
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
			'''
			self.labelright[2].setText("cout: "+str(infos[0])+"€")
			self.labelright[3].setText("accel: "+str(infos[1]))
			self.labelright[4].setText("reprise: "+str(infos[2]))
			self.labelright[5].setText("freins: "+str(-infos[3]))
			self.labelright[6].setText("tenue de route: "+str(-infos[4]))
			'''
			for i in range(self.c):
				if(infos[i]>=0):
					self.labelright[i+2].setText(critere[i]+": "+str(infos[i]))
				else:
					self.labelright[i+2].setText(critere[i]+": "+str(-infos[i]))



	def initlist(self):
		l=[]
		for i in range(self.C):
			l.append(QLabel())
		#print(len(l))

		return l







