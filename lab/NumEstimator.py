#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:23:39 2020

@author: futianyu
"""
# \alpha = constant

def NumEstimator(alpha,num_edge,max_degree,num_clique,G):
    return int(alpha*num_edge*(max_degree**(num_clique-2)) / G ) 
