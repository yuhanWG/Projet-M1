from PyQt5.QtGui import *
import numpy as np

class color():
#nous allez construire une couleur en utilisant les donnees
	def __init__(self,donnee):
		#dmax=np.max(donnee)
		#donnee=donnee/(255/dmax)
		self.r,self.g,self.b=donnee/(255/np.max(donnee))

	def getColor():
		c=(self.r,self.g,self.b)
		return c
