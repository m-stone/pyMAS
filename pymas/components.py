# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:40:41 2024

@author: stone
"""

import numpy as np

class Node:
    def __init__(self,
                 id: int,
                 ndof: int = 2,
                 position: np.ndarray = np.zeros(2),
                 restraints: np.ndarray = np.zeros(2),
                 loads: np.ndarray = np.zeros(2)
                 ):
        self.id = id
        self.ndof = ndof
        self.SetPosition(position)
        self.SetRestraints(restraints)
        self.SetLoads(loads)
        self.scn1, self.scn2 = 0, 0
        self.scn = np.array([self.scn1, self.scn2])
        
    def SetPosition(self,
                    position: np.ndarray = np.zeros(2)
                    ):
        self.position = position
        [self.x, self.y] = position
        
    def SetRestraints(self,
                     restraints: np.ndaray = np.zeros(2)):
        self.restraints = restraints
        [self.r1, self.r2] = restraints
        
    def SetLoads(self,
                 loads: np.ndarray = np.zeros(2)):
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
                 density: float = 0.28,
                 nu: float = 0.30
                 ):
        self.id = id
        self.E = modulus
        self.rho = density
        self.nu = nu
        
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
        
class Truss:
    def __init__(self,
                 member_id: int,
                 node1: Node,
                 node2: Node,
                 material: Material,
                 section: Section ):
        self.member_id = member_id
        self.node1 = node1
        self.node2 = node2
        self.ndof = node1.ndof
        self.material = material
        self.section = section
        self.CalculateLength()
        
        self.k = np.zeros((2,2))
        self.SetLocalStiffness()
        self.Transform = np.zeros((2,2*self.ndof))
        self.SetTransform()
        self.SetGlobalTransform()
        
    def CalculateLength(self):
        # Calculate Length
        self.length = np.linalg.norm(self.node2.position - self.node1.position)
        # Calculate global cosines
        self.COS = np.zeros(self.ndof)
        for idx in range(self.ndof):
            self.COS[idx] = (self.node2.position[idx] - self.node1.position[idx]) / self.length
        
    def SetLocalStiffness(self):
        Z = self.material.E * self.section.Ag / self.length
        self.k = Z * np.array([[1, -1],
                               [-1, 1]])

    def SetTransform(self):
        for idx in range(self.ndof):
            self.Transform[0,idx] = self.COS[idx]
            self.Transform[1,self.ndof+idx] = self.COS[idx]
    
    def SetGlobalStiffness(self):
        self.K = np.matmul(np.matmul(self.Transform.T, self.k), self.Transform)
        
