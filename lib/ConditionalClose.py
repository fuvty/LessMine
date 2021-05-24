# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 16:07:35 2019

@author: WanZiqian
"""
from lib.FullyConnected import FullyConnected

# this function try to find edges to complete the pattern in the stream
# it is used in neighborhood method
def ConditionalClose(edge_list,subgraph1,L,dict_loc,dict_node):
    # input the graph, the subgraph, the max number of the sampled edges and 2 dictionaries
    
    found = 1
    
    # find the edges needed to complete the pattern
    subgraph3 = []
    subgraph2 = FullyConnected(subgraph1)

    for e in subgraph2:
        if e not in subgraph1:
            subgraph3.append(e) #subgraph3 is the subgraph needed to complete the pattern
    
    # try to find the edges in the edge stream
    for e in subgraph3:
        if e[0] not in dict_node: #if the first node is not in the keys of dict_node, then the edge doesn't exist
            found = 0
            break
        
        if dict_loc[e[0]][1]<=L: #if the range of the searched edge is out of the remaining stream, then the edge doesn't exist
            found = 0
            break
        
        if e[1] not in dict_node[e[0]]: #if the second node is not in the dictionary, then the edge doesn't exist
            found = 0
            break
        
        left = max(L+1,dict_loc[e[0]][0]) #the left search boundary
        
        if e not in edge_list[left:dict_loc[e[0]][1]+1]: #execute this slowest code only if the above 3 condition is not enough to tell whether the edge exist
            found = 0
            break
    
    return found