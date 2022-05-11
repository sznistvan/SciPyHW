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

	def get_combobox_value(self):
		return self.combobox.currentText()

	def main(self):
		app = QApplication(sys.argv)

		

		window = QWidget()
		window.setWindowTitle('Protein Domain Identifier')
		window.setGeometry(500,100,580,250)
		window.move(200,200)
		window.setStyleSheet("background-color: #e2e7f2")

		menubar = QMenuBar()
		

		layout = QVBoxLayout()

		layout.setMenuBar(menubar)
		file = menubar.addMenu("File")
		open_ = file.addAction("Open")
		exit = file.addAction("Exit")
		open_.triggered.connect(self.openPDB)
		exit.triggered.connect(lambda: self.exitProgram(app))

		msg = QLabel('Welcome! \n Open a PDB file!',parent=window)
		msg.setAlignment(Qt.AlignCenter)
		msg.setFont(QFont('Century',20))

		self.combobox = QComboBox()

		self.combobox.setFont(QFont('Century',10))

		MainWindow.find(self,'*.ent',os.getcwd())

		textbox = QLineEdit()
		textbox.setFont(QFont('Century',12))
		button = QPushButton("Get PDB")
		
		button.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color: #0b378c"
                             "}")
		button.setFont(QFont('Century',12))

		plotbutton = QPushButton("Plot")
		plotbutton.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color: #0b378c"
                             "}")
		plotbutton.setFont(QFont('Century', 12))

		button.clicked.connect(lambda: MainWindow.openPDB(self,textbox.text()))
		
		plotbutton.clicked.connect(lambda: MainWindow.plotActual(self,self.combobox.currentText()))

		showbutton = QPushButton("Show 3D")
		showbutton.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color: #0b378c"
                             "}")
		showbutton.setFont(QFont('Century', 12))
		showbutton.clicked.connect(lambda: MainWindow.show3D(self.combobox.currentText()))

		layout.addWidget(msg)
		layout.addWidget(self.combobox)
		layout.addWidget(textbox)
		layout.addWidget(button)
		layout.addWidget(plotbutton)
		layout.addWidget(showbutton)

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
	def plotActual(self,protein):
		print("PLOTTING")
		d = Domain()
		pdb_file_name="pdb{}.ent".format(protein)
		parser = PDBParser()
		structure = parser.get_structure(self.combobox.currentText(),"pdb"+self.combobox.currentText()+".ent")
		chains_list = []
		for model in structure:
			for chain in model:
				ch = str(chain)[-2:-1]
				chains_list.append(ch)
				print(ch)
		print(structure[0])
		Domain.getDom(d,pdb_file_name,chains_list[0])
		Domain.plotDomains(d,protein)

	def show3D(pdb):
		python_file = open("show3D.py","r")
		good_lines = []
		for line in python_file:
			print(line)
			if("pdb=" in line):
				good_lines.append("pdb=\""+pdb+"\"\n")
			else:
				good_lines.append(line)
		python_file.close()
		print(good_lines)

		python_new = open("show3D.py","w")
		for gl in good_lines:
			python_new.write(gl)
		python_new.close()
		os.system("start cmd.exe @cmd /k nglview show3D.py --auto")


if __name__ == '__main__':
	program = MainWindow()
	MainWindow.main(program)