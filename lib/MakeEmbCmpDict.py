import networkx as nx
import itertools

# given the queried graph, compute all the possible route of finding the graph
def MakeEmbCmpDict(query: nx.Graph):

    num_query_n = query.number_of_nodes()
    emb_cmp_dict = dict()
    for seq in itertools.permutations(range(num_query_n)):
        # print(seq)
        map = dict(zip([i for i in range(num_query_n)],seq))
        # print(map)
        iso_query = nx.relabel.relabel_nodes(query,map,copy=True)
        # print(iso_query.edges)
        edges = [(min(e),max(e)) for e in iso_query.edges]
        edges.sort()
        emb_ns = set()
        key = list()
        for i,e in enumerate(edges):
            emb_ns.add(e[0])
            emb_ns.add(e[1])
            key.append(e)
            if len(emb_ns) == num_query_n:
                if i < num_query_n-1:
                    cmp = tuple(edges[i+1:])
                else:
                    cmp = tuple()
                break
        key = tuple(key)
        if key not in emb_cmp_dict.keys():
            emb_cmp_dict[key] = set()
        emb_cmp_dict[key].add(cmp)

    return emb_cmp_dict

if __name__ == '__main__':
    query = nx.Graph()
    query.add_edges_from([(1,0),(0,2),(1,2),(1,3)])
    emb_cmp_dict = MakeEmbCmpDict(query)
    print('num_plans',len(emb_cmp_dict))
    print(emb_cmp_dict)