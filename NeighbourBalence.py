# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 14:02:05 2019
Modified on Fri Feb 21 2020

@author: WanZiqian
@editor: TianyuFu
"""
import networkx as nx
import matplotlib.pyplot as plt
import time
from lib.SampleEdge import SampleEdge
from lib.ConditionalSampleEdge import ConditionalSampleEdge
from lib.ConditionalClose import ConditionalClose
import numpy as np
from lib.Dictionary import Dictionary

from lib.FixClique import FixClique,PreComb
from lib.CloseClique import CloseClique
from lib.MakeDictionary import MakeDictionary,MakeFullDictionary

import random

EXTRA = 50


def NeighbourBalence(file,Edge_list,nodes):    
    # input graph
    # file = './data/819306.txt'
    
    '''
    exact = 29782587
    # for 25571(d) is triangle:105461
    # for 925872 is triangle:667129
    # for 2987624 is triangle:3056386
    N = 20000
    total_count = 0.0
    avg_count = []
    error = []
    num_partition = 1
    num_clique = 4
    '''
    
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
    print('size of the whole graph is',num_E)
    # DONE READ MESSAGE
    
    
    
    # START MEAN PROGRAM
    # dict_node = DictNeighbour(Edge_list)
    node_list = list(nodes)
    
    
    # Auto Balence based on half info
    '''
    dict_node = DictNeighbour(Edge_list)
    node_reindex = NeighbourAnalysis(node_list, dict_node)
    '''
    '''
    for i in range(2):
        dict_node = DictNeighbour(Edge_list)
        node_reindex = NeighbourAnalysis(node_list, dict_node)
        Edge_list = RefreshNodeList(Edge_list, node_reindex)
    '''
    # original
    dict_node = DictNeighbour(Edge_list)
    node_reindex = NeighbourAnalysis(node_list, dict_node)
    
    # Auto Balence Based on Full info
    dict_node = DictFullNeighbour(Edge_list)
    node_reindex = NodeIndexArrange(node_list, dict_node)
    Edge_list = RefreshNodeList(Edge_list, node_reindex)
    
    # visualization
    dict_node = DictFullNeighbour(Edge_list)
    NodeIndexArrange(node_list, dict_node)# show
    
    # dict_node = DictNeighbour(Edge_list)
    # node_reindex = NeighbourAnalysis(node_list, dict_node)
    
    # Auto Balence based on half info
    for i in range(0):
        dict_node = DictNeighbour(Edge_list)
        node_reindex = NeighbourAnalysis(node_list, dict_node)
        Edge_list = RefreshNodeList(Edge_list, node_reindex)
    
    # visualization
    dict_node = DictNeighbour(Edge_list)
    NeighbourAnalysis(node_list, dict_node)
    
    return Edge_list,nodes
    
    '''
    np_edge_list = np.array(Edge_list)
    MegaNode = np_edge_list.reshape(len(np_edge_list)*2)
    MegaNode.sort()
    # print(MegaNode)
    node_num = MegaNode[-1]
    node_re = {}
    for i in range(len(MegaNode)):
        MegaNode[i] = int(MegaNode[i]/100)
    for N in MegaNode:
        node_re[N] = node_re.get(N,0) + 1
    # print(node_re)
    '''
    # plt.plot( [i for i in range(len(node_re_sorted))]  , [ a[1] for a in node_re_sorted] ,"r",linewidth=1)
    # plt.plot( [i for i in node_re.keys() ] , [ i for i in node_re.values() ] ,"r",linewidth=1)
    print("done")

    '''
    # visualize some e
    G = nx.Graph()
    for edge in edge_list[0:200]:
        G.add_edge(edge[0],edge[1])
    nx.draw(G,node_size=10,with_lables=True,pos=nx.spring_layout(G))
    plt.show()
    '''
    
def PlotDistribution():
    return 0

def DictNeighbour(Edge_list):
    # to make the first node smaller than the second in every edge
    num_E = len(Edge_list)
    for j in range(num_E): 
        if Edge_list[j][0] > Edge_list[j][1]:
            t = Edge_list[j][0]
            Edge_list[j][0] = Edge_list[j][1]
            Edge_list[j][1] = t
    dict_node = MakeDictionary(Edge_list)
    return dict_node

def DictFullNeighbour(Edge_list):
    # to make the first node smaller than the second in every edge
    dict_node = MakeFullDictionary(Edge_list)
    return dict_node
    
def NeighbourAnalysis(node_list,dict_node):
    node_neighbour_num = {}
    node_list.sort()
    # count the num of neighbours of every node
    for i in range(node_list[-1]):
        if i not in dict_node.keys():
            node_neighbour_num[i] = 0
        else:
            node_neighbour_num[i] = len(dict_node[i])
    
    plt.title("Num of 1-way Neighbour Distribution")
    plt.plot( [i for i in node_neighbour_num.keys() ] , [ i for i in node_neighbour_num.values() ] ,"r",linewidth=1)
    plt.show()
    print("plot")
    
    #{key(nodeNo),neighbournum}
    #sort based on neighbournum 0->max            
    node_neighbour_num_sorted = sorted(node_neighbour_num.items(),key=lambda x:x[1])
    
    
    re_mean = np.mean( list(node_neighbour_num.values()) )
    print( "mean", re_mean )
    print("Max Neighbour Num",node_neighbour_num_sorted[-1][1])
    
    MegaNo = 0
    node_num = len(node_list)
    node_reindex = {}
    for e,i in enumerate( range(len(node_neighbour_num_sorted)-1,0,-1) ):
        swpnode = node_neighbour_num_sorted[e][0]
        node_reindex[ node_neighbour_num_sorted[i][0] ] = swpnode
        node_reindex[ swpnode ] = node_neighbour_num_sorted[i][0]
        # prevent double switch
        # can be better
        # considered too large
        if node_neighbour_num_sorted[i][1] < EXTRA*re_mean:
            MegaNo = i
            break
        
    print("MegaNo:",MegaNo,",means for",node_num,"nodes,there're",node_num-MegaNo,"extremely large ones,aka",float(node_num-MegaNo)*100/node_num,"%")
    return node_reindex
    
def RefreshNodeList(Edge_list,node_reindex):
    Edge_list_new = []
    for edge in Edge_list:
        tmp_from_node = edge[0]
        tmp_to_node = edge[1]
        if tmp_from_node in node_reindex.keys():
            tmp_from_node = node_reindex[tmp_from_node]
        if tmp_to_node in node_reindex.keys():
            tmp_to_node = node_reindex[tmp_to_node]
        Edge_list_new.append([tmp_from_node,tmp_to_node])
    return Edge_list_new

def NodeIndexArrange(node_list,dict_node):
    node_neighbour_num = {}
    node_list.sort()
    # count the num of neighbours of every node
    for i in range(node_list[-1]):
        if i not in dict_node.keys():
            node_neighbour_num[i] = 0
        else:
            node_neighbour_num[i] = len(dict_node[i])
    
    plt.title("Num of 2-way Neighbour Distribution")
    plt.plot( [i for i in node_neighbour_num.keys() ] , [ i for i in node_neighbour_num.values() ] ,"r",linewidth=1)
    plt.show()
    print("plot")
    
    #{key(nodeNo),neighbournum}
    #sort based on neighbournum 0->max            
    node_neighbour_num_sorted = sorted(node_neighbour_num.items(),key=lambda x:x[1])
    
    
    re_mean = np.mean( list(node_neighbour_num.values()) )
    print( "mean", re_mean )
    
    MegaNo = 0
    node_num = len(node_list)
    node_reindex = {}
    for e,i in enumerate( range(len(node_neighbour_num_sorted)-1,0,-1) ):
        swpnode = node_num -1 -e
        # prevent double switch
        # can be better
        if (swpnode not in node_reindex.keys()) and (node_neighbour_num_sorted[i][0] not in node_reindex.keys()):
            node_reindex[ node_neighbour_num_sorted[i][0] ] = swpnode
            node_reindex[ swpnode ] = node_neighbour_num_sorted[i][0]
        # considered too large
        if node_neighbour_num_sorted[i][1] < EXTRA*re_mean:
            MegaNo = i
            break
    print("MegaNo:",MegaNo,",means for",node_num,"nodes,there're",node_num-MegaNo,"extremely large ones(consider both direction),aka",float(node_num-MegaNo)*100/node_num,"%")
    return node_reindex
    
    

if __name__ == '__main__':
    Edge_list = []
    nodes = set()  
    Edge_list,nodes = NeighbourBalence('./data/2987624.txt',Edge_list,nodes)
    # print(Edge_list)