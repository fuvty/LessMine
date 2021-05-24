
# -*- coding: utf-8 -*-
"""
@author: TianyuFu
"""
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

import random

from lib import *

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
    dict_node = MakeDiDictionary(edge_list)


    
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

def LessMine_core(target: list, adj_di_dict: dict, query: nx.Graph, emb_cmp_dict: dict, num_estimator):   
    '''
    The core function of LessMine
    inputs: 
    [target] : list of tuples, the edge list of target graph. Need to be sorted
    [query_dict] : the emb_cmp_dict of LessMine
    [num_estimator] : number of estimators used in LessMine
    ''' 

    # get basic info
    num_target_e = len(target)
    num_query_n = query.number_of_nodes() 

    # make the combination table
    max_comb = max(len(adj_di_dict.values()))
    comb_table = PreComb(num_query_n, max_comb)
    # comb_table = PreComb(num_query_n,int((2*len(target))**0.5) )

    total_count = 0.0
    avg_count = []
    target = []
    for i in range(num_estimator):
        # randomly sample an edge from the graph
        [e1,invP1,pos] = SampleEdge(target,num_target_e) 
        # concurrent sample
        invP2,fix_node_list = ConcurrentSample(e1,adj_di_dict,num_query_n,comb_table) 
        if invP2 == 0:
            count = 0
        else:
            if UniformClose(fix_node_list, adj_di_dict, emb_cmp_dict):
                count = invP1*invP2
            else:
                count = 0

        total_count += count
        avg_count.append(total_count/(i+1))

    return avg_count


def LessMine_main(target_filename: str, query: nx.Graph, num_estimator):
    '''
    The main function of LessMine
    inputs: 
    [target_filename] : str, indicate the filename of the edge list of the target graph
    [query] : nx.Graph, the networkx instance of query. 
    WARNING: temporarily only support cliques 
    [num_estimator] : number of estimators used in LessMine
    '''

    edge_list = []
    node_set = set()  
    # read, make first node smaller, sort
    ReadEdgeFile(target_filename, edge_list, node_set)

    # generate schedule 
    emb_cmp_dict = MakeEmbCmpDict(query)
    print('generate',len(emb_cmp_dict),'schedule')

    adj_di_dict = MakeDictionary(edge_list)

    avg_count = LessMine_core(edge_list, adj_di_dict, query, emb_cmp_dict, num_estimator)

    return avg_count
    
def main():
    target_filename = './data/2987624.txt'
    num_estimator = 1000000

    query = nx.Graph()
    query.add_edges_from([(0,1),(0,2),(1,2)]) # triangle
    
    LessMine_main('./data/2987624.txt', query, num_estimator)
    
if __name__ == '__main__':
    main()