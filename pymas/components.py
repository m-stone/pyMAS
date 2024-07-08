# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:40:41 2024

@author: stone
"""

import numpy as np

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
        self.scn1, self.scn2 = 0, 0
        self.scn = np.array([self.scn1, self.scn2])
        
    def SetPosition(self,
                    position: list = [0., 0.]
                    ):
        #self.position = position
        [self.x, self.y] = position
        
    def SetRestraints(self,
                     restraints: list = [0,0]):
        self.restraints = restraints
        [self.r1, self.r2] = restraints
        
    def SetLoads(self,
                 loads: list = [0., 0.]):
        #self.loads = loads
        [self.Px, self.Py] = loads
        
    def SetSCN(self, dof: int = 1, scn: int = 0):
        if dof == 1:
            self.scn1 = scn
        else:
            self.scn2 = scn
        self.scn = np.array([self.scn1, self.scn2])
        
class Material:
    def __init__(self,
                 id: int,
                 modulus: float = 29000.,
                 density: float = 0.28
                 ):
        self.id = id
        self.E = modulus
        self.rho = density
        
class Section:
    def __init__(self,
                 id: int,
                 area: float = 1.0
                 ):
        self.id = id
        self.Ag = area
        
class Member:
    def __init__(self,
                 id: int,
                 node1: Node,
                 node2: Node,
                 material: Material,
                 section: Section,
                 member_type: str = 'truss'):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.material = material
        self.section = section
        self.member_type = member_type
        self.CalculateLength()
        self.k = np.zeros((4,4))
        self.SetLocalStiffness()
        
    def CalculateLength(self):
        self.length = np.linalg.norm([self.node2.x-self.node1.x,
                                      self.node2.y-self.node1.y])
        self.CX = (self.node2.x - self.node1.x) / self.length
        self.CY = (self.node2.y - self.node1.y) / self.length
        
    def SetLocalStiffness(self):
        Z = self.material.E * self.section.Ag / self.length
        Z1 = Z * np.power(self.CX,2)
        Z2 = Z * np.power(self.CY,2)
        Z3 = Z * self.CX * self.CY
        self.k = np.array([[Z1, Z3, -Z1, -Z3],
                           [Z3, Z2, -Z3, -Z2],
                           [-Z1, -Z3, Z1, Z3],
                           [-Z3, -Z2, Z3, Z2]])
        
