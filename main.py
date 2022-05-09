import sys
import os
import fnmatch

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Bio.PDB import *

from domain import Domain

class MainWindow():

	def __init__(self):
		self.protein_list = []
		self.actualprot = None

	def main(self):
		app = QApplication(sys.argv)

		

		window = QWidget()
		window.setWindowTitle('Protein Domain Identifier')
		window.setGeometry(500,100,580,250)
		window.move(200,200)

		menubar = QMenuBar()
		

		layout = QVBoxLayout()

		layout.setMenuBar(menubar)
		file = menubar.addMenu("File")
		open_ = file.addAction("Open")
		exit = file.addAction("Exit")
		open_.triggered.connect(self.openPDB)
		exit.triggered.connect(lambda: self.exitProgram(app))

		msg = QLabel('Welcome! Open a PDB file!',parent=window)
		msg.setAlignment(Qt.AlignCenter)

		self.combobox = QComboBox()

		MainWindow.find(self,'*.ent',os.getcwd())

		textbox = QLineEdit()
		button = QPushButton("Get PDB")
		plotbutton = QPushButton("Plot")

		button.clicked.connect(lambda: MainWindow.openPDB(self,textbox.text()))
		
		plotbutton.clicked.connect(lambda: MainWindow.plotActual(self.combobox.currentText()))

		layout.addWidget(msg)
		layout.addWidget(self.combobox)
		layout.addWidget(textbox)
		layout.addWidget(button)
		layout.addWidget(plotbutton)

		window.setLayout(layout)
		window.show()
		sys.exit(app.exec_())

	def openPDB(self,PDBID):
		print("{}\\pdb{}.ent".format(os.getcwd(),PDBID))
		pathtofile = "{}\\pdb{}.ent".format(os.getcwd(),PDBID)
		if(not os.path.exists(pathtofile)):
			print("Collecting PDB")

			pdbl = PDBList()
			pdbl.retrieve_pdb_file(PDBID,pdir=os.getcwd(),file_format="pdb")
			self.combobox.addItem(PDBID)
		else:
			print("PDB file exists")

	def exitProgram(app):
		app.quit()

	def find(self,pattern, path):
	    result = []
	    for root, dirs, files in os.walk(path):
	        for name in files:
	            if fnmatch.fnmatch(name, pattern):
	                result.append(os.path.join(root, name))
	                self.combobox.addItem(name[3:7])
	                print(result)
	    return result
	def plotActual(protein):
		print("PLOTTING")
		d = Domain()
		pdb_file_name="pdb{}.ent".format(protein)
		Domain.getDom(d,pdb_file_name)
		d.plotDomains(protein)


if __name__ == '__main__':
	program = MainWindow()
	MainWindow.main(program)