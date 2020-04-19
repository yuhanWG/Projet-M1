#interface2
img=["tipo","alfa","sunny","mazda","colt","corolla","civic","astra","escort","R19","P30916","P309","galant","R21t"]
id_voiture=[]
for i in range(N):
	if(i<9):
		id_voiture.append("a0"+str(i+1))
	else:
		id_voiture.append("a"+str(i+1))


class MainWindow(QMainWindow):
	def __init__(self,nom_fichier,parent=None):
		self.press_flag=False

		QMainWindow.__init__(self,parent)
		self.resize(500,300)
		#layout est modife de horizontal
		self.hbox=QHBoxLayout()
		self.widget=QWidget(self)

		###########################
		#DONNEE DE GUROBI
		###########################
		self.donnee=readFile(nom_fichier)
		self.l,self.c=self.donnee.shape
		#self.donnee,self.l,self.c=self.normaliser(donnee)
		self.pmr=pmr(self.donnee)
		self.label=list(range(1,self.l+1))
		self.marque=id_voiture
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