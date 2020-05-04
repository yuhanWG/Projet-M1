import numpy as np
from gurobipy import *
import random

#05/04
def readCritere(nom_file):
    data=open(nom_file,'r')
    l=[]
    #l = [str(line) for line=line.strip('\n') in data]
    for line in data:
        line=line.strip('\n')
        l.append(str(line))

    return list(l)
    data.close()


def readFile(nom_file):
    data=open(nom_file,'r')
    next(data)
    l = [[float(num) for num in line.split()] for line in data]

    return np.asarray(l)
    data.close()


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
def max_regret(pmrM,l):
    nb_alt=pmrM.shape[0]
    max_regret=np.zeros(nb_alt)
    worst_ad=np.zeros(nb_alt)
    for i in range(nb_alt):
        max_regret[i]=np.ndarray.max(pmrM[i,:])
        worst_ad[i]=int(np.argmax(pmrM[i,:]))
    return max_regret,worst_ad


def expression(q,ligne):
    expr=LinExpr()
    for i in range(len(q)):
        expr+=q[i]*ligne[i]
    return expr


def newPMR(m,matrice,pmr,delete,q):
    matrice=np.delete(matrice,delete,0)
    pmr=np.delete(pmr,delete,0)
    pmr=np.delete(pmr,delete,1)
    #print("old pmr is",pmr)
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