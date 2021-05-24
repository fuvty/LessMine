
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:02:05 2019
Modified on Fri Feb 21 2020

@author: WanZiqian
@editor: TianyuFu
"""
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import time
from lib.SampleEdge import SampleEdge,SampleEdges
from lib.ConditionalSampleEdge import ConditionalSampleEdge
from lib.ConditionalClose import ConditionalClose
import numpy as np
from lib.Dictionary import Dictionary

from lib.FixClique import FixClique,PreComb
from lib.CloseClique import CloseClique
from lib.MakeDictionary import MakeDictionary
from lib.NeighbourBalence import NeighbourBalence


import random

def main_clique():    
    # input graph
    file = './data/2987624.txt'
    exact = 275961
    # for 25571(d) is triangle:105461
    # for 925872 is triangle:667129
    # for 2987624 is triangle:3056386; 4-clique:275961
    N = 200000
    # 5% bound 
    total_count = 0.0
    avg_count = []
    error = []
    num_partition = 1
    num_clique = 4
    
    
    with open(file, 'r') as f:
        rawlines = f.readlines()
    f.close()
    
    nodes = set()    
    Edge_list = []
    edge_list = []

    for line in rawlines:
        splitted = line.strip('\n').split()

        from_node = int(splitted[0])
        to_node   = int(splitted[1])
        
        nodes.add(from_node)
        nodes.add(to_node)

        
        Edge_list.append([from_node, to_node])

    num_E = len(Edge_list)
    print('size of the whole graph is',num_E)

    # partition(暂时先不用考虑图划分，这里划分成一份，相当于没划分)
    nodes_per_machine = dict()
    for a in nodes:
        nodes_per_machine[a] = random.randint(1,num_partition)
    
    # assigne each edge to a machine
    for j in range(num_E):
        if nodes_per_machine[Edge_list[j][0]]==1 and nodes_per_machine[Edge_list[j][1]]==1:
            edge_list.append(Edge_list[j])

    num_e = len(edge_list)    
    print('size of the first partition is',num_e)
    
    # to make the first node smaller than the second in every edge
    '''
    j=0
    while j < len(edge_list) : 
        if edge_list[j][0] > edge_list[j][1]:
            t = edge_list[j][0]
            edge_list[j][0] = edge_list[j][1]
            edge_list[j][1] = t
        # prevent self-loop
        elif edge_list[j][0] == edge_list[j][1]:
            del edge_list[j]
            j=j-1
        j=j+1
    num_e = len(edge_list)
    '''
    # to make the first node smaller than the second in every edge
    for j in range(num_e): 
        if edge_list[j][0]>edge_list[j][1]:
            t = edge_list[j][0]
            edge_list[j][0] = edge_list[j][1]
            edge_list[j][1] = t
    

    # sort the edges
    edge_list = sorted(edge_list,key=lambda x:(x[0],x[1])) 
    
    '''
    # visualize some e
    G = nx.Graph()
    for edge in edge_list[0:200]:
        G.add_edge(edge[0],edge[1])
    nx.draw(G,node_size=10,with_lables=True,pos=nx.spring_layout(G))
    plt.show()
    '''

    # get the dictionaries        
    dict_node = MakeDictionary(edge_list)


    
    comb_table = PreComb(num_clique,int((2*len(edge_list))**0.5) )

    # test
    e = range(1,N+1)
    plt.figure(figsize=(20,10))

    for k in range(1):
        # SACM algorithm
        i = 0

        # test
        total_count = 0
        avg_count = []
        error = []

        while i<N:
            [e1,invP1,l1] = SampleEdge(edge_list,num_e) # randomly sample an edge from the graph
            invP2,fix_node = FixClique(e1,dict_node,num_clique,comb_table) # fix all the nodes
            if invP2 == 0:
                count = 0
            else:
                if CloseClique(fix_node,dict_node):
                    count = invP1*invP2
                else:
                    count = 0

            total_count += count

            avg_count.append(total_count/(i+1))
            error.append(abs(avg_count[i]-exact)/exact*100)
            i += 1

        print(int(avg_count[-1]))
        print(f'{error[-1]:.3f}')
        # plt.plot(e,error,linewidth=1)
        # plt.plot(e,avg_count,linewidth=1)


    # plot the result    
    e = range(1,len(error)+1)
    plt.figure(figsize=(20,10))
    plt.plot(e,error,"r",linewidth=1)
    # plt.plot(e[-1000:],error[-1000:],"r",linewidth=1)
    # plt.plot(e,avg_count,"g",linewidth=1)
    plt.show()
    

def ReadFile(file,Edge_list,nodes):
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
    
    print('edge_num of the whole graph is',num_E)
    print('node_num of the graph is',len(nodes))
    
    return Edge_list,nodes


def SACM(Edge_list,nodes,N,exact=1):    
    # 5% bound 
    total_count = 0.0
    avg_count = []
    error = []
    edge_list = []
    num_partition = 1
    num_clique = 4
    
    num_E = len(Edge_list)
    print('size of the whole graph is',num_E)

    # partition(暂时先不用考虑图划分，这里划分成一份，相当于没划分)
    edge_list = Edge_list
    '''
    nodes_per_machine = dict()
    for a in nodes:
        nodes_per_machine[a] = random.randint(1,num_partition)
    '''
    # assigne each edge to a machine
    '''
    for j in range(num_E):
        if nodes_per_machine[Edge_list[j][0]]==1 and nodes_per_machine[Edge_list[j][1]]==1:
            edge_list.append(Edge_list[j])
    '''
    num_e = len(edge_list)    
    print('size of the first partition is',num_e)
    
    # to make the first node smaller than the second in every edge
    '''
    j=0
    while j < len(edge_list) : 
        if edge_list[j][0] > edge_list[j][1]:
            t = edge_list[j][0]
            edge_list[j][0] = edge_list[j][1]
            edge_list[j][1] = t
        # prevent self-loop
        elif edge_list[j][0] == edge_list[j][1]:
            del edge_list[j]
            j=j-1
        j=j+1
    num_e = len(edge_list)
    '''
    # to make the first node smaller than the second in every edge
    for j in range(num_e): 
        if edge_list[j][0]>edge_list[j][1]:
            t = edge_list[j][0]
            edge_list[j][0] = edge_list[j][1]
            edge_list[j][1] = t
    

    # sort the edges
    start = time.perf_counter()
    edge_list = sorted(edge_list,key=lambda x:(x[0],x[1])) 
    end = time.perf_counter()
    print('sort time: %s Seconds'%(end-start))
    
    '''
    # visualize some e
    G = nx.Graph()
    for edge in edge_list[0:200]:
        G.add_edge(edge[0],edge[1])
    nx.draw(G,node_size=10,with_lables=True,pos=nx.spring_layout(G))
    plt.show()
    '''

    # get the dictionaries        
    dict_node = MakeDictionary(edge_list)


    
    comb_table = PreComb(num_clique,int((2*len(edge_list))**0.5) )

    # test
    plt.figure(figsize=(20,10))

    
    for k in range(1):
        Lstart = time.perf_counter()
        # SACM algorithm
        i = 0

        # test
        total_count = 0
        avg_count = []
        error = []
        
        
        #[es,invP1] = SampleEdges(edge_list, num_e, N)
        while i<N:
            [e1,invP1,l1] = SampleEdge(edge_list,num_e) # randomly sample an edge from the graph
            invP2,fix_node = FixClique(e1,dict_node,num_clique,comb_table) # fix all the nodes
            if invP2 == 0:
                count = 0
            else:
                if CloseClique(fix_node,dict_node):
                    count = invP1*invP2
                else:
                    count = 0

            total_count += count

            avg_count.append(total_count/(i+1))
            error.append(abs(avg_count[i]-exact)/exact*100)
            i += 1
            if i%100000 == 0:
                print("i=",i,"error=",error[-1])

        Lend = time.perf_counter()
        print('Loop time: %s Seconds'%(Lend-Lstart))
        
        print(int(avg_count[-1]))
        print("error=",f'{error[-1]:.3f}',"%")
        
        plt.plot([i for i in range(len(error))],error,linewidth=1)
        plt.show()
        
        # plt.plot(e,avg_count,linewidth=1)


    # plot the result    
    # e = range(1,len(error)+1)
    # plt.figure(figsize=(20,10))
    # plt.plot(e,error,"r",linewidth=1)
    # plt.plot(e[-1000:],error[-1000:],"r",linewidth=1)
    # plt.plot(e,avg_count,"g",linewidth=1)
    plt.show()

    
    
    
if __name__ == '__main__':
    Edge_list = []
    nodes = set()  
    Edge_list,nodes = NeighbourBalence('./data/819306.txt',Edge_list,nodes)
    # Edge_list,nodes = ReadFile('./data/2987624.txt',Edge_list,nodes)
    N = 1000000
    exact = 5240250
    SACM(Edge_list,nodes,N,exact)