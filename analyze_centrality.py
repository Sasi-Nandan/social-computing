import os
import snap
import time

def get_overlaps(snap_dict, filename):
    snap_list = []
    c = 0
    for i in snap_dict:
        if c >= 100:
            break

        c += 1
        snap_list.append(i)

    file_list=[]
    with open(os.path.join("centralities", filename), "r") as f:
        for i in range(100):
            s = f.readline()
            node_ind = int(s.split()[0])

            file_list.append(node_ind)

    intersection_set = set.intersection(set(snap_list), set(file_list))
    return len(intersection_set)



def analyze(graph, file1, file2, file3):
    ####### closeness centrality #######
    t0 = time.time()
    closeness_dict = {}

    for node in graph.Nodes():
        closeness_dict[node.GetId()] = snap.GetClosenessCentr(graph,node.GetId())

    closeness_dict = {k:v for k,v in sorted(closeness_dict.items(), key=lambda item: item[1], reverse=True)}

    ans1 = get_overlaps(closeness_dict, file1)

    ######## betweenness centrality #######
    vertices_bt_dict = snap.TIntFltH()
    edge_bt_dict = snap.TIntPrFltH()

    snap.GetBetweennessCentr(graph, vertices_bt_dict, edge_bt_dict, 0.8)

    betweenness_dict = {}
    for node in graph.Nodes():
        betweenness_dict[node.GetId()] = vertices_bt_dict[node.GetId()]

    betweenness_dict = {k:v for k,v in sorted(betweenness_dict.items(), key=lambda item: item[1], reverse=True)}

    ans2 = get_overlaps(betweenness_dict, file2)

    ########## PageRank #############
    pr_dict = snap.TIntFltH()

    snap.GetPageRank(graph, pr_dict, 0.8)

    pagerank = {}
    for node in graph.Nodes():
        pagerank[node.GetId()] = pr_dict[node.GetId()]

    pagerank = {k:v for k,v in sorted(pagerank.items(), key=lambda item: item[1], reverse=True)}

    ans3 = get_overlaps(pagerank, file3)

    print("#overlaps for Closeness Centrality: {}".format(ans1))
    print("#overlaps for Betweenness Centrality: {}".format(ans2))
    print("#overlaps for PageRank Centrality: {}".format(ans3))




if __name__ == "__main__":
    graph = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt")

    analyze(graph, "closeness.txt", "betweenness.txt", "pagerank.txt")