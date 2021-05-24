# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:56:05 2019

@author: WanZiqian
"""
import random

# this function randomly sample an edge from the neighbor of the subgraph
def ConditionalSampleEdge(edge_list,subgraph,dict_edge,L): 
    # inputs the graph,the sampled subgraph,a dictionary which documents 
    #neighbor edges of each node, and the max number of the sampled edges
    
    # find all vertice in the subgraph
    V = []
    
    for e in subgraph: #find all the node in the subgraph
        for v in e:            
            if v not in V:
                V.append(v)
    
    # find ids of adjacent edges of the subgraph
    neighbor = []
    
    for v in V:
        neighbor.extend(dict_edge[v]) #find all the neighbors of the subgraph
    
    # filter, deduplicate    
    neighbor2 = []
    
    for i in neighbor:
        if i not in neighbor2 and i>L:
            neighbor2.append(i)
    num_n = len(neighbor2)  
    
    # randomly samples an edge from the neighbors
    if num_n == 0: #if the subgraph has no neighbor
        p = 'Inf'
        e = [0,0]
        l = 0
        
    else:
        p = 1/float(num_n)
        l = int(neighbor2[random.randint(0,num_n-1)])
        e = edge_list[l]
        
    return e,p,l