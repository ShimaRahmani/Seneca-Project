def mynetwork(source,target,weightdf):
    # g = nx.Digraph()

    g = nx.from_pandas_edgelist(weightdf,'from_node','to_node', edge_attr=['weight(s)'])
    try:
        path = nx.shortest_path(g,source=source,target=target, weight='weight(s)')
        # print(path)
        time_tot = path_time(g,path,'weight(s)')
        #------------- add attributes from edge table to the graph ------------
        # pathGraph = nx.path_graph(path)
        # # read attributes from each edge
        # for ej in pathGraph.edges():
        #     print(ej, g.edges[ej[0],ej[1]])
        for i,row in weightdf.iterrows():
            g.add_edge(row[6],row[9], distance = row[3])
        distance_tot = path_distance(g,path, 'distance')
        #---------------------------------------------------
        return [time_tot, path, distance_tot]

    except nx.NetworkXNoPath:
        return None

def subgraph_shortpath(G, node):
    """ unidirection, O(1)"""
    nodes = nx.single_source_shortest_path(G,node).keys()
    return G.subgraph(nodes)

def path_time(g, nodes, weight):
    w = 0
    for ind,nd in enumerate(nodes[1:]):
        prev = nodes[ind]
        w += g[prev][nd][weight]
    return w

def path_distance(g, nodes, weight):
    w = 0
    for ind,nd in enumerate(nodes[1:]):
        prev = nodes[ind]
        w += g[prev][nd][weight]
    return w

import networkx as nx