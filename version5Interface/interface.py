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
doc="Donnees/tabNDS_5_3.txt"
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
		self.index=[]
		self.index.append(self.sol)
		self.index.append(self.pire_ad)

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
		#self.butonset.append((QPushButton("this"),self.sol))
		self.butonset.append(QPushButton("this"))
		self.butonset.append(QPushButton("that"))
		#self.butonset.append((QPushButton("that"),self.pire_ad))
		#colorset va enregistrer les couleurs correspond a comparer
		self.colorset=[]
		self.cpt=0
		
		
		###########################
		#PARTIE LAYOUT
		###########################

		for i in range(N):
			index=self.index[i]
			d=self.donnee[index,:]
			c=self.getColor(d)
			self.butonset[i].setStyleSheet(mot_color+c)
			self.vbox.addWidget(self.butonset[i])

		self.butonset[0].clicked.connect(lambda:self.optimiser(self.index[0]))
		self.butonset[1].clicked.connect(lambda:self.optimiser(self.index[1]))
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
		#if(datamax>255):
		i=RGB/datamax
		for a in data:
			for b in a:
				new_data.append(b*i)
		new_data=np.array(new_data)
		new_data=np.reshape(new_data,(l,c))
		#else:
		#	new_data=data
		
		return new_data,l,c


	#cette fonction sert a mettre des donnees a formes d'une couleur
	def getColor(self,data):
		r,g,b=data/(255/np.max(data))
		return "("+str(r)+","+str(g)+","+str(b)+")"

	#def changeColor():


	def optimiser(self,index):
		delete=-10
		if(self.index[0]==self.index[1]):
			self.log_action("Vous avez repondu "+str(self.cpt)+" questions")
			self.log_action("On a trouve la solution optimale "+str(self.label[self.index[0]]))

		else:
			if(self.index[0]==index):
				index2=self.index[1]
			else:
				index2=self.index[0]
			self.log_action("Vous preferez la solutioin: "+str(self.label[index])+" que la solution "+str(self.label[index2]))
			
			#index: ce qui est prefere
			#index2: ce qui n'est pas prefere
			print(self.donnee)
			print("index1",index,"index2",index2)
			'''
			if self.cpt==0:
				#print(self.donnee[index,:],self.donnee[index2,:])
				expr1=expression(self.var,self.donnee[index,:])
				expr2=expression(self.var,self.donnee[index2,:])
				delete=index2
			else:
				i1,i2=self.where(index+1,index2+1)
				print(i1,i2)
				print(self.donnee[i1+1,:],self.donnee[i2+1,:])
				expr1=expression(self.var,self.donnee[i1,:])
				expr2=expression(self.var,self.donnee[i2,:])
				index2=i2
			'''
			print(self.donnee[index,:],self.donnee[index2])
			expr1=expression(self.var,self.donnee[index,:])
			expr2=expression(self.var,self.donnee[index2,:])

			self.m.addConstr(expr1<=expr2)
			self.donnee,self.pmr=newPMR(self.m,self.donnee,self.pmr,index2,self.var)
			#print(self.donnee)
			self.label.pop(index2)
			print("label is",self.label)
			
			self.matrice_mr,self.worst_ad=max_regret(self.pmr,self.label)
			
			print("pmr is",self.pmr)
			print("matrice_mr is",self.matrice_mr)
			

			#self sol, self pire_ad deux index des solutions les plus interessants
			self.sol=np.argmin(self.matrice_mr)
			print("sol",self.sol)
			print("worst ad is",self.worst_ad)
			self.pire_ad=int(self.worst_ad[self.sol])
			self.index=[]
			self.index.append(self.sol)
			self.index.append(self.pire_ad)
			print("index now is",self.index)

			for i in range(N):
				print(self.index[i])
				index=self.index[i]
				d=self.donnee[index,:]
				c=self.getColor(d)
				#print(d)
				self.butonset[i].setStyleSheet(mot_color+c)
			self.cpt+=1


	#fonction permet afficher les donnees dans textEdit
	def log_action(self,str):

		content=self.textEdit.toPlainText()
		self.textEdit.setPlainText(content+"\n"+str)

	def where(self,ind1,ind2):
		a=0
		b=0
		for i in range(len(self.label)):
			if(ind1==self.label[i]):
				a=i
			if(ind2==self.label[i]):
				b=i
		return a,b

if __name__=='__main__':
	app=QApplication(sys.argv)
	w=MainWindow(doc)
	#print(w.getColor([255,255,255]))
	w.show()
	#print(w.var)
	print(w.index)
	sys.exit(app.exec_())
	
