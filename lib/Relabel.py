# Relabel nodes to start from 0

import networkx as nx

def RelabelEdgeListMap(node_set:set, edge_list:list):
    '''
    return the mapping of vertices of edge_list
    '''
    node_list = list(node_set)
    node_list.sort()
    map = dict(zip(node_list, [i for i in range(len(node_set))]))
    return map

def RelabelEdgeList(node_set:set, edge_list:list):
    '''
    return the reordered edge_list
    '''
    node_list = list(node_set)
    node_list.sort()
    map = dict(zip(node_list, [i for i in range(len(node_set))]))
    return [(map[e[0]],map[e[1]]) for e in edge_list]

def RelabelNX(graph: nx.Graph):
    edge_list = [(min(e),max(e)) for e in graph.edges]
    edge_list.sort()
    graph = nx.Graph()
    graph.add_edges_from(edge_list)
    return graph