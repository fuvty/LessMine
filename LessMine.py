
# -*- coding: utf-8 -*-
"""
@author: TianyuFu
"""
import networkx as nx
import numpy as np
from tqdm import tqdm

from lib import *

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
    max_comb = max(len(v) for v in adj_di_dict.values())
    comb_table = PreComb(num_query_n, max_comb)
    # comb_table = PreComb(num_query_n,int((2*len(target))**0.5) )

    total_count = 0.0
    avg_count = []
    # for i in range(num_estimator):
    for i in tqdm(range(num_estimator)):
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

    # ONLY SUPPORT CLIQUE NOW
    num_query_n = query.number_of_nodes()
    if query.number_of_edges() != num_query_n*(num_query_n-1)/2:
        print('SORRY: ONLY SUPPORT CLIQUE NOW, building more')
        raise NotImplementedError
    avg_count = LessMine_core(edge_list, adj_di_dict, query, emb_cmp_dict, num_estimator)

    return avg_count
    
def main():
    target_filename = './data/88234.txt'
    num_estimator = 10000

    query = nx.Graph()
    # query.add_edges_from([(0,1),(0,2),(1,2)]) # triangle
    # exact = 1612010 # triangle

    query.add_edges_from([(0,1),(0,2),(1,2),(0,3),(1,3),(2,3)]) # 4-clique
    exact = 30004668 # 4-clique

    query = RelabelNX(query)
    avg_count = LessMine_main(target_filename, query, num_estimator)
    num_pattern = avg_count[-1]
    print(num_pattern)
    print('error:',abs(num_pattern-exact)/exact*100,'%')
    
if __name__ == '__main__':
    main()