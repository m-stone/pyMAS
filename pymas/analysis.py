# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 21:44:56 2024

@author: stone
"""

import numpy as np

def ConstructMSUP(ComponentDict):
    MSUP = np.array([])
    for node in ComponentDict['Nodes']:
        MSUP = np.append([MSUP,[node.id,node.r1,node.r2]])
    
    return MSUP
    

