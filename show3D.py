import warnings
import nglview as nv 
import Bio
from Bio.PDB import PDBParser
import sys

pdb="4yom"

print(pdb)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', Bio.PDB.PDBExceptions.PDBConstructionWarning)
    parser = PDBParser()
    structure = parser.get_structure(pdb, "pdb"+pdb+".ent")

w = nv.show_biopython(structure)
w