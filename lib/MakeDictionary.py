# -*- coding: utf-8 -*-
"""
Motified on Sat Feb 22 2020

@author: WanZiqian
@edit: FuTianyu
"""
# this function outputs 1 dictionary of a graph, which is used to make the basic functions(FC,CC) run faster
#@profile
import copy

def MakeDictionary(edge_list): 
    
    dict_node = dict() #document the neighbor nodes of the first node in the edge_list
    
    for i in range(len(edge_list)):
        if edge_list[i][0] not in dict_node:
            dict_node[edge_list[i][0]] = [edge_list[i][1]]
        else:
            # prevent double edge
            # if edge_list[i][1] not in dict_node[edge_list[i][0]]:
                dict_node[edge_list[i][0]].extend([edge_list[i][1]])

    return dict_node


def MakeFullDictionary(old_edge_list): 
    # Alert: Will Double Edge-List
    # edge_list has to be undirected one-way edge ;
    # e.g if [1,2] in edge_list,then [2,1] can't be in it
    dict_node = dict() #document the neighbor nodes of the first node in the edge_list
    reverse_edge_list = [ [e[1],e[0]] for e in old_edge_list ]
    edge_list = copy.deepcopy(old_edge_list)
    edge_list.extend(reverse_edge_list)
    
    for i in range(len(edge_list)):
        if edge_list[i][0] not in dict_node:
            dict_node[edge_list[i][0]] = [edge_list[i][1]]
        else:
            # prevent double edge
            # if edge_list[i][1] not in dict_node[edge_list[i][0]]:
                dict_node[edge_list[i][0]].extend([edge_list[i][1]])
    return dict_node

if __name__ == '__main__':
    edge_list = [[1,2],[3,4]]
    dict_node = MakeFullDictionary(edge_list)
    print(edge_list)