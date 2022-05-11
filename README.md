# SciPyHW
Scientific Python University Course Project Repository
* Orsolya Réka Molnár (MS1YRR)
* István Szepesi-Nagy (K45SFS)
---
## Description
The aim of the project is to identify the structural domains of a given protein. 
The protein PDB file can be imported from locally or from the PDB database. 
The program calculates the least connected parts in the protein and plots the results on the GUI. 
The workload is distributed evenly, but Orsolya will be mainly responsible for the GUI implementation, 
while István will be responsible for the domain finder algorithm implementation. 
For version control and cooperative work, GitHub will be used.

---
## Usage
After starting the program all existing PDB files in the directory is added to the dropdown box. New PDB files can be downloaded after typing the PDB id into the text field and pushing the Get PDB button.
![getpdb](/SciPyHW/img/01.png)

------
The new pdb ("\*.ent") file is downloaded to the woriking directory.
![done](/SciPyHW/img/00.png)

-----
With the plot button the user can calculate and plot the results of the selected PDB protein. In the plot, the highest peak represents the domain cutting place in the sequence.
![plot](/SciPyHW/img/02.png)

-----
To view the protein in 3D the user can push the show3D button to start an external python file which opens the jupyter-notebook.
![command](/SciPyHW/img/03.png)

![3d](/SciPyHW/img/04.png)
