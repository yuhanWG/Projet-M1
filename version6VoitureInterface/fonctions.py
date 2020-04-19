import numpy as np
from gurobipy import *
import random

#pour etre capable de traiter les chiffres avec des decimales, int() est remplace par float()
def readFile(nom_file):
	data=open(nom_file,'r')
	next(data)
	l = [[float(num) for num in line.split()] for line in data]

	return np.asarray(l)
	data.close()

def calcul_opt(matrice,poids):
    result=[]
    for i in range(matrice.shape[0]):
        result.append(np.sum(matrice[i,:]*poids))
    return(np.argmin(result)+1)


#generer les poids aleatoirement
def poid_aleatoire(nb):
    plist=[]
    plist=[random.randint(0,100) for _ in range(nb)]
    total=sum(plist)
    plist=[p/total for p in plist]
    return plist


#calculer la matrice ou une indice(x,y) presente le regret en choissisant x au lieu de y 
#taille n*n
def pmr(matrice):
    nb_alt,nb_citere=matrice.shape
    matrice_pmr=np.zeros((nb_alt,nb_alt))
    for i in range(nb_alt):
        for j in range(nb_alt):
            if i!=j:               
                cpt=np.ndarray.max(np.array(matrice[i,:]-matrice[j,:]))
                matrice_pmr[i,j]=cpt
    return matrice_pmr

#determiner pour chaque alternative son pire adversaire
#max_regret et worst_ad: taille n*1
def max_regret(pmrM,l):
    nb_alt=pmrM.shape[0]
    max_regret=np.zeros(nb_alt)
    worst_ad=np.zeros(nb_alt)
    for i in range(nb_alt):
        max_regret[i]=np.ndarray.max(pmrM[i,:])
        worst_ad[i]=int(np.argmax(pmrM[i,:]))
    return max_regret,worst_ad


#etant donne les poids pour chaque critere, comparer les deux solutions, retourner si sol1 est plus preferable que sol2
def Query(poid,sol1,sol2):
    #print(poid*sol1,poid*sol2)
    print(np.sum(poid*sol1),np.sum(poid*sol2))
    if(np.sum(poid*sol1)>np.sum(poid*sol2)):  
        return False
    else:
        return True
    

def expression(q,ligne):
    expr=LinExpr()
    for i in range(len(q)):
        expr+=q[i]*ligne[i]
    return expr

#en ajoutant des nouvelles contreintes, re-calculer la matricePMR
def newPMR(m,matrice,pmr,delete,q):
    matrice=np.delete(matrice,delete,0)
    pmr=np.delete(pmr,delete,0)
    pmr=np.delete(pmr,delete,1)
    #print(pmr)
    a,b=pmr.shape
    for i in range(a):
        for j in range(b):
            if(i!=j):
                expr1=expression(q,matrice[i,:])
                expr2=expression(q,matrice[j,:])
                m.setObjective(expr1-expr2,GRB.MAXIMIZE)
                m.optimize()
                pmr[i,j]=m.objVal
    return matrice,pmr


class MiniMaxRegret(object):
    def __init__(self,matrice,list_poids):
        """
        matrice:matrice de alternatives et leurs evaluations par criteres
        resultat:enregistrer les labels des alternatives
        """
        self.matrice=matrice
        self.nb_alt,self.nb_c=matrice.shape
        self.label=list(range(1,self.nb_alt+1))
        self.poids=list_poids
        self.nb_question=0
        
    
    def MMR(self):
        m = Model("s0")
        #n=matrice.shape[1]
        n=self.nb_c
        var=[]
        for j in range(n):
            var.append(m.addVar(vtype=GRB.CONTINUOUS, name="w%d"%(j+1)))
        expr=LinExpr()
        
        #la premiere constrainte : la somme est egale a 1
        for j in range(n):
            expr+=var[j]
        m.addConstr(expr==1)
        #enlever l'affichage de Gurobi
        m.Params.OutputFlag=0
        
        i=0
        pmr_matrice=pmr(self.matrice)
        matrice_mr,worst_ad=max_regret(pmr_matrice,self.label)

        while(min(matrice_mr)>0):
        
            matrice_mr,worst_ad=max_regret(pmr_matrice,self.label)
            print("matrice_mr is",matrice_mr)
            print("minimum in matrice_mr is",min(matrice_mr))
            sol=np.argmin(matrice_mr)
            print(self.label)
            print("iteration",i+1)
            print("the solution de min-max regret est solution",self.label[sol])
            pire_ad=int(worst_ad[sol])
            print("son pire adversaire est la solution",self.label[pire_ad])
            if(self.label[sol]==self.label[pire_ad]):
                print("best solution est solution",self.label[sol])
                return self.label[sol],self.nb_question
                break
            expr1=expression(var,self.matrice[sol,:])
            expr2=expression(var,self.matrice[pire_ad,:])
            self.nb_question+=1
            if(Query(self.poids,self.matrice[sol,:],self.matrice[pire_ad,:])):
                print(self.matrice[sol,:],self.matrice[pire_ad,:])
                print("solution",self.label[sol],"est plus prefere que",self.label[pire_ad])
                m.addConstr(expr1<=expr2)
                self.label.pop(pire_ad)
                delete=pire_ad
                
            else:
                print("solution",self.label[pire_ad],"est plus prefere que",self.label[sol])
                self.label.pop(sol)
                m.addConstr(expr2<=expr1)
                delete=sol
           
            self.matrice,pmr_matrice=newPMR(m,self.matrice,pmr_matrice,delete,var)
            i+=1
