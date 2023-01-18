def mynetwork(source,target,weightdf,flag):
    # g = nx.Digraph()
    if flag==1:
        g = nx.from_pandas_edgelist(weightdf,'from_node','to_node', edge_attr=['weight(s)'])
        try:
            path = nx.shortest_path(g,source=source,target=target, weight='weight(s)')
            # print(path)
            length = path_length(g,path,'weight(s)')
            return [length, path]

        except nx.NetworkXNoPath:
            return None

    if flag==2:
        g = nx.from_pandas_edgelist(weightdf,'from_node','to_node', edge_attr=['mean_weight'])
    try:
        path = nx.shortest_path(g,source=source,target=target, weight='mean_weight')
        # print(path)
        length = path_length(g,path,'mean_weight')
        return [length, path]

    except nx.NetworkXNoPath:
        return None


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