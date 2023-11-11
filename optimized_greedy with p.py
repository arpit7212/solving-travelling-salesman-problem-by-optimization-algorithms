#The most common greedy algorithm for dominating set is to repeatedly selecting a vertex with the maximum number of adjacent vertices that are not selected and that are not connected to any vertices selected (not dominated) so far until all vertices are dominated. Here we do a little change - "we'll select a vertex v if it covers p number of vertices that are not already selected
import csv
from random import randrange

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


def Vchecker(i, inc, adjlist, p):
    count = 0
    for j in adjlist[i]:
        if inc[j] == 0:
            count+=1
    if p>count:
        return False
    else:
        return True

    

def minDomSet(graph, gsize, p):
    adjlist = makeAdjList(graph,gsize)
    L = len(adjlist)
    inc = [0]*L
    deg = [0]*L
    soln = []
    for i in range(L):
        deg[i]=len(adjlist[i])

    while checkIsCovered(inc):
        large = 0
        while large<gsize:
            if inc[large] == 0:
                break
            else:
                large+=1
        #large = randrange(0, gsize)

        for i in range(L):
            if deg[large] < deg[i] and Vchecker(i, inc, adjlist, p):
                large = i
        
        inc[large]=1
        deg[large]=0
        for i in adjlist[large]:
            inc[i]=1
        soln.append(large)
    return soln

'''def redundantRemoval(soln, gsize, adjlist):
    vRepeated = [0]*gsize
    for v in soln:
        vRepeated[v] += 1
        for i in adjlist[v]:
            vRepeated[i] += 1
    j=0
    while j < len(soln):
        flag = True
        if( vRepeated[j]-1 == 0 ):
            flag = False
        if(flag):
            for a in adjlist[j]:
                if( vRepeated[a]-1 == 0 ):
                    flag = False
                    break
        if(flag):
            soln.pop(j)
            vRepeated[j]-=1
            for a in adjlist[j]:
                vRepeated[a]-=1
        else:
            j+=1
    
    return soln'''


def getInput(Graphnumber, gsize):
    graphs = []
    with open('../../used_graphs/testing_p_graphs/graphs'+str(Graphnumber)+'size'+str(gsize)+'.csv', newline='') as graphfile:
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








Graphnumber = 30
#gsize = 20
gsizes = [100,120,140,160,180]
ps =[1, 2, 3, 4, 5, 6]
with open('graphsAverageOutput_new.csv', 'w', newline='') as graphAverageOutputFile:
    writer = csv.writer(graphAverageOutputFile)
    for p in ps:
        graphAverageOutput = []
        for gsize in gsizes:
            graphs = getInput(Graphnumber, gsize)
            
            #with open('graphs'+str(Graphnumber)+'size'+str(gsize)+'p'+str(p)+'result.csv', 'w', newline='') as graphCsv:
            #writer = csv.writer(graphCsv)
            i=0
            total = 0
            for graph in graphs:
                    
                soln = minDomSet(graph,gsize,p)
                    
                #print(len(soln))
                    
                #writer.writerow([i,len(soln)])
                total+= len(soln)
                i+=1
                
            avg = total/Graphnumber
            #writer.writerow(['average',avg])
            graphAverageOutput.append(avg)
            print(p,gsize,avg)
        
        writer.writerow(graphAverageOutput)
    
'''def getAvg(graphs,gsize,gnumber):
    total = 0
    for graph in graphs:
        soln = minDomSet(graph, gsize, 4)
        total+= len(soln)

    avg = total/gnumber
    return avg'''



'''graphs = getInput()
gsize = 30
numberOfGraphs = 30
print(getAvg(graphs,gsize,numberOfGraphs))'''


