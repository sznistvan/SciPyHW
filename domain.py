#!/usr/bin/env python

import numpy
import matplotlib.pyplot as mt
import sys

class Domain:

    def __init__(self):
        self.to_plot = []

    def getDom(self,PBDID):

        coordx = []
        coordy = []
        coordz = []

        pdb_resnum = []


        cutoff = 8

        nres = 0

        protein_id =""
        error = False


        try:
            pdbfile = open(PBDID,"r")
            if(pdbfile != None):
                print("ok")
                for line in pdbfile:
                    if line.startswith("HEADER"):
                        protein_id=str(line[62:66])
                    # only ATOM lines will be considered
                    if line.startswith("ATOM"):
                        # obtaining the atom name and getting rid of spaces
                        atom=line[12:15].replace(" ","")
                        # the chain identifier is 1 character
                        chain=line[21:22]
                        # processing only lines of CA atoms in chain E
                        if atom == "CA" and chain == "A":
                            # the append function adds a value to the array. The substring at given positions of the line
                            # should be converted to a floating-point number.
                            coordx.append(float(line[30:37]))
                            coordy.append(float(line[38:45]))
                            coordz.append(float(line[46:53]))
                            # storing residue numbers, they are integers 
                            pdb_resnum.append(int(line[22:27]))
                            # we have appended a value to each array, they should have equal size and the data
                            # for the same residue should be accessible at the same index that corresponds to nres 
                            # (the first index is zero and we set nres to zero above). Now we increase nres to keep track.
                            nres=nres+1
        except FileNotFoundError:
            print("ERROR! PDB file doesn't exist!")
            error=True
        else:
            print("ERROR! Usage: python {} PROT.pdb CHAIN".format(sys.argv[0])) 
            error = True


        contact_matrix = [[0 for h in range(nres)] for k in range(nres)]



        for i in range(1, nres):
            for j in range(0, i): 
                distance=((coordx[i]-coordx[j])*(coordx[i]-coordx[j]))+((coordy[i]-coordy[j])*(coordy[i]-coordy[j]))+((coordz[i]-coordz[j])*(coordz[i]-coordz[j]))
                distance=numpy.sqrt(distance)

                if distance <= cutoff:
                    contact_matrix[j][i]=1
                    contact_matrix[i][j]=contact_matrix[j][i]

        
        def contacts_intradomain(p, q):
            contacts_i=0
            for r in range(p,q):
                for s in range(p,r):
                    contacts_i+=contact_matrix[r][s]
                    
            return contacts_i
            
        def contacts_interdomain(p1, p2, q1, q2):
            contacts_e=0
            for r in range(p1,q1):
                for s in range(p2,q2):
                    contacts_e+=contact_matrix[r][s]

            return contacts_e

        writefile = open("output.txt","a")
        for c in range (1, nres-1):
            intradomain_A=contacts_intradomain(0,c)
            intradomain_B=contacts_intradomain(c+1,nres)
            interdomain_AB=contacts_interdomain(0,c+1,c,nres)
            d=intradomain_A*intradomain_B/(interdomain_AB*interdomain_AB)
            print("A:", intradomain_A," B:",intradomain_B,"  AB:",interdomain_AB, "{} \t {}".format(pdb_resnum[c],d))
            self.to_plot.append(d)
            outp = "A:"+ str(intradomain_A)+" B:"+str(intradomain_B)+"  AB:"+str(interdomain_AB)+ "{} \t {}".format(pdb_resnum[c],d)+"\n"
            writefile.write(outp)



    def plotDomains(self,PBDID):
        mt.plot(self.to_plot,color="red")
        mt.title("Domain identification ({})".format(PBDID))
        mt.xlabel("Residues")
        mt.ylabel("IntraA * IntraB / InterAB^2")
        mt.show()




