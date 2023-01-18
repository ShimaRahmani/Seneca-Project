def mynetwork(source,target,weightdf):
    # g = nx.Digraph()
    g = nx.from_pandas_edgelist(weightdf,'from_node','to_node', edge_attr=['Length(m)(poly)'])
    # check full connectivity of edges
    # for i in EdgeIndex_unique:
    #     if g.has_edge(i,)==0:
    #        g.add_edge(ind,ind+1)
    # a = subgraph_shortpath(g, g.nodes())
    try:
        path = nx.shortest_path(g,source=source,target=target, weight='Length(m)(poly)')
        # print(path)
        length = path_length(g,path,'Length(m)(poly)')
        return [length, path]

    except nx.NetworkXNoPath:
        return None

    # for path in nx.shortest_simple_paths(g, source=source,target=target, weight='Length(m)(poly)'):
    #     print(path, len(path)) # number of edges
    #     print(path, path_length(g,path,'Length(m)(poly)')) # estimated time
    #     print("--------------")



def subgraph_shortpath(G, node):
    """ unidirection, O(1)"""
    nodes = nx.single_source_shortest_path(G,node).keys()
    return G.subgraph(nodes)

def path_length(g, nodes, weight):
    w = 0
    for ind,nd in enumerate(nodes[1:]):
        prev = nodes[ind]
        w += g[prev][nd][weight]
    return w

import networkx as nx