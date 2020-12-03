import snap
import time
import numpy as np 
import os


def output_closeness_centrality(graph, filename):
    num_nodes = graph.GetNodes()
    t0 = time.time()
    closeness_dict = {}

    for start in graph.Nodes():
        # get the sum of shortest path distances from start to all nodes by using snap algorithms
        sht_distance_htable = snap.TIntH()
        snap.GetShortPath(graph, start.GetId(), sht_distance_htable)

        sum_of_sht_paths = 0
        for item in sht_distance_htable:
            sum_of_sht_paths += sht_distance_htable[item]

        closeness_centrality_i = (num_nodes-1)/sum_of_sht_paths
        closeness_dict[start.GetId()] = closeness_centrality_i

    # sort the closeness centrality values in descending order
    closeness_dict = {k:v for k,v in sorted(closeness_dict.items(), key=lambda item: item[1], reverse=True)}

    with open(filename, "w") as f:
        for i in closeness_dict:
            f.write("{} {:.6f}\n".format(i, closeness_dict[i]))

    print("Time taken for calculation of closeness centrality = {:.6f}".format(time.time()-t0))


def is_converged(curr, prev):
    diff = curr-prev

    if sum(diff*diff) <= 1e-8:
        return True
    return False

def output_biased_pagerank(graph, filename):
    t0 = time.time()
    alpha = 0.8

    d = {}
    cnt = 0
    ind_to_node_mapping = {}
    node_to_ind_mapping = {} 
    i = 0

    for node in graph.Nodes():
        ind_to_node_mapping[i] = node.GetId()
        node_to_ind_mapping[node.GetId()] = i
        i += 1

        if node.GetId()%4 == 0:
            cnt += 1

    for node in graph.Nodes():
        if(node.GetId()%4 == 0):
            d[node.GetId()] = 1/cnt
        else:
            d[node.GetId()] = 0

    d_array = [d[k] for k in d]
    d_array = np.array(d_array)

    pagerank_array = [d[k] for k in d]
    pagerank_array = np.array(pagerank_array)

    while(True):
        prev = pagerank_array.copy()

        for i in range(len(pagerank_array)):
            u = ind_to_node_mapping[i]
            node_u = graph.GetNI(u)

            deg = node_u.GetDeg()

            t = 0
            for j in range(deg):
                v = node_u.GetNbrNId(j)
                node_v = graph.GetNI(v)
                out_deg = node_v.GetDeg()
                ind_v = node_to_ind_mapping[v]

                t += pagerank_array[ind_v]/out_deg

            pagerank_array[i] = alpha*t + (1-alpha)*d_array[i]

        pagerank_array = pagerank_array/sum(pagerank_array)

        if is_converged(pagerank_array, prev):
            break

    pagerank = {}
    for i in range(len(pagerank_array)):
        node_id = ind_to_node_mapping[i]
        pagerank[node_id] = pagerank_array[i]

    pagerank = {k:v for k,v in sorted(pagerank.items(), key=lambda item: item[1], reverse=True)}

    with open(filename, "w") as f:
        for i in pagerank:
            f.write("{} {:.6f}\n".format(i, pagerank[i]))

    print("Time taken for execution of PageRank = {:.6f}".format(time.time()-t0))


def output_betweenness_centrality(graph, filename):
    # Brandes' algorithm is used
    t0 = time.time()

    n = graph.GetNodes()
    normalization_factor = (n-1)*(n-2)

    betweenness_dict = {}
    for node in graph.Nodes():
        betweenness_dict[node.GetId()] = 0

    for start in graph.Nodes():
        S = []
        Q = []

        P = {}
        sigma = {}
        d = {}
        delta = {}
        for node in graph.Nodes():
            P[node.GetId()] = []
            sigma[node.GetId()] = 0
            d[node.GetId()] = -1
            delta[node.GetId()] = 0

        sigma[start.GetId()] = 1
        d[start.GetId()] = 0

        Q.append(start.GetId())
        while(len(Q) > 0):
            v = Q.pop(0)
            S.append(v)

            # find the iterator corresponding to the current node
            # and its degree to iterate over its neighbors
            node_v = graph.GetNI(v)
            deg = node_v.GetDeg()

            for i in range(deg):
                w = node_v.GetNbrNId(i)

                if d[w] < 0:
                    Q.append(w)
                    d[w] = d[v] + 1

                if d[w] == d[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)

        while len(S) > 0:
            w = S.pop()

            for v in P[w]:
                delta[v] += sigma[v]*(1+delta[w])/sigma[w]

            if w != start.GetId():
                betweenness_dict[w] += delta[w]

        
    betweenness_dict = {k:v for k,v in sorted(betweenness_dict.items(), key=lambda item: item[1], reverse=True)}

    with open(filename, "w") as f:
        for i in betweenness_dict:
            f.write("{} {:.6f}\n".format(i, betweenness_dict[i]/normalization_factor))

    print("Time taken for execution of Brandes' algorithm for betweenness centrality = {:.6f}".format(time.time()-t0))





if __name__ == "__main__":
    graph = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined.txt")

    directory = "centralities"
    if not os.path.exists(directory):
        os.mkdir(directory)

    output_closeness_centrality(graph, os.path.join(directory,"closeness.txt"))
    output_biased_pagerank(graph, os.path.join(directory,"pagerank.txt"))
    output_betweenness_centrality(graph, os.path.join(directory,"betweenness.txt"))