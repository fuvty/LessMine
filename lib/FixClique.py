# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 2020

@author: TianyuFu
"""
import random
import math

def FixClique(e1,dict_node,num_clique,comb_table):
    fix_node = []
    # fix first two nodes ; note that the first one is the smallest
    if e1[0] <= e1[1]:
        fix_node.append(e1[0])
        fix_node.append(e1[1])
    else:
        fix_node.append(e1[1])
        fix_node.append(e1[0])

    # find cadidate notes
    candidate_node = [] 
    # print("allINfo",fix_node[0],dict_node[fix_node[0]])
    for index,node in enumerate(dict_node[fix_node[0]]):
        if node > fix_node[1]:
            break
    
    # print("e1,index,node",e1,index,dict_node[fix_node[0]])
    candidate_node = dict_node[fix_node[0]][index:]
    # print("candicateNode",candidate_node)
    if len(candidate_node) < num_clique-2:
        return [0,[]]
    fix_node.extend(random.sample(candidate_node,num_clique-2))
    # print("fixNode=",fix_node,end='')

    # cauculate probability
    n = len(candidate_node)
    max_comb = comb_table[0]
    if n < max_comb:
        invP = comb_table[n]
    else:
        # print("num_neighbor_exceed",n)
        m = num_clique-2
        invP = math.factorial(n)//(math.factorial(n-m)*math.factorial(m))
    # can be better;remember C
    # print(" Prob=",invP)
    return[invP,fix_node]


def PreComb(num_clique,max_comb):
    comb_table = [max_comb]
    m = num_clique-2
    for n in range(1,m):
        comb_table.append(0)
    for n in range(m,max_comb):
        invP = math.factorial(n)//(math.factorial(n-m)*math.factorial(m))
        comb_table.append(invP)

    return comb_table