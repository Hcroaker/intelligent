from random import *
import random
import time
import math
import sys

#Returns an array of positions with 1 queen randomly placed in each "column"
def createBoard(n):
    positions = []
    for y in range(n):
        x = randint(0,n-1)
        positions.append(x)
    return positions

#Prints a string representation of the current state of the board.
def printBoard(n, newBoard):
    Matrix = [[0 for row in range(n)] for col in range(n)]
    for x in range(n):
        Matrix[newBoard[x]][x]=1

    print('\n'.join([''.join(['{:4}'.format(num) for num in x])
      for x in Matrix]))

#Function for difference in two numbers
def diff(n1, n2):
    return abs(n1-n2)

#Checks if two posisions collide.
def doCollide(pos1, pos2):
    if(pos1[0]==pos2[0]): #In the same row
        return True
    elif(diff(pos1[0], pos2[0]) == diff(pos1[1], pos2[1])): #Check if they're diagonol, diff between row1 & row 2 == diff col1 & col2
        return True
    else:
        return False

#Returns the cost of a given state
def cost(n, newBoard):
    collisions = 0
    #print(board)

    #For each queen, check how many collisions to the right
    for index in range(n):
        for i in range(index+1,n):

            paired = ((newBoard[index], index), (newBoard[i], i))
            # print("Do the queens", paired, "Collide?")
            if(doCollide((newBoard[index], index), (newBoard[i], i))):
                # print("Yes")
                collisions += 1

    # print(collisions)
    return collisions

#Probability function for simulated annealing
def prob(e, e1, T):
    return math.exp(-(e1-e)/T)

def findTwoFittest(population, populationSize, n):
    lowest = 0;
    lengthOfUnsorted = populationSize

    for index in range(2):

        for i in range(lengthOfUnsorted):
            c1 = cost(n,population[i])
            c2 = cost(n,population[lowest])
            if(c1<c2):
                lowest = i

        temp = population[lengthOfUnsorted-1];
        population[lengthOfUnsorted-1] = population[lowest]
        population[lowest] = temp

        lengthOfUnsorted = lengthOfUnsorted - 1
        lowest = 0

    population = population[-3:populationSize]

    return population;


def repoduce(x,y,n):

    crossOverPoint = randint(0,n-1)
    temp = list(x[0:crossOverPoint])
    x[0:crossOverPoint] = y[0:crossOverPoint]
    y[0:crossOverPoint] = temp

    c1 = cost(n,x)
    c2 = cost(n,y)

    if(c1>=c2):
        return (x,c1)
    else:
        return (y,c2)

def generatePopulation(n,k):
    population = []
    for i in range(k):
        population.append(createBoard(n))

    return population


def geneticAlgorithm(population, populationSize, n):
    generations = 0;
    while True:
        newPopulation = []
        bestChild = 0
        bestCost = sys.maxsize
        if(bestCost!=sys.maxsize):
            newPopulation.append(bestChild)

        for i in range(populationSize-1):

            # population = findTwoFittest(population, populationSize, n)

            # populationSize -= 1
            x = population[randint(0,populationSize-2)];
            y = population[randint(0,populationSize-2)];

            repoduceReturn = repoduce(x,y,n)
            child = repoduceReturn[0]
            fitnessOfChild = repoduceReturn[1]

            if(fitnessOfChild<=bestCost):
                bestChild = list(child)
                bestCost = fitnessOfChild

            if(fitnessOfChild==0):
                return bestChild

            if(randint(0,100)<=40):
                child[randint(0,n-1)] = randint(0,n-1)

            newPopulation.append(child)

        population = list(newPopulation)
        generations += 1;

        #print(generations)
        #print(population);


#Simulated Annealing Algorithm
def simulatedAnnealing(n, board):

    newBoard = list(board)
    k=0
    T=4;
    # print(T)
    alpha = 0.995;

    while T>0.00001:
        k=0
        while(k<n/2):

            newBoardRand = list(newBoard)
            newBoardRand[randint(0,n-1)] = randint(0,n-1)
            # newRandomBoard[col]=randint(0,n-1);
            collisionAmount1 = int(cost(n, newBoard))
            collisionAmount2 = int(cost(n,newBoardRand))

            # print(collisionAmount2-collisionAmount1)

            if(collisionAmount2==0):
                print(T)
                return newBoardRand

            if(collisionAmount1==0):
                print(T)
                return newBoard

            if(collisionAmount2<=collisionAmount1):
                newBoard = list(newBoardRand)
                #print("Not prob")
            elif(prob(collisionAmount1, collisionAmount2, T) >= random.uniform(0, 1)):
                #print("Prob")
                newBoard = list(newBoardRand)


            k+=1
        T = alpha*T
    print(T)
    return newBoard

#Hill Climbing Algorithm
def hillClimbing(n, board):

    lowest = int((n*n)*n)
    lowestRow = 0
    newBoard = list(board)

    for col in range(n):
        for row in range(n):
            newBoard[col]=row;
            collisionAmount = int(cost(n, newBoard))
            if(collisionAmount<=lowest):
                lowest = collisionAmount
                lowestRow = row;
        newBoard[col]=lowestRow
    return newBoard

#Random Restart Algorithm
def hillClimbingRandomRestart(n, board):

    lowest = int((n*n)*n)
    lowestRow = 0
    newBoard = list(board)

    for col in range(n):
        for row in range(n):
            newBoard[col]=row;
            newRandomBoard = createBoard(n)
            collisionAmount1 = int(cost(n, newBoard))
            collisionAmount2 = int(cost(n,newRandomBoard))
            if(collisionAmount2<collisionAmount1):
                newBoard = newRandomBoard;
                #print("New random board")
                if(collisionAmount2<=lowest):
                    lowest = collisionAmount2
                    lowestRow = row;
            else:
                if(collisionAmount1<=lowest):
                    lowest = collisionAmount1
                    lowestRow = row;
        newBoard[col]=lowestRow
    return newBoard

def __init__():

    #Ask the user to input the size of the board
    print("Input the board size (n): ")
    n = int(input());



    #Ask the user which algorithm they would like to use?
    #(Hill Climbing, Hill Climbing Random Restart, Simulated Annealing, Genetic Algorithm, All of them)
    print("Which algorithm would you like to use? (h, hr, sa, ga, all)")
    command = input()

    if(command=="h"):
        print("_____Hill climbing Algorithm_____  ")
        print("\nInitial Sate: ")
        #Create a board
        board = createBoard(n)
        printBoard(n, board)
        print("Cost %s" % (cost(n,board)))
        hillClimb_start = time.time()

        newBoard = hillClimbing(n, board)
        i=0

        #Allow to iterate 100 times or until there is no more collisions
        while(i<100 and cost(n,newBoard)!=0):
            newBoard = hillClimbing(n, newBoard)
            i+=1

        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - hillClimb_start))

    elif(command=='hr'):
        print("_____Hill climbing Random Restart Algorithm_____  ")
        print("\nInitial Sate: ")
        randHillBoard = createBoard(n)
        printBoard(n, randHillBoard)
        print("Cost %s" % (cost(n,randHillBoard)))
        hillClimbRand_start = time.time()

        newBoard = hillClimbingRandomRestart(n, randHillBoard)
        i=0

        #Allow to iterate 100 times or until there is no more collisions
        while(i<100 and cost(n,newBoard)!=0):
            newBoard = hillClimbingRandomRestart(n, newBoard)
            i+=1

        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - hillClimbRand_start))

    elif(command=="sa"):
        print("_____Simulated Annealing Algorithm_____  ")
        print("\nInitial Sate: ")
        saBoard = createBoard(n)
        printBoard(n, saBoard)
        print("Cost %s" % (cost(n,saBoard)))
        saBoard_start = time.time()

        newBoard = simulatedAnnealing(n, saBoard)

        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - saBoard_start))

    elif(command=="ga"):
        print("_____Genetic Algorithm_____  ")
        print("\nInitial Sate: ")
        gaBoard = createBoard(n)
        printBoard(n, gaBoard)
        print("Cost %s" % (cost(n,gaBoard)))
        gaBoard_start = time.time()

        k=200
        population = generatePopulation(n, 200)

        newBoard = geneticAlgorithm(population, k, n)

        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - gaBoard_start))

    elif(command=="all"):
        #Create a board
        board = createBoard(n)

        #HILL CLIMBING
        print("_____Hill climbing Algorithm_____  ")
        print("\nInitial Sate: ")
        printBoard(n, board)
        print("Cost %s" % (cost(n,board)))
        hillClimb_start = time.time()

        newBoard = hillClimbing(n, board)
        i=0

        #Allow to iterate 100 times or until there is no more collisions
        while(i<100 and cost(n,newBoard)!=0):
            newBoard = hillClimbing(n, newBoard)
            i+=1

        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - hillClimb_start))


        #HILL CLIMBING RANDOM RESTART
        print("\n_____Hill climbing Random Restart Algorithm_____  ")
        print("\nInitial Sate: ")
        printBoard(n, board)
        print("Cost %s" % (cost(n,board)))
        hillClimbRand_start = time.time()

        newBoard2 = hillClimbingRandomRestart(n, board)
        i=0

        #Allow to iterate 100 times or until there is no more collisions
        while(i<100 and cost(n,newBoard2)!=0):
            newBoard = hillClimbingRandomRestart(n, newBoard2)
            i+=1

        print("\nNew State:")
        printBoard(n,newBoard2)
        print("Cost %s" % (cost(n,newBoard2)))
        print("Exection time = %s" % (time.time() - hillClimbRand_start))



        #SIMULATED ANNEALING
        print("\n_____Simulated Annealing Algorithm_____  ")
        print("\nInitial Sate: ")
        printBoard(n, board)
        print("Cost %s" % (cost(n,board)))
        saBoard_start = time.time()

        newBoard3 = simulatedAnnealing(n, board)

        print("\nNew State:")
        printBoard(n,newBoard3)
        print("Cost %s" % (cost(n,newBoard3)))

        print("Exection time = %s" % (time.time() - saBoard_start))



        #GENETIC ALGORITHM
        print("\n_____Genetic Algorithm_____  ")
        print("\nInitial Sate: ")
        printBoard(n, board)
        print("Cost %s" % (cost(n,board)))
        gaBoard_start = time.time()

        k=200
        population = generatePopulation(n, 200)

        newBoard4 = geneticAlgorithm(population, k, n)

        print("\nNew State:")
        printBoard(n,newBoard4)
        print("Cost %s" % (cost(n,newBoard4)))

        print("Exection time = %s" % (time.time() - gaBoard_start))





__init__()
