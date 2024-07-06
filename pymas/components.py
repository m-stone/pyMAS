# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:40:41 2024

@author: stone
"""

class Node:
    def __init__(self,
                 id: int,
                 position: list = [0., 0.],
                 restraints: list = [0, 0],
                 loads: list = [0., 0.]
                 ):
        self.id = id
        self.SetPosition(position)
        self.SetRestraints(restraints)
        self.SetLoads(loads)
        
    def SetPosition(self,
                    position: list = [0., 0.]
                    ):
        self.position = position
        
    def SetRestraints(self,
                     restraints: list = [0,0]):
        self.restraints = restraints
        
    def SetLoads(self,
                 loads: list = [0., 0.]):
        self.loads = loads
        
class Material:
    def __init__(self,
                 id: int,
                 modulus: float = 29000.,
                 density: float = 490
                 ):
        self.id = id
        self.modulus = modulus
        self.density = density
        
class Section:
    def __init__(self,
                 id: int,
                 area: float = 1.0
                 ):
        self.id = id
        self.area = area
        
class Member:
    def __init__(self,
                 id: int,
                 node1: Node,
                 node2: Node,
                 material: Material,
                 section: Section):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.material = material
        self.section = section
        
        
