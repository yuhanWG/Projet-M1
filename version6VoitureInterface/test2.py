#import fonctions as f
from fonctions2 import *

N=14
doc="Donnees/tabNDS_5_14_Voiture"
id_voiture=[]
#enregistre les marques des voitures
img=["tipo","alfa","sunny","mazda","colt","corolla","civic","astra","escort","R19","P30916","P309","galant","R21t"]

for i in range(N):
	if(i<9):
		id_voiture.append("a0"+str(i+1))
	else:
		id_voiture.append("a"+str(i+1))

nom_file=doc+'.txt'
matrice=readFile(nom_file)
#print(len(img))
#print(matrice)
#print(id_voiture) affichage a01-a14