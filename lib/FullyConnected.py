# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:08:43 2019

@author: WanZiqian
"""

# this function generate the fully connected pattern of a given subgraph
def FullyConnected(subgraph):
    #find all vertice of the subgraph, and sort
    V = []
    for e in subgraph:
        for v in e:
            if v not in V:
                V.append(v)
    V.sort()
    
    #generate fully connected pattern (clique)
    clique = []            
    num_v = len(V)
    for i in range(num_v):
        for j in range(i+1,num_v):
            clique.append([V[i],V[j]])

    return clique