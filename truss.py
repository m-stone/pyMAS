# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 16:21:49 2024

@author: stone
"""

from pathlib import Path
import numpy as np
import pymas.components as pmc
import pymas.io
import pymas.analysis

# Parse input deck
ComponentDict = pymas.io.ParseTrussInput('truss.txt')

# print(ComponentDict)

#MSUP
NCJT = 2 # 2 for plane, 3 for space
NJ = len(ComponentDict['Nodes'])
MSUP = pymas.analysis.ConstructMSUP(ComponentDict)
NR = MSUP[:,1:].sum()
NDOF = NCJT*NJ - NR
# print(MSUP)
# print(NJ,NR,NDOF)

print(f'{NR} restraints')

# NSC
NSC = pymas.analysis.ConstructNSC(ComponentDict, NDOF, NR, NCJT)
# print(NSC)

# Global Stiffness K
print('Global stiffness matrix K.')
K = pymas.analysis.ConstructGlobalStiffness(ComponentDict, NCJT)
# print(K)

cd = ComponentDict
nodes = cd['Nodes']
        
# Load Matrix P
print(f'Load matrix:')
P = pymas.analysis.ConstructJointLoadVector(ComponentDict, NCJT)
print(P)

# Calculate Resultant Displacements:
print(f'Resultant Displacements:')
D = np.matmul(np.linalg.inv(K[:NR,:NR]), P[:NR])
print(D)

DF = np.concatenate((D,np.zeros((NR,1))))

# Internal Forces
print('Internal forces:')
Q = np.matmul(K[NR:,:],DF)
print(Q)

print('Final joint load vector:')
P[NR:] += Q
print(P)