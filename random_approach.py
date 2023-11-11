
import random
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
    soln = []

    vlist = list(range(0,gsize))
    while checkIsCovered(inc):
        asoln = random.choice(vlist)
        vlist.remove(asoln)
        inc[asoln]=1
        for i in adjlist[asoln]:
            inc[i]=1
        soln.append(asoln)
    return soln 



def getInput(gnumber, gsize, edgeDensity):
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

def getAvg(graphs,gsize,gnumber):
    total = 0
    for graph in graphs:
        soln = minDomSet(graph, gsize)
        total+= len(soln)

    avg = total/gnumber
    return avg

gsize = 25
gnumber = 30

EdgeDensity = [0.1,0.2,0.3,0.4,0.5]

for ed in EdgeDensity:
    graphs = getInput(gnumber, gsize, ed)
    #for graph in graphs:
        #print(minDomSet(graph, gsize))
    print('for ed '+str(ed)+' avg is:' , getAvg(graphs, gsize, gnumber))


