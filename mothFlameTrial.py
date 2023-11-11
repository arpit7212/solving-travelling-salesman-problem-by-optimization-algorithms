import random_approach
import getGraphs
import genetic_algorithm
from random import random
from random import choice
import numpy as np


#initialize constants
graphSize = 30
graphCount = 9

maxIt = 100
maxFlames = 20

graphs = getGraphs.getInput(graphCount, graphSize)
graphs = graphs[:graphCount]

 
#for converting graph into 0-1
def convertTo01(g,gsize):
    p = [0]*gsize
    for i in g:
        p[i]=1
    return p

#cost function
def costFunction(position):
    return sum(position)




def distanceCalc(bFlame, mothPos, graphSize):
    distanceToFlame = 0
    for i in range(graphSize):
        if bFlame[i] == mothPos[i]:
            distanceToFlame = pow(-1,choice([0,1]))*random()
        else:
            distanceToFlame = bFlame[i] - mothPos[i]
    return distanceToFlame

def updateMothPos(distanceMul, distanceToFlames, adder, graphSize):
    temp = np.multiply(distanceMul, distanceToFlames)
    temp = [0 if (temp[i]+adder[i])<0.75 else 1 for i in range(graphSize)]
    return temp

def MFO(maxFlames, graphSize, maxIt, costFunction, graph):
# def MFO(nsa, dim, ub, lb, shift, max_iter, fobj):
    ''' Main function
    Parameters :
    - nsa : Number of Search Agents
    - dim : Dimension of Search Space
    - ub : Upper Bound
    - lb : Lower Bound
    - max_iter : Number of Iterations
    - fobj : Objective Function (Fitness Function)
    Returns :
    - bFlameScore : Best Flame Score
    - bFlamePos : Best Flame Position
    - ConvergenceCurve : Evolution of the best Flame Score on every iteration
    '''
    
    # Initialize the positions of moths
    
    mothPos = [convertTo01(random_approach.minDomSet(graph,graphSize), graphSize) for i in range(maxFlames)]
    mothPos = np.array(mothPos)
    convergenceCurve = np.zeros(shape=(maxIt))

    # print("Optimizing  \"" + fobj.__name__ + "\"")

    for iteration in range(maxIt):  # Main loop
        # Number of flames Eq. (3.14) in the paper
        flameNo = int(np.ceil(maxFlames-(iteration+1)*((maxFlames-1)/maxIt)))

        # Check if moths go out of the search space and bring them back
        

        # Calculate the fitness of moths
        mothFit = []
        for i in range(maxFlames):
            mothFit.append(costFunction(mothPos[i]))


        mothFit = np.array(mothFit)
        
        if iteration == 0:
            # Sort the first population of moths
            order = mothFit.argsort(axis=0)
            mothFit = mothFit[order]
            mothPos = mothPos[order, :]

            # Update the flames
            bFlames = np.copy(mothPos)
            bFlamesFit = np.copy(mothFit)

        else:
            # Sort the moths
            doublePop = np.vstack((bFlames, mothPos))
            doubleFit = np.hstack((bFlamesFit, mothFit))
            
            order = doubleFit.argsort(axis=0)
            doubleFit = doubleFit[order]
            doublePop = doublePop[order, :]


            # Update the flames
            bFlames = doublePop[:maxFlames, :]
            bFlamesFit = doubleFit[:maxFlames]
            
        # Update the position best flame obtained so far
        bFlameScore = bFlamesFit[0]
        bFlamesPos = bFlames[0, :]

        # a linearly dicreases from -1 to -2 to calculate t in Eq. (3.12)
        a = -1 + (iteration+1) * ((-1)/maxIt)

        b = 1
        t = (a-1)*np.random.rand(maxFlames, graphSize) + 1
        
        ''' Update the position of the moth with respect to its corresponding
        flame if the moth position is less than the number of flames
        calculated, otherwise update the position of the moth with respect
        to the last flame '''
        temp1 = bFlames[:flameNo, :]
        temp2 = bFlames[flameNo-1, :]*np.ones(shape=(maxFlames-flameNo, graphSize))
        temp2 = np.vstack((temp1, temp2))

        

        # D in Eq. (3.13)
        
        distanceToFlames = [0]*graphSize
        for i in range(maxFlames):
            distanceToFlames[i] = distanceCalc(temp2[i], mothPos[i], graphSize)

        distanceToFlames = np.array(distanceToFlames)

        
        distanceMultiplier = np.exp(b*t)*np.cos(t*2*np.pi)
        
        for i in range(len(mothPos)):
            mothPos[i] = updateMothPos(distanceMultiplier[i], distanceToFlames[i], temp2[i], graphSize)
            mothPos[i] = genetic_algorithm.completeP(mothPos[i], graph, graphSize)
            mothPos[i] = genetic_algorithm.redundantRemoval(mothPos[i], graph, graphSize)
        

        convergenceCurve[iteration] = bFlameScore

    return bFlameScore, bFlamesPos, convergenceCurve


total=0
for graph in graphs:
    bFlameScore, bFlamesPos, convergenceCurve = MFO(maxFlames, graphSize, maxIt, costFunction, graph)
    print(bFlameScore)
    total+=bFlameScore

total = total/graphCount
print(total)
