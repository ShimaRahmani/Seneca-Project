def network(h,df_specific,path):

    platform = re.findall(r'\d{3}[A-Z]+',path[0])
    date = re.findall(r'\d{4}\-\d{2}\-\d{2}',path[0])
    node_name_list=[]
    node_pos_list=[]
    edge_labels = []
    previous_EdgeID = [0000]
    j=0
    k=0
    for i, row in df_specific.iterrows():
        if previous_EdgeID[k]==row['EdgeIndex']:
            j +=1
            node_name = str(row['EdgeIndex'])+'_{0}'.format(j)+'_['+platform[0]+'_'+date[0]+']'
            node_pos = (row['latitude'],row['longitude'])
            previous_EdgeID.append(row['EdgeIndex'])
            k +=1
        else:
            if k<len(df_specific):
                j = 0
                node_name = str(row['EdgeIndex'])+'_{0}'.format(j)+'_['+platform[0]+'_'+date[0]+']'
                node_pos = (row['latitude'],row['longitude'])
                previous_EdgeID.append(row['EdgeIndex'])
                k +=1
            else:
                break
            
        
        node_name_list.append(node_name)
        node_pos_list.append(node_pos)
        edge_labels.append(row['EdgeIndex'])

    dic = dict(zip(node_name_list,node_pos_list))
    g = nx.Graph()
    g.add_nodes_from(node_name_list)
    fixed_layout = dic
    # add edge between pairs of nodes
    for ind,s in enumerate(node_name_list):
        if  ind < len(node_name_list)-1:
            if g.has_edge(node_name_list[ind],node_name_list[ind+1])==0:
                g.add_edge(node_name_list[ind],node_name_list[ind+1])

    # plt.figure(1)

    # nx.draw_networkx_nodes(g,pos=fixed_layout,alpha=0.1)
    # nx.draw(g,with_labels=True,pos=fixed_layout,alpha=0.1)
    # nx.draw_networkx_edges(g,pos=fixed_layout,edge_labels=edge_labels)
    # plt.show()
    # print(nx.info(g))


    # plt.figure(2)
    # nx.draw(h,with_labels=0,alpha=0.5)
    return g,dic
    






import re
import matplotlib.pyplot as plt
import networkx as nx
