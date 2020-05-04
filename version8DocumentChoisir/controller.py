from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from home import *
from mainUi import *
from endPage import *


class Controller:
	def __init__(self):
		pass

	def show_home(self):
		self.home=Home()
		self.home.switch_page.connect(self.show_quiz)
		self.home.show()

	def show_quiz(self,index):
		self.quiz=MainUi(index)
		self.quiz.switch_page.connect(self.show_result)
		self.home.close()
		self.quiz.show()

	#img,self.sol,self.matrice[self.sol,:],self.cpt,self.label
	def show_result(self,img,sol,info,cpt,label,critere,path):
		self.result=endpage(img,sol,info,cpt,label,critere,path)
		self.result.switch_page.connect(self.recommencer)
		self.quiz.close()
		self.result.show()

	def recommencer(self):

		self.result.close()
		self.show_home()

def main():
	app=QApplication(sys.argv)
	controller=Controller()
	controller.show_home()
	sys.exit(app.exec_())

if __name__=="__main__":
	main()