import warnings
import nglview as nv 
import Bio
from Bio.PDB import PDBParser
import sys

"""
Simple program for 3D structural vizualization with nglview
This snippet is passed to the jupyter-notebook.
The pdb variable is always updated with the desired pdb id.
"""

pdb="4yom"

print(pdb)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', Bio.PDB.PDBExceptions.PDBConstructionWarning)
    parser = PDBParser()
    structure = parser.get_structure(pdb, "pdb"+pdb+".ent")

w = nv.show_biopython(structure)
w