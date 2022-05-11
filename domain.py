#!/usr/bin/env python

import numpy
import matplotlib.pyplot as mt
import sys


"""
Domain class for the domain identification functions.
"""
class Domain:
    """
    Constructor inicializes an array for the results.
    """
    def __init__(self):
        self.to_plot = []

    """
    getDom function calculates the connection values between the atoms and stores them in an array.
    """
    def getDom(self,PBDID,Chain):

        print("GetDOM!")

        
        #Lists for the 3D coordinates for each Calpha atom.
        coordx = []
        coordy = []
        coordz = []

        pdb_resnum = []

        #the split value set to 8 angstroms
        cutoff = 8

        nres = 0

        protein_id =""
        error = False


        try:
            #open the pdb file
            pdbfile = open(PBDID,"r")
            if(pdbfile != None):
                print("ok")
                for line in pdbfile:
                    if line.startswith("HEADER"):
                        #store the protein name
                        protein_id=str(line[62:66])
                    # only ATOM lines will be read
                    if line.startswith("ATOM"):
                        #delete spaces for better handling
                        atom=line[12:15].replace(" ","")
                        # read the actual chain id in the line
                        chain=line[21:22]
                        # processing only lines of CA atoms in Chain
                        if atom == "CA" and chain == Chain:
                            # store all three coordinates of each atoms
                            coordx.append(float(line[30:37]))
                            coordy.append(float(line[38:45]))
                            coordz.append(float(line[46:53]))
                            # storing the residue neumbers
                            pdb_resnum.append(int(line[22:27]))
                            
                            nres=nres+1
        except FileNotFoundError:
            print("ERROR! PDB file doesn't exist!")
            error=True

        #create a residue x residue large matrix filled with 0s.
        contact_matrix = [[0 for h in range(nres)] for k in range(nres)]


        #calculate the distances. and update the matrix.
        for i in range(1, nres):
            for j in range(0, i): 
                distance=((coordx[i]-coordx[j])*(coordx[i]-coordx[j]))+((coordy[i]-coordy[j])*(coordy[i]-coordy[j]))+((coordz[i]-coordz[j])*(coordz[i]-coordz[j]))
                distance=numpy.sqrt(distance)

                if distance <= cutoff:
                    contact_matrix[j][i]=1
                    contact_matrix[i][j]=contact_matrix[j][i]

        #iterate through the matrix to find the number of intradomain contacts
        def contacts_intradomain(p, q):
            contacts_i=0
            for r in range(p,q):
                for s in range(p,r):
                    contacts_i+=contact_matrix[r][s]
                    
            return contacts_i
            
        #iterate through to find the interdomain contacts.
        def contacts_interdomain(p1, p2, q1, q2):
            contacts_e=0
            for r in range(p1,q1):
                for s in range(p2,q2):
                    contacts_e+=contact_matrix[r][s]

            return contacts_e


        """
        calculate the DOMAK values for each residue based on intradomain_A*intradomain_B/(interdomain_AB*interdomain_AB)
        formula.
        This part writes the values to the to_plot array.
        """
        for c in range (1, nres-1):
            intradomain_A=contacts_intradomain(0,c)
            intradomain_B=contacts_intradomain(c+1,nres)
            interdomain_AB=contacts_interdomain(0,c+1,c,nres)
            d=intradomain_A*intradomain_B/(interdomain_AB*interdomain_AB)
            print("A:", intradomain_A," B:",intradomain_B,"  AB:",interdomain_AB, "{} \t {}".format(pdb_resnum[c],d))
            self.to_plot.append(d)
            outp = "A:"+ str(intradomain_A)+" B:"+str(intradomain_B)+"  AB:"+str(interdomain_AB)+ "{} \t {}".format(pdb_resnum[c],d)+"\n"
            writefile.write(outp)

        print("ok_calculations")


    """
    plotDomains function creates the plot pane and plots to_plot array content
    This function is called in the mainwindow's plot button.
    """
    def plotDomains(self,PBDID):
        print("PLOTDOM!")
        mt.plot(self.to_plot,color="red")
        print(self.to_plot)
        mt.title("Domain identification ({})".format(PBDID))
        mt.xlabel("Residues")
        mt.ylabel("IntraA * IntraB / InterAB^2")
        mt.show()




