import sys
import os
import statistics
import snap
Rnd = snap.TRnd(42)
Rnd.Randomize()

def printWithOutNewLine(line, value):
    print(line, end = " ")
    print(value)

def main():
    
    parentDir = os.getcwd()
    os.chdir(parentDir+"/subgraphs")
    sub_graph = snap.LoadEdgeList(snap.PUNGraph, sys.argv[1], 0, 1)
    subGraphName = sys.argv[1].split(".")[0]
    os.chdir(parentDir)

    #### 1 ########
    node_count = 0
    for node in sub_graph.Nodes():
        node_count = node_count+1

    printWithOutNewLine("Number of nodes:", node_count)
    printWithOutNewLine("Number of edges:", snap.CntUniqBiDirEdges(sub_graph))

    #### 2 ########
    printWithOutNewLine("Number of nodes with degree=7:", snap.CntDegNodes(sub_graph, 7))

    rndMaxDegNId = snap.GetMxDegNId(sub_graph)
    nodeDegPairs = snap.TIntPrV()
    snap.GetNodeInDegV(sub_graph, nodeDegPairs)
    maxDegVal = 0

    for pair in nodeDegPairs:
        if ( pair.GetVal1() == rndMaxDegNId ):
            maxDegVal = pair.GetVal2()
            break

    maxDegNodes = []
    for pair in nodeDegPairs:
        if( pair.GetVal2() == maxDegVal ):
            maxDegNodes.append(pair.GetVal1())

    print("Node id(s) with highest degree:", end =" ")
    print(*maxDegNodes, sep=',')

    #### 3 ########
    sampledFullDiam = []
    sampledFullDiam.append(snap.GetBfsFullDiam(sub_graph, 10, False))
    sampledFullDiam.append(snap.GetBfsFullDiam(sub_graph, 100, False))
    sampledFullDiam.append(snap.GetBfsFullDiam(sub_graph, 1000, False))
    
    sampledFullDiamStats = []
    sampledFullDiamStats.append( round( statistics.mean(sampledFullDiam), 4 ) )
    sampledFullDiamStats.append( round( statistics.variance(sampledFullDiam), 4 ) )

    printWithOutNewLine("Approximate full diameter by sampling 10 nodes:", sampledFullDiam[0])
    printWithOutNewLine("Approximate full diameter by sampling 100 nodes:", sampledFullDiam[1])
    printWithOutNewLine("Approximate full diameter by sampling 1000 nodes:", sampledFullDiam[2])
    print("Approximate full diameter (mean and variance):", end =" ")
    print(*sampledFullDiamStats, sep=',')

    sampledEffDiam = []
    sampledEffDiam.append( round(snap.GetBfsEffDiam(sub_graph, 10, False), 4) )
    sampledEffDiam.append( round(snap.GetBfsEffDiam(sub_graph, 100, False), 4) )
    sampledEffDiam.append( round(snap.GetBfsEffDiam(sub_graph, 1000, False), 4) )
    
    sampledEffDiamStats = []
    sampledEffDiamStats.append( round( statistics.mean(sampledEffDiam), 4 ) )
    sampledEffDiamStats.append( round( statistics.variance(sampledEffDiam), 4 ) )

    printWithOutNewLine("Approximate effective diameter by sampling 10 nodes:", sampledEffDiam[0])
    printWithOutNewLine("Approximate effective diameter by sampling 100 nodes:", sampledEffDiam[1])
    printWithOutNewLine("Approximate effective diameter by sampling 1000 nodes:", sampledEffDiam[2])
    print("Approximate effective diameter (mean and variance):", end =" ")
    print(*sampledEffDiamStats, sep=',')

    #### 4 ########
    printWithOutNewLine("Fraction of nodes in largest connected component:", round( snap.GetMxSccSz(sub_graph), 4))

    bridgeEdges = snap.TIntPrV()
    snap.GetEdgeBridges(sub_graph, bridgeEdges)
    printWithOutNewLine("Number of edge bridges:", len(bridgeEdges))

    articulationPoints = snap.TIntV()
    snap.GetArtPoints(sub_graph, articulationPoints)
    printWithOutNewLine("Number of articulation points:", len(articulationPoints))

    #### 5 ########
    printWithOutNewLine("Average clustering coefficient:", round(snap.GetClustCf(sub_graph, -1), 4))

    printWithOutNewLine("Number of triads:", snap.GetTriads(sub_graph, -1))

    randomNodeId = sub_graph.GetRndNId()
    nodeIdCcfMap = snap.TIntFltH()
    snap.GetNodeClustCf(sub_graph, nodeIdCcfMap)
    
    print("Clustering coefficient of random node", end=" ")
    print(randomNodeId, end=": ")
    print( round(nodeIdCcfMap[randomNodeId], 4) )

    print("Number of triads random node", end=" ")
    print(randomNodeId, end=" participates: ")
    print( snap.GetNodeTriads(sub_graph, randomNodeId) )

    printWithOutNewLine("Number of edges that participate in at least one triad:", snap.GetTriadEdges(sub_graph, -1))

    #### plots ########
    if not os.path.isdir('plots'):
        os.makedirs('plots')

    
    os.chdir(parentDir+"/plots")
    plotsDir = os.getcwd()

    snap.PlotOutDegDistr(sub_graph, subGraphName, subGraphName + " Subgraph Degree Distribution")
    snap.PlotShortPathDistr(sub_graph, subGraphName, subGraphName + " Subgraph Shortest Path Lengths Distribution")
    snap.PlotSccDistr(sub_graph, subGraphName, subGraphName + " Subgraph Connected Components Size Distribution")
    snap.PlotClustCf(sub_graph, subGraphName, subGraphName + " Subgraph Clustering Coefficient Distribution")

    files = os.listdir(plotsDir)

    for file in files:
        if not file.endswith(".png"):
            os.remove(os.path.join(plotsDir, file))
    
    plots = os.listdir(plotsDir)
    filePrefix = "filename"
    for file in plots:
        nameSplit = file.split(".")
        if( len(nameSplit) == 2 ):
            continue
        if( nameSplit[0] == "ccf" ):
            filePrefix = "clustering_coeff_"
        elif( nameSplit[0] == "outDeg" ):
            filePrefix = "deg_dist_"
        elif( nameSplit[0] == "diam" ):
            filePrefix = "shortest_path_"
        elif( nameSplit[0] == "scc" ):
            filePrefix = "connected_comp_"
        
        os.rename(file, filePrefix+nameSplit[1]+"."+nameSplit[2])
    
    os.chdir(parentDir)

if __name__ == "__main__":
    main()