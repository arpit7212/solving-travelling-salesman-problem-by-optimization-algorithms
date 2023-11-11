import random_approach
import getGraphs
import genetic_algorithm
from random import random
from random import choice

graphSize = 50
maxIt = 100
npop = 20
w=1
c1=0.5
c2=0.5
graphCount = 30


graphs = getGraphs.getInput(graphCount, graphSize)

class Particle:
    position = [1]*graphSize
    velocity = [0]*graphSize
    cost = graphSize
    Bestposition = [1]*graphSize
    Bestcost = graphSize


class GlobalBest:
    position = [1]*graphSize
    cost = graphSize

def convertTo01(g,gsize):
    p = [0]*gsize
    for i in g:
        p[i]=1
    return p

def costFunction(position):
    #print(fitness)
    #print("cost function inside", position)
    return sum(position)

#calculating new velocity
def getNewVelocity(oldVelocity, particleBestPosition, currentPosition, GB):
    newVelocity = [0]*graphSize
    bestAndCurrentDiff = [0]*graphSize
    bestAndGlobalDiff = [0]*graphSize
    for i in range(graphSize):
        if particleBestPosition[i] == currentPosition[i]:
            bestAndCurrentDiff[i] = pow(-1,choice([0,1]))*random()
        else:
            bestAndCurrentDiff[i] = particleBestPosition[i] - currentPosition[i]

    for i in range(graphSize):
        if GB.position[i] == currentPosition[i]:
            bestAndGlobalDiff[i] = pow(-1,choice([0,1]))*random()
        else:
            bestAndGlobalDiff[i] = GB.position[i] - currentPosition[i]

    for i in range(graphSize):
        newVelocity[i] = w*oldVelocity[i] + c1*random()*bestAndCurrentDiff[i] + c2*random()*bestAndGlobalDiff[i]
        if newVelocity[i] < -2:
            newVelocity[i] = -2
        if newVelocity[i] > 1:
            newVelocity[i] = 1
    return newVelocity
 
#completing the position so that it satisfies MDS property
def completePos(pos):
    p=genetic_algorithm.completeP(pos,graph, graphSize)
    p=genetic_algorithm.redundantRemoval(p, graph, graphSize)

    return p

def startPSO(graph, w):
    # Initialization of particles
    particles = [Particle() for i in range(npop)]
    GB = GlobalBest()
    for i in range(npop):
        particles[i].position = convertTo01(random_approach.minDomSet(graph,graphSize), graphSize)
        particles[i].cost = costFunction(particles[i].position)  
        
        #print("initial",particles[i].cost)
        particles[i].velocity = [0]*graphSize
        particles[i].Bestposition = particles[i].position
        particles[i].Bestcost = particles[i].cost
        if particles[i].Bestcost < GB.cost:
            GB.position = particles[i].Bestposition
            GB.cost = particles[i].Bestcost
        


    # list to hold best cost value at each iterations
    #bestCosts = [graphSize]*maxIt
        
    #main loop
    for it in range(maxIt):
        for i in range(npop):
            particles[i].velocity = getNewVelocity(particles[i].velocity, particles[i].Bestposition, particles[i].position, GB)
            particles[i].position = [0 if (particles[i].position[j] + particles[i].velocity[j])<=0.75 else 1 for j in range(graphSize)]
            
            particles[i].position = genetic_algorithm.completeP(particles[i].position, graph, graphSize)
            particles[i].position = genetic_algorithm.redundantRemoval(particles[i].position, graph, graphSize)
            
            particles[i].cost = costFunction(particles[i].position)

            if particles[i].cost < particles[i].Bestcost:
                
                particles[i].Bestposition = particles[i].position
                particles[i].Bestcost = particles[i].cost
                
                if particles[i].Bestcost < GB.cost:
                    GB.position = particles[i].Bestposition
                    GB.cost = particles[i].Bestcost


    return GB

total=0
for graph in graphs:
    GB = startPSO(graph, 1)
    #print('global best position before',sum(GB.position))
    #total+=sum(genetic_algorithm.redundantRemoval(GB.position, graph, graphSize))
    total+=GB.cost
    print(GB.cost)
    #print("global best position",sum(genetic_algorithm.redundantRemoval(GB.position, graph, graphSize)))
print(total/graphCount)









    
