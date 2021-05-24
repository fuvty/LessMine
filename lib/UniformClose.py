# -*- coding: utf-8 -*-
"""
@author: TianyuFu
"""
# NOT DONE
import math

def CloseClique(fix_node_list, adj_di_dict):
    fix_node_list.sort()
    for i in range(1,len(fix_node_list)-1):
        # print("find",fix_node[i],end='')
        if fix_node_list[i] not in adj_di_dict:
            return False
        for j in range(i+1,len(fix_node_list)):
            # print("-",fix_node[j])
            if fix_node_list[j] not in adj_di_dict[fix_node_list[i]]:
                return False
    return True

def UniformClose(fix_node_list: list, adj_di_dict: dict, query_dict: dict):
    '''
    NOT FULLY IMPLEMENTED
    only support cliques now
    '''
    close = CloseClique(fix_node_list, adj_di_dict)
    return close
