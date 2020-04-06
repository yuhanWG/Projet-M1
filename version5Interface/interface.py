from fonctions2 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from color import *
import numpy as np
import sys
from gurobipy import * 

RGB=255
N=2
doc="Donnees/tabNDS_50_3.txt"
mot_color="background-color:rgb"

class MainWindow(QMainWindow):

	myClicked=pyqtSignal(int)

	def __init__(self,nom_fichier,parent=None):
		self.press_flag=False

		QMainWindow.__init__(self,parent)
		self.resize(500,300)
		self.vbox=QVBoxLayout()
		self.widget=QWidget(self)

		###########################
		#DONNEE DE GUROBI
		###########################
		donnee=readFile(nom_fichier)
		self.donnee,self.l,self.c=self.normaliser(donnee)
		self.pmr=pmr(self.donnee)
		self.label=list(range(1,self.l+1))
		#matrice_mr, worst_ad deux list de taille n*1
		self.matrice_mr,self.worst_ad=max_regret(self.pmr,self.label)
		#self sol, self pire_ad deux index des solutions les plus interessants
		self.sol=np.argmin(self.matrice_mr)
		self.pire_ad=int(self.worst_ad[self.sol])

		self.m=Model("s0")
		self.m.Params.OutputFlag=0
		self.var=[]
		expr=LinExpr()
		for i in range(self.c):
			self.var.append(self.m.addVar(vtype=GRB.CONTINUOUS, name="w%d"%(i+1)))
			expr+=self.var[i]
		#premiere constreinte : le somme des poids=1
		self.m.addConstr(expr==1)

		#butonset enregistre un tuple qui contient (QPushButton,index)
		self.butonset=[]
		self.butonset.append((QPushButton("this"),self.sol))
		self.butonset.append((QPushButton("that"),self.pire_ad))
		#colorset va enregistrer les couleurs correspond a comparer
		self.colorset=[]
		self.cpt=0
		
		
		###########################
		#PARTIE LAYOUT
		###########################

		for i in range(N):
			index=self.butonset[i][1]
			d=self.donnee[index,:]
			c=self.getColor(d)
			print(d)
			self.butonset[i][0].setStyleSheet(mot_color+c)
			#self.butonset[i][0].clicked.connect(lambda:self.optimiser(index))
			self.vbox.addWidget(self.butonset[i][0])
		self.butonset[0][0].clicked.connect(lambda:self.optimiser(self.butonset[0][1]))
		self.butonset[1][0].clicked.connect(lambda:self.optimiser(self.butonset[1][1]))
			#print(self.butonset[i][1])
		self.widget.setLayout(self.vbox)
		self.setCentralWidget(self.widget)
		self.textEdit=QTextEdit(self)
		self.vbox.addWidget(self.textEdit)

	
	#normaliser les chiffres pour qu'ils soient dans intervalle [0,255]
	def normaliser(self,data):
		
		#l nb alternatives,c nb de critreres
		l,c=data.shape
		new_data=[]
		datamax=np.amax(data)
		i=RGB/datamax
		for a in data:
			for b in a:
				new_data.append(b*i)
		new_data=np.array(new_data)
		new_data=np.reshape(new_data,(l,c))
		
		return new_data,l,c


	#cette fonction sert a mettre des donnees a formes d'une couleur
	def getColor(self,data):
		r,g,b=data/(255/np.max(data))
		return "("+str(r)+","+str(g)+","+str(b)+")"

	def optimiser(self,index):
		a=[]
		for b in self.butonset:
			a.append(b[1])

		if(a[0]==a[1]):
			self.log_action("Vous avez repondu"+str(self.cpt)+" questions")
			self.log_action("On a trouve la solution optimale"+str(index+1))

		else:
			if(a[0]==index):
				index2=a[1]
			else:
				index2=a[0]
			self.log_action("Vous preferez la solutioin: "+str(self.label[index])+" que la solution "+str(self.label[index2]))
			self.cpt+=1
			#index: ce qui est prefere
			#index2: ce qui n'est pas prefere
			expr1=expression(self.var,self.donnee[index,:])
			expr2=expression(self.var,self.donnee[index2,:])
			self.label.pop(index2)
			self.m.addConstr(expr2<=expr1)
			self.donnee,self.pmr=newPMR(self.m,self.donnee,self.pmr,index2,self.var)
			
			self.matrice_mr,self.worst_ad=max_regret(self.pmr,self.label)
			#self sol, self pire_ad deux index des solutions les plus interessants
			self.sol=np.argmin(self.matrice_mr)
			self.pire_ad=int(self.worst_ad[self.sol])

			for i in range(N):
				index=self.butonset[i][1]
				d=self.donnee[index,:]
				c=self.getColor(d)
				print(d)
				self.butonset[i][0].setStyleSheet(mot_color+c)



	#fonction permet afficher les donnees dans textEdit
	def log_action(self,str):

		content=self.textEdit.toPlainText()
		self.textEdit.setPlainText(content+"\n"+str)


if __name__=='__main__':
	app=QApplication(sys.argv)
	w=MainWindow(doc)
	#print(w.getColor([255,255,255]))
	w.show()
	print(w.var)
	sys.exit(app.exec_())
	
