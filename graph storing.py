import numpy as np
import csv
import random
from networkx.generators.random_graphs import erdos_renyi_graph

def getGraph(v, i):
    #p=random.uniform(0.1, 0.3)
    g = erdos_renyi_graph(v, i) # erdos_renyi_graph produces a random graph with probability p. Setting it 0.5 means the edges are completely random 
    return g


graphCount = 30
gsize = 90
for i in [0.1, 0.2, 0.3, 0.4, 0.5]:
    with open('graphs'+str(graphCount)+'size'+str(gsize)+'EdgeDensity'+str(i)+'.csv', 'w', newline='') as graphCsv:
        writer = csv.writer(graphCsv)
        for count in range(graphCount):
            graph = getGraph(gsize, i)
            indexedGraph = [count]+list(graph.edges())
            print(indexedGraph)
            writer.writerow(indexedGraph)

