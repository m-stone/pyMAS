# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 16:21:49 2024

@author: stone
"""

from pathlib import Path
import numpy as np
import pymas.components as pmc
import pymas.io

# Parse input deck
ComponentDict = pymas.io.ParseTrussInput('truss.txt')

print(ComponentDict)

        
        
        
