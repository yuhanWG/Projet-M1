#import MiniMaxRegret as mmr
import fonctions as f
import numpy as np


res=[]
doc="Donnees/tabNDS_50_"

for i in range(2,9):
	nom_file=doc+str(i)+'.txt'
	matrice=f.readFile(nom_file)
	print(type(matrice))
	nbSol,nbCrit=matrice.shape
	poids=f.poid_aleatoire(nbCrit)
	m=f.MiniMaxRegret(matrice,poids)
	sol_opt,nb_qu=m.MMR()
	if(sol_opt==f.calcul_opt(matrice,poids)):
		opt="OUI"
	else:
		opt="NON"
	#print(type(poids))
	l=[nbCrit,nbSol,nb_qu,opt,sol_opt]+poids
	#res.append(nbCrit,nbSol,nb_qu,opt,sol_opt)
	res.append(l)
	#res=res+(poids)

#dt=np.dtype("int,int,int,str,int")
l=np.asarray(res)
print(l)

fname="testresult.txt"
np.savetxt(fname,l,fmt='%s')