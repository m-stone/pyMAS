# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 21:44:56 2024

@author: stone
"""

import numpy as np

def ConstructMSUP(ComponentDict):
    MSUP = np.array([[]])
    for idx, node in enumerate(ComponentDict['Nodes']):
        if idx == 0:
            MSUP = np.array([[node.id,node.r1,node.r2]])
        else:
            MSUP = np.concatenate((MSUP,[[node.id,node.r1,node.r2]]),axis=0)
    return MSUP
    
def ConstructNSC(ComponentDict):
    NSC = np.array([])
    return NSC

