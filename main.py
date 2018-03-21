from random import *
import random
import time
import math

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

def repoduce(x,y):
    print("Hey")

def geneticAlgorithm(population, cost, n):
    newRandPop = createBoard(n)
    while cost(population)!=0:
        newPopulation = []
        splitNum = randint(0,n-1)
        x = population.splice(0)



#Simulated Annealing Algorithm
def simulatedAnnealing(n, board):

    newBoard = board
    k=0
    T=10000000;
    # print(T)
    alpha = 0.99;

    while T>0.00001:

        newRandomBoard = createBoard(n)
        # newRandomBoard[col]=randint(0,n-1);
        collisionAmount1 = int(cost(n, newBoard))
        collisionAmount2 = int(cost(n,newRandomBoard))
        if(collisionAmount2<=collisionAmount1):
            newBoard = newRandomBoard
            #print("Not prob")
        elif(prob(collisionAmount1, collisionAmount2, T) >= random.uniform(0, 1)):
            #print("Prob")
            newBoard = newRandomBoard

        T = alpha*T
        k+=1
    return newBoard

#Hill Climbing Algorithm
def hillClimbing(n, board):

    lowest = int((n*n)*n)
    lowestRow = 0
    newBoard = board

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
    newBoard = board

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

        newBoard = geneticAlgorithm(gaBoard, cost, n)

        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - gaBoard_start))




__init__()
