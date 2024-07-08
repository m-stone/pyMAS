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

# NSC
NSC = pymas.analysis.ConstructNSC(ComponentDict, NDOF, NR, NCJT)
# print(NSC)

# Global Stiffness K
K = pymas.analysis.ConstructGlobalStiffness(ComponentDict, NCJT)
print('Global stiffness matrix K:')
print(K)

cd = ComponentDict
nodes = cd['Nodes']
        
# Load Matrix P