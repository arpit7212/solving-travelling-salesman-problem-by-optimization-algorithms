import csv





def makeAdjList(graph, size):
    adjlist = [[] for i in range(size)]
    for i in graph:
        adjlist[i[0]].append(i[1])
        adjlist[i[1]].append(i[0])
    return adjlist

def latencyChecker(temp, adjList, gsize):
    inc = [0]*gsize
    for v in range(gsize):
        if temp[v] == 1:
            inc[v] = 1
            for i in adjList[v]:
                inc[i] = 1

    if inc == [1]*gsize:
        #print('soln mila')
        return True
    else:
        return False
 
def minDomSet(graph,gsize):
    adjList = makeAdjList(graph, gsize)
    ones = [1]*gsize
    asoln = [1]*gsize
    temp = [0]*gsize
    while temp != ones:
        
        if latencyChecker(temp, adjList, gsize):
            #print(temp)
            #print(asoln)
            if sum(temp) < sum(asoln):
                #print('les go')
                asoln = temp[:]

        temp[-1]+=1
        for i in range(gsize-1,-1,-1):
            if temp[i]==2:
                if i!=0:
                    temp[i-1]+=1
                temp[i]=0

    return asoln
            
        






def getInput(gsize):
    graphs = []
    with open('../used_graphs/graphs30size'+str(gsize)+'.csv', newline='') as graphfile:
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

def getInput(gsize, edgeDensity):
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

edgeDensity = [0.1, 0.2, 0.3, 0.4, 0.5]
for i in edgeDensity:
    gsize = 25
    graphs = getInput(gsize, i)
    total = 0

    Graphnumber = 30
    for graph in graphs:
        soln = minDomSet(graph,gsize)
        print(sum(soln))
        total+= sum(soln)
        
    avg = total/Graphnumber
    print('average of 30 graphs of size 30 each is')
    print(avg)
