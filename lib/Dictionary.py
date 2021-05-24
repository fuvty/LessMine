# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:40:44 2019

@author: WanZiqian
"""
# this function outputs 3 dictionaries of a graph, which is used to make the basic functions(SE,CSE,CC) run faster
#@profile
def Dictionary(edge_list): 
    
    # dict_loc = dict() #document the max number of edge related to the first node of the edge_list
    dict_node = dict() #document the neighbor nodes of the first node in the edge_list
    # dict_edge = dict() #document the neighbor edges of each node in the edge_list
    # dict_edge_in = dict()
    # dict_edge_out = dict()
    
    '''
    #dict_loc    
    dict_loc[edge_list[0][0]] = [0]
    for i in range(0,len(edge_list)-1): 
        if not edge_list[i][0] == edge_list[i+1][0]:
            dict_loc[edge_list[i][0]].append(i)
            dict_loc[edge_list[i+1][0]] = [i+1]
    if not edge_list[-1][0] == edge_list[-2][0]:
        dict_loc[edge_list[-1][0]].append(len(edge_list)-1)
    '''

    #dict_node    
    for i in range(len(edge_list)):
        if edge_list[i][0] not in dict_node:
            dict_node[edge_list[i][0]] = [edge_list[i][1]]
        else:
            dict_node[edge_list[i][0]].extend([edge_list[i][1]])

    '''
    #dict_edge
    for i in range(len(edge_list)):    
        if edge_list[i][0] not in dict_edge:
            dict_edge[edge_list[i][0]] = [i]
        else:
            dict_edge[edge_list[i][0]].extend([i])
        if edge_list[i][1] not in dict_edge:
            dict_edge[edge_list[i][1]] = [i]
        else:
            dict_edge[edge_list[i][1]].extend([i])
    
    for i in range(len(edge_list)):
        if edge_list[i][0] not in dict_edge_out:
            dict_edge_out[edge_list[i][0]] = [i]
        else:
            dict_edge_out[edge_list[i][0]].extend([i])
        if edge_list[i][1] not in dict_edge_in:
            dict_edge_in[edge_list[i][1]] = [i]
        else:
            dict_edge_in[edge_list[i][1]].extend([i])
    '''
    max_deg = 0
    for a in dict_edge:
        if len(dict_edge[a])>max_deg:
            max_deg = len(dict_edge[a])
            
    return dict_node


    