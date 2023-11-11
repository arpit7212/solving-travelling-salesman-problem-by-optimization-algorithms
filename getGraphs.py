import csv

def getInput(graphsCount, graphSize):
    graphs = []
    with open('../used_graphs/graphs'+str(graphsCount)+'size'+str(graphSize)+'.csv', newline='') as graphfile:
        graphreader = csv.reader(graphfile)
        
        for row in graphreader:
            edges = []
            for i in row[1:]:
                comma = i.find(",")
                brack = i.find(")")
                v1 = int(i[1:comma])
                v2 = int(i[comma+1:brack])
                edges.append((v1,v2))
            graphs.append(edges)
    return graphs
