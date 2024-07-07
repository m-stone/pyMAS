# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 12:01:56 2024

@author: stone
"""

from pathlib import Path
import numpy as np
import pymas.components as pmc

def ParseTrussInput(fname = 'truss.txt'):
    # Have to parse the input file. Do this according to Kassimali or other method?
    fpath = Path(fname)
    nodelist = []
    matlist = []
    sxnlist = []
    memberlist = []
    inputidx = 0
    typelist = ['JOINTS','SUPPORTS','MATERIALS','SECTIONS','MEMBERS','LOADS']
    with fpath.open('r+') as fin:
        for line in fin:
            # skip blank lines and comments
            if line == '\n' or line[0] == '#': continue
            # strip newline
            line = line.strip()
            if line in typelist:
                input_type = line
                print(line)
                continue
            if line == 'END':
                print(f'Read in {inputidx} items.')
                input_type = None
                inputidx = 0
            if input_type == 'JOINTS':
                # joint procedure
                coord = np.array(line.split(','),dtype=float).tolist()
                nodelist.append(pmc.Node(inputidx,coord))
                inputidx += 1
            if input_type == 'SUPPORTS':
                [nodenum,r1,r2] = [int(i) for i in line.split(',')]
                nodelist[nodenum].SetRestraints([r1,r2])
                inputidx += 1
            if input_type == 'MATERIALS':
                [E, rho] = [float(i) for i in line.split(',')]
                matlist.append(pmc.Material(inputidx, E, rho))
                inputidx += 1
            if input_type == 'SECTIONS':
                sxnlist.append(pmc.Section(inputidx,float(line)))
                inputidx += 1
            if input_type == 'MEMBERS':
                [n1, n2, mat, sxn] = [int(i) for i in line.split(',')]
                memberlist.append(pmc.Member(inputidx,nodelist[n1],nodelist[n2],matlist[mat],sxnlist[sxn]))
                inputidx += 1
            if input_type == 'LOADS':
                [n,fx,fy] = line.split(',')
                n = int(n)
                fx,fy = float(fx), float(fy)
                nodelist[n].SetLoads([fx,fy])
                inputidx += 1
                
    ComponentDict = {'Nodes' : nodelist,
                     'Materials' : matlist,
                     'Sections' : sxnlist,
                     'Members' : memberlist}
    
    return ComponentDict
            
        
        
