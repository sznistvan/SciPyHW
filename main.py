import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Bio.PDB import *

def main():
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
	open_.triggered.connect(openPDB)
	exit.triggered.connect(lambda: exitProgram(app))

	msg = QLabel('Welcome! Open a PDB file!',parent=window)
	msg.setAlignment(Qt.AlignCenter)

	textbox = QLineEdit()
	button = QPushButton("Get PDB")

	button.clicked.connect(lambda: openPDB(textbox.text()))

	layout.addWidget(msg)
	layout.addWidget(textbox)
	layout.addWidget(button)

	window.setLayout(layout)
	window.show()
	sys.exit(app.exec_())

def openPDB(PDBID):
	print("{}\\{}.cif".format(os.getcwd(),PDBID))
	pathtofile = "{}\\{}.cif".format(os.getcwd(),PDBID)
	if(not os.path.exists(pathtofile)):
		print("Collecting PDB")

		pdbl = PDBList()
		pdbl.retrieve_pdb_file(PDBID,pdir=os.getcwd())
	else:
		print("PDB file exists")

def exitProgram(app):
	app.quit()


if __name__ == '__main__':
	main()