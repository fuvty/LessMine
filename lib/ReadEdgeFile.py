#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:03:58 2020

@author: futianyu
"""
import time

# read edge list and sort in ascending order
def ReadEdgeFile(file,Edge_list,nodes):
    with open(file, 'r') as f:
        rawlines = f.readlines()
    f.close()  

    for line in rawlines:
        splitted = line.strip('\n').split()

        from_node = int(splitted[0])
        to_node   = int(splitted[1])
        
        nodes.add(from_node)
        nodes.add(to_node)

        Edge_list.append([from_node, to_node])

    num_E = len(Edge_list)
    
    # to make the first node smaller than the second in every edge
    for j in range(num_E): 
        if Edge_list[j][0]>Edge_list[j][1]:
            t = Edge_list[j][0]
            Edge_list[j][0] = Edge_list[j][1]
            Edge_list[j][1] = t
    

    # sort the edges
    start = time.perf_counter()
    Edge_list = sorted(Edge_list,key=lambda x:(x[0],x[1])) 
    end = time.perf_counter()
    print('sort time: %s Seconds'%(end-start))
    
    print('edge_num of the whole graph is',len(Edge_list))
    print('node_num of the graph is',len(nodes))
    
    # return Edge_list,nodes