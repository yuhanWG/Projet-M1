from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from color import *
import numpy as np
import sys
from gurobipy import * 
import sys
from fonctions2 import *

####Voici des donnees des voitures qu'on va utiliser
N=14
doc="Donnees/tabNDS_5_14_Voiture"
#enregistre les marques des voitures
img=["tipo","alfa","sunny","mazda","colt","corolla","civic","astra","escort","R19","P30916","P309","galant","R21t"]



class MainUi(QMainWindow):
	def __init__(self,parent=None):
		super(MainUi,self).__init__(parent)
		self.resize(650,480)
		self.setStyleSheet('QMainWindow{background-color:rgb(244,167,185)}')

		nom_file=doc+'.txt'
		self.matrice=readFile(nom_file)
		self.l,self.c=self.matrice.shape

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
		#print(self.pmr.shape,self.label)
		self.matrice_mr,self.worst_ad=max_regret(self.pmr,self.label)
		self.sol=np.argmin(self.matrice_mr)
		self.pire_ad=int(self.worst_ad[self.sol])
		print(self.label[self.sol],self.label[self.pire_ad])
		self.cpt=0

		###########################
		#PARTIE qui pose probleme
		#j'ai connecte les deux boutons a fonction optimiser(), ce qui devrait modifier 
		#le contenu dans les deux layout self.vleft et self.vright 
		###########################
		self.widget=QWidget()
		#self.infol=self.getInfos(self.sol,self.matrice[self.sol])
		#self.infor=self.getInfos(self.pire_ad,self.matrice[self.pire_ad])
		if(self.sol!=self.pire_ad):
			self.btn1=QToolButton()
			self.btn2=QToolButton()
			self.img1=img[self.sol]+".jpg"
			self.img2=img[self.pire_ad]+".jpg"
			#print(img1,img2)
			self.btn1.setIcon(QIcon('./image/'+self.img1))
			self.btn2.setIcon(QIcon('./image/'+self.img2))
			self.btn1.setIconSize(QSize(200,200))
			self.btn2.setIconSize(QSize(200,200))

			self.infol=self.getInfos(self.sol,self.matrice[self.sol])
			self.infor=self.getInfos(self.pire_ad,self.matrice[self.pire_ad])

			####partie layout####
			
			self.hbox=QHBoxLayout()
			self.vleft=QVBoxLayout()
			self.vright=QVBoxLayout()

			self.vleft.addWidget(self.btn1)
			self.vleft.addLayout(self.infol)

			self.vright.addWidget(self.btn2)
			self.vright.addLayout(self.infor)

			self.hbox.addLayout(self.vleft)
			self.hbox.addLayout(self.vright)
			self.widget.setLayout(self.hbox)
			#self.setCentralWidget(self.widget)
			####partie signal et slot####
			self.btn1.clicked.connect(lambda :self.optimiser(self.sol,self.pire_ad))
			self.btn2.clicked.connect(lambda:self.optimiser(self.pire_ad,self.sol))
			QGuiApplication.processEvents()

		else:
			l1=QLabel()
			l1.setText("Apres avoir repondu "+str(self.cpt)+" questions, on a trouve votre voiture!")
			self.btn=QToolButton()
			img1=img[self.sol]+".jpg"
			self.btn1.setIcon(QIcon('./image/'+img1))
			self.btn1.setIconSize(QSize(200,200))
			self.info=self.getInfos(self.sol,self.matrice[self.sol])
			self.vbox=QVBoxLayout()
			self.vbox.addWidget(l1)
			self.vbox.addLayout(self.info)
			self.widget.setLayout(self.vbox)

		self.setCentralWidget(self.widget)


	def optimiser(self,prefere,delete):
	#def optimiser(self,params):
		#print(params)
		#prefere=params[0]
		#delete=params[1]
		print(prefere,delete)
		print("prefere "+str(self.label[prefere])+" que "+str(self.label[delete]))
		expr1=expression(self.var,self.matrice[prefere,:])
		expr2=expression(self.var,self.matrice[delete,:])
		self.m.addConstr(expr1<=expr2)
		self.matrice,self.pmr=newPMR(self.m,self.matrice,self.pmr,delete,self.var)
		#print("shape",self.matrice.shape,self.pmr.shape)
		self.matrice_mr,self.worst_ad=max_regret(self.pmr,self.label)

		self.label.pop(delete)
		img.pop(delete)
		self.sol=np.argmin(self.matrice_mr)
		#print(self.sol)
		self.pire_ad=int(self.worst_ad[self.sol])
		print("hello",self.label[self.sol],self.label[self.pire_ad])

		#mettre a jour les informations
		self.img1=img[self.sol]+".jpg"
		self.img2=img[self.pire_ad]+".jpg"

		self.btn1.setIcon(QIcon('./image/'+self.img1))
		self.btn2.setIcon(QIcon('./image/'+self.img2))
		#je pense que c'est cette partie qui ne fonctionne pas
		self.infol=self.getInfos(self.sol,self.matrice[self.sol,:])
		self.infor=self.getInfos(self.pire_ad,self.matrice[self.pire_ad,:])

		#print(self.infor)
		QGuiApplication.processEvents()
		self.widget.update()

		self.cpt+=1
		

	def getInfos(self,id,infos):
	#en utilisant les informations donnees, getInfos va retourner un QVBoxlayout
		coordonne=QVBoxLayout()
		l1=QLabel()
		l2=QLabel()
		cout=QLabel()
		accel=QLabel()
		reprise=QLabel()
		freins=QLabel()
		tdr=QLabel()
		print(infos)
		if(self.label[id]<9):
			print("hello "+"a0"+str(self.label[id]))
			l1.setText("a0"+str(self.label[id]))
		else:
			print(infos)
			print("hello "+"a"+str(self.label[id]))
			l1.setText("a"+str(self.label[id]))
		l2.setText("marque: "+img[id])
		cout.setText("cout: "+str(infos[0])+"€")
		accel.setText("accel: "+str(infos[1]))
		reprise.setText("reprise: "+str(infos[2]))
		freins.setText("freins: "+str(-infos[3]))
		tdr.setText("tenue de route: "+str(-infos[4]))
		
		coordonne.addWidget(l1)
		coordonne.addWidget(l2)
		coordonne.addWidget(cout)
		coordonne.addWidget(accel)
		coordonne.addWidget(reprise)
		coordonne.addWidget(freins)
		coordonne.addWidget(tdr)

		return coordonne








