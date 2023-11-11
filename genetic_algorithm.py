import csv
import greedy_approach
import optimized_greedy
import random_approach
import random
import getGraphs

def convertTo01(g,gsize):
    p = [0]*gsize
    for i in g:
        p[i]=1

    return p


def pickOne(population, psize, fitness):
    index = 0
    r = random.random()
    while r>0:
        r = r - fitness[index]
        index+=1
    index-=1
    #print(index)
    return population[index]


def completeP(p,graph, gsize):
    adj = optimized_greedy.makeAdjList(graph,gsize)
    L = len(adj)
    inc = [0]*L
    deg = [0]*L
    for i in range(L):
        deg[i]=len(adj[i])
    #print(p)
    for i in range(len(p)):
        if p[i]==1:
            for j in adj[i]:
                inc[j]=1
            deg[i] = 0
            inc[i] = 1

    while optimized_greedy.checkIsCovered(inc):
        while True:
            large = random.randrange(0,gsize)
            if inc[large]==0:
                break

        for i in range(L):
            if deg[large] < deg[i] and optimized_greedy.Vchecker(i, inc, adj, 4):
                large = i

        inc[large]=1
        deg[large]=0
        for i in adj[large]:
            inc[i]=1

        p[large]=1
    
    return p


def redundantRemoval(p, graph, gsize):
    adjlist = optimized_greedy.makeAdjList(graph,gsize)

    dcount = [0]*gsize
    for v in range(gsize):
        if p[v]==1:
            dcount[v]+=1
            for i in adjlist[v]:
                dcount[i]+=1

    for i in range(gsize):
        if p[i]==1:
            flag=True
            if dcount[i]>1:
                for j in adjlist[i]:
                    if dcount[j]==1:
                        flag=False
            else:
                flag=False
                

            if flag==True:
                for j in adjlist[i]:
                    dcount[j]-=1

                dcount[i]-=1

                p[i]=0

    return p
    

def crossoverMutation(population, fitness, graph, gsize, psize):
    #print(len(population))
    for p in range(len(population)):
        pick1 = pickOne(population, psize, fitness)
        pick2 = pickOne(population, psize, fitness)
        i = random.randint(0, len(pick1)-1)
        newp = pick1[:i]+pick2[i:]
        #print(p)
        #print(newp)
        i = random.randint(0,len(pick1)-1)
        if newp[i] == 1:
            newp[i]=0
        else:
            newp[i]=1

        '''union=[0]*gsize
        for i in range(gsize):
            if pick1[i]==1 or pick2[i]==1:
                union[i]=1

        newp = somethingnew(newp, graph)'''
        newp = completeP(newp, graph, gsize)
        newp = redundantRemoval(newp, graph, gsize)
        population[p]=newp
        

    return population

    
def InitializePopulation(graph, gsize, psize):
    population = [[]]*psize
    population[0] = greedy_approach.minDomSet(graph, gsize)
    population[1] = optimized_greedy.minDomSet(graph, gsize, 4)
    

    #for i in range(2,psize):
    #for i in range(psize):
    for i in range(2,psize):
        population[i] = random_approach.minDomSet(graph,gsize)

    for i in range(psize):
         population[i] = convertTo01(population[i], gsize)

    #print("initial population")
    #print(population[1])
    return population


def normalizeFitness(fitness, fsize):
    s = sum(fitness)
    for i in range(fsize):
        fitness[i] = fitness[i]/s

    #print(fitness)
    return fitness

def calculateFitness(population, psize):
    fitness = [0]*psize
    for g in range(psize):
        fitness[g] = (1/sum(population[g]))
        
    #print(fitness)
    return fitness


def startGA(graph, gsize, psize, generationLimit):
    population = InitializePopulation(graph, gsize, psize)
    #print(population)
    #fitness
    fbest = 0
    pbest = []
    for _ in range(generationLimit):
        fitness = calculateFitness(population, psize)
        for f in range(psize):
            if fitness[f] > fbest:
                fbest = fitness[f]
                pbest = population[f]
        fitness = normalizeFitness(fitness, psize)
        population = crossoverMutation(population, fitness, graph, gsize, psize)
        #print(population)

    return pbest

def getAvg(gsize, numberOfGraphs, psize, generationLimit):
    
    graphs = getGraphs.getInput(numberOfGraphs,gsize)



    #print("final population")
    solutions=[]
    total=0
    for graph in graphs:
        s = startGA(graph, gsize, psize, generationLimit)
        print(sum(s))
        total+=sum(s)
    avg = total/30
        

    print(avg)



'''psize=20
generationLimit = 100
numberOfGraphs = 30
gsize = 50

getAvg(gsize, numberOfGraphs, psize, generationLimit)'''



