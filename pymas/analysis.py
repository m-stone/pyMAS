# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 21:44:56 2024

@author: stone
"""

import numpy as np
import itertools as iter

def ConstructMSUP(ComponentDict):
    MSUP = np.array([[]])
    for idx, node in enumerate(ComponentDict['Nodes']):
        if idx == 0:
            MSUP = np.array([[node.id,node.r1,node.r2]])
        else:
            MSUP = np.concatenate((MSUP,[[node.id,node.r1,node.r2]]),axis=0)
    return MSUP
    
def ConstructNSC(ComponentDict, NDOF, NR, NCJT: int = 2):
    # create empty zero array
    # print('nsc subroutine')
    NSC = np.zeros((len(ComponentDict['Nodes'])*NCJT,1)) - 1
    DOF_COUNTER, SUPPORT_COUNTER = 0, NR
    # print(DOF_COUNTER, SUPPORT_COUNTER)
    for idx, node in enumerate(ComponentDict['Nodes']):
        # print(idx, node.r1, node.r2)
        if node.r1 == 0:
            NSC[2*idx] = DOF_COUNTER
            node.SetSCN(1,DOF_COUNTER)
            DOF_COUNTER += 1
        elif node.r1 != 0:
            NSC[2*idx] = SUPPORT_COUNTER
            node.SetSCN(1, SUPPORT_COUNTER)
            SUPPORT_COUNTER += 1
        if node.r2 == 0:
            NSC[2*idx+1] = DOF_COUNTER
            node.SetSCN(2,DOF_COUNTER)
            DOF_COUNTER += 1
        elif node.r2 != 0:
            NSC[2*idx+1] = SUPPORT_COUNTER
            node.SetSCN(2, SUPPORT_COUNTER)
            SUPPORT_COUNTER += 1
        # print(NSC)
    # print(DOF_COUNTER, SUPPORT_COUNTER)
    return NSC

def ConstructGlobalStiffness(ComponentDict, NCJT: int = 2):
    dof = len(ComponentDict['Nodes']) * NCJT
    K = np.zeros((dof, dof))
    for idx, member in enumerate(ComponentDict['Members']):
        [[i,j],[k,l]] = [member.node1.scn, member.node2.scn]
        # print(i,j,k,l)
        for jdx, (ki,kj) in enumerate(iter.product(*[[i,j,k,l]],repeat=2)):
            # print(ki,kj)
            # print(member.k)
            # print(member.k.flatten()[jdx])
            K[ki,kj] += member.k.flatten()[jdx]
        # for node in [member.node1, member.node2]:
        #     # K[]
        #     pass
    return K

def ConstructJointLoadVector(ComponentDict, NCJT: int=2):
    dof = len(ComponentDict['Nodes']) * NCJT
    P = np.zeros((dof,1))
    for node in ComponentDict['Nodes']:
        P[node.scn1] += node.Px
        P[node.scn2] += node.Py
    return P