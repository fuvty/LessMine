# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:50:54 2019

@author: WanZiqian
"""

import random

# this function randomly samples an edge from the graph
# modified invP = 1/p
def SampleEdge(edge_list,num_e):
    
    # the probability of sample an edge
    invP = num_e 
    
    # randomly samples an edge
    l = random.randint(0,num_e-1)
    e = edge_list[l]

    # output the edge, probability and edge id
    return e,invP,l

def SampleEdges(edge_list,num_e,N):
    # the probability of sample an edge
    invP = num_e 
    es = []
    
    # randomly samples an edge
    if N<num_e:
        ls = random.sample(range(num_e),k=N)
    else:
        ls = [i for i in range(num_e)]
        print("N exceed num_e")
    for l in ls:
        es.append(edge_list[l])

    # output the edge, probability and edge id
    return es,invP