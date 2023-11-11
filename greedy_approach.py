#The most common greedy algorithm for dominating set is to repeatedly selecting a vertex with the maximum number of adjacent vertices that are not selected and that are not connected to any vertices selected (not dominated) so far until all vertices are dominated.
import csv

def makeAdjList(graph, size):
    adjlist = [[] for i in range(size)]
    for i in graph:
        adjlist[i[0]].append(i[1])
        adjlist[i[1]].append(i[0])
    return adjlist

def checkIsCovered(inc):
    flag = False
    for i in inc:
        if i == 0:
            flag = True
            break
    return flag


def minDomSet(graph, gsize):
    adjlist = makeAdjList(graph, gsize)
    L = len(adjlist)
    inc = [0]*L
    deg = [0]*L
    soln = []
    for i in range(L):
        deg[i]=len(adjlist[i])

    while checkIsCovered(inc):
        
        large = 0
        for i in range(L):
            if deg[large] < deg[i]:
                large = i
        inc[large]=1
        deg[large]=-1
        for i in adjlist[large]:
            deg[i]=-1
            inc[i]=1
        soln.append(large)
    return soln       

def getInput(gsize, gnumber):
    graphs = []
    with open('graphs'+str(gnumber)+'size'+str(gsize)+'.csv', newline='') as graphfile:
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


def getInput(gsize, gnumber, edgeDensity):
    graphs = []
    with open('graphs30size'+str(gsize)+'EdgeDensity'+str(edgeDensity)+'.csv', newline='') as graphfile:
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



gsize = 25
graphNumber = 30
EdgeDensity = [0.1, 0.2, 0.3, 0.4, 0.5]
for ed in EdgeDensity:
    graphs = getInput(gsize, graphNumber, ed)

    total = 0

    for graph in graphs:
        soln = minDomSet(graph, gsize)
        total+= len(soln)
        print(len(soln))
    
    avg = total/graphNumber
    print('edge density:'+str(ed)+' average is:')
    print(avg)


'''def getAvg(graphs,gsize,gnumber):
    total = 0
    for graph in graphs:
        soln = minDomSet(graph, gsize)
        total+= len(soln)

    avg = total/gnumber
    return avg'''

    


