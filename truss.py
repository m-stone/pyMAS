# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 16:21:49 2024

@author: stone
"""

from pathlib import Path
import numpy as np
import pymas.components as pmc

fpath = Path('truss.txt')

n1 = pmc.Node(0,[0,0])
n2 = pmc.Node(1,[0,3])
n3 = pmc.Node(2,[4,0])

# Have to parse the input file. Do this according to Kassimali or other method?
with fpath.open('r+') as fin:
    for line in fin:
        if line == '\n' or line[0] == '#': continue
    
        if line == 'JOINTS':
            pass
            # joint procedure
        if line == 'SUPPORTS':
            pass
        if line == 'MATERIALS':
            pass
        if line == 'SECTIONS':
            pass
        if line == 'MEMBERS':
            pass
        if line == 'LOADS':
            pass
    # lines = fin.readlines()
    # line = fin.readline()
    # while len(line) != 0:
    # # if len(line) == 0:
    #     # pass
    #     print(line)
        
        