# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 2020

@author: TianyuFu
"""

import math

def CloseClique(fix_node,dict_node):
    fix_node.sort()
    for i in range(1,len(fix_node)-1):
        # print("find",fix_node[i],end='')
        if fix_node[i] not in dict_node:
            return False
        for j in range(i+1,len(fix_node)):
            # print("-",fix_node[j])
            if fix_node[j] not in dict_node[fix_node[i]]:
                return False
    return True


