from random import *
import random
import time
import math
import sys


## A Function to generate a random N-Queens board ##
#
# Eg [0,4,3,2,4,1] where n = 5.
# Only the positions need to stored as
# there is only 1 queen per column
#
def createBoard(n):
    # Input:
    # n: int = size of the board, specified by the user

    # Output:
    # positions: list = list of queens positions

    positions = []
    for y in range(n):

        #Set the position of a queen in a column to be a random number between 0 - n-1
        x = randint(0,n-1)
        positions.append(x)

    #Returns an array of positions with 1 queen randomly placed in each "column"
    return positions


## A function that prints a string representation of the current state of the board.
def printBoard(n, newBoard):

    # Input:
    # n: int = size of the board, specified by the user
    # newBoard: list = a list representing the positions of the queens on the board

    # Output:
    # none

    #Using List comprehension to initialize the board to all 0s
    Matrix = [[0 for row in range(n)] for col in range(n)]
    for x in range(n):
        #At the position of a queen insert a 1
        Matrix[newBoard[x]][x]=1

    #Using list comprehension format and print the board such that it is in the format of:
    # 0 1 0 0 0
    # 0 0 0 1 0
    # 1 0 0 0 0
    # 0 0 1 0 0
    # 0 0 0 0 1
    print('\n'.join([''.join(['{:4}'.format(number) for number in index])
      for index in Matrix]))


## A Function for calculating the difference in two numbers
def diff(n1, n2):

    # Input:
    # n1: int = number 1
    # n2: int = number 2

    # Output:
    # int = difference between two numbers

    return abs(n1-n2)


## A function to check if two queen positions collide
def doCollide(pos1, pos2):

    # Input:
    # pos1: int tuple = two numbers representing the position of a queen (row,col)
    # pos2: int tuple = two numbers representing the position of a queen (row,col)

    # Output:
    # boolean = returns true if the two queens collide, else returns false

    #Checks if the queens are in the same row
    if(pos1[0]==pos2[0]):
        return True
    #Check if they're colliding diagonolly, diff between row1 & row 2 is equal to the diff between col1 & col2
    elif(diff(pos1[0], pos2[0]) == diff(pos1[1], pos2[1])):
        return True
    #Return false if they do no collide
    else:
        return False


## A function to compute the cost of a given state
def cost(n, newBoard):

    # Input:
    # n: int = size of the board, specified by the user
    # newBoard: list = a list representing the positions of the queens on the board

    # Output:
    # collisions: int = the amount of collisions a given state has, the cost of a given state

    collisions = 0

    #For each queen, check how many collisions to the right of that queen
    for index in range(n):
        for i in range(index+1,n):

            #Pass two positions to the do collide function
            if(doCollide((newBoard[index], index), (newBoard[i], i))):
                #If they do collide then increase the collisions amount
                collisions += 1

    #Return the amount of collisions which in turn is the cost of a given state
    return collisions


## A functtion to compute the probability for simulated annealing
def prob(e, e1, T):

    # Input:
    # e: int = cost of 1 state
    # e1: int = cost of another state
    # T: decimal = current temperature

    # Output:
    # int = computed probability

    return math.exp(-(e1-e)/T)


## A function to reproduce a child given two parents in the genetic algorithm
def repoduce(x,y,n):

    # Input:
    # x: list = parent 1
    # y: list = parent 2
    # n: int = size of the board

    # Output:
    # tuple = (child, cost/fitness of the child)

     # Get a random crossover point
    crossOverPoint = randint(0,n-1)

    #Swap two subsections using a temporary variable
    temp = list(x[0:crossOverPoint])
    x[0:crossOverPoint] = y[0:crossOverPoint]
    y[0:crossOverPoint] = temp

    #Calculate the cost of both children
    c1 = cost(n,x)
    c2 = cost(n,y)

    #Return the fittest child
    if(c1<=c2):
        return (x,c1)
    else:
        return (y,c2)


## A function to generate an initial population of size k for the genetic algorithm
def generatePopulation(n,k):

    # Input:
    # n: int = size of the board
    # k: int = size of population

    # Output:
    # list = generated population

    population = []
    for i in range(k):
        population.append(createBoard(n))

    return list(population)


#Function to implement the genetic algorithm
def geneticAlgorithm(population, populationSize, n):

    # Input:
    # population: list = list of individuals in the created population
    # populationSize: int = the size of the population
    # n: int = size of the board

    # Output:
    # tuple = (fittest individual, cost of individual)

    generations = 0;
    bestChild = 0
    bestCost = sys.maxsize

    while True:

        newPopulation = list([])

        #Append the best child to the new population
        if(bestCost!=sys.maxsize):
            newPopulation.append(bestChild)

        #Creating a new population
        for i in range(populationSize-1):

            #Pick two random parents
            x = population[randint(0,populationSize-2)];
            y = population[randint(0,populationSize-2)];

            #Reproduce a child
            repoduceReturn = repoduce(x,y,n)
            child = list(repoduceReturn[0])         # The actual child list
            fitnessOfChild = repoduceReturn[1]      # The cost/fitness of the child calculated in the reproduce function

            # Check if the fitness of the new child is then the current best
            if(fitnessOfChild<=bestCost):
                bestChild = list(child)             # Set best child to the new child
                bestCost = fitnessOfChild           # Set best cost to the fitnessOfChild

            # Check if the fitness of the new child = 0
            if(fitnessOfChild==0):
                return list(bestChild),generations  # Return it and the amount of generations

            # Mutate with a chance of 60%
            if(randint(0,100)<=60):
                child[randint(0,n-1)] = randint(0,n-1) # The queen at a random position equals a random position
                if(cost(n,child)==0):                  # If this random mutation has reached the cost of 0 then
                    return child,generations           # return it and the amount of generations

            # Append the child to the new population
            newPopulation.append(child)

        # Make the population equal to the new population and increase the amount of generations
        population = list(newPopulation)
        generations += 1;
        # print(bestCost)


## A function to implement the simulated annealing algorithm
def simulatedAnnealing(n, board):

    # Input:
    # n: int = size of board
    # board: list = list representing positions of queens

    # Output:
    # newBoard: list = current state of the newBoard

    newBoard = list(board)

    # Set the initial parameters
    k=0
    T=4;
    alpha = 0.995;

    # While T gets very close to 0
    while T>0.00001:
        k=0

        # Repeat n/2 times
        while(k<n/2):

            # Choose a random neighbour
            newBoardRand = list(newBoard)
            newBoardRand[randint(0,n-1)] = randint(0,n-1)

            # Calculate the cost for the current position and the new position
            collisionAmount1 = int(cost(n, newBoard))
            collisionAmount2 = int(cost(n,newBoardRand))

            # If the current state has a cost of 0 then return the current state
            if(collisionAmount1==0):
                return newBoard

            # If the board with a new position has a cost of 0 then return newBoardRand
            if(collisionAmount2==0):
                return newBoardRand

            # Compare the two costs the two states newBoard and newBoardRand
            if(collisionAmount2<=collisionAmount1):
                # Set newBoard to newBoardRand if the cost of newBoardRand is better then newboard (current state)
                newBoard = list(newBoardRand)

            # If the new state isnt better, still take it with the probability computed in the prob function
            elif(prob(collisionAmount1, collisionAmount2, T) >= random.uniform(0, 1)):
                newBoard = list(newBoardRand)


            k+=1

        # Cool down the the temperature slowly
        T = alpha*T

    # Return the newBoard
    return newBoard

## A function to implement the hill clibing algorithm
def hillClimbing(n, board):

    # Input:
    # n: int = size of the board
    # board: list = list representing the positions of the queens

    # Output:
    # newBoard: list = current state of newBoard

    # Set the initial variables
    lowest = int((n*n)*n)
    lowestRow = 0
    newBoard = list(board)

    # Search through the entire board
    # Find the lowest cost position in each column, then move the queen to that lowest cost position
    for col in range(n):
        for row in range(n):
            newBoard[col]=row;
            # Checking the cost of each position in each column
            collisionAmount = int(cost(n, newBoard))
            if(collisionAmount<=lowest):
                lowest = collisionAmount
                # Set the lowest row if a better state has been found
                lowestRow = row;

        # Set the position of the queen to the lowest-cost row found
        newBoard[col]=lowestRow

    # Return the current state of the board
    return newBoard

## A function to implement the hill climbing random restart algorithm
def hillClimbingRandomRestart(n, board):

    # Input:
    # n: int = size of the board
    # board: list = list representing the positions of the queens

    # Output:
    # newBoard: list = computed probability

    # Set the initial variables
    lowest = int((n*n)*n)
    lowestRow = 0
    newBoard = list(board)

    # Search through the entire board for a better state
    for col in range(n):
        for row in range(n):

            newBoard[col]=row;

            # Create a new random board
            newRandomBoard = createBoard(n)

            # Get the costs of the current state and the new random board
            collisionAmount1 = int(cost(n, newBoard))
            collisionAmount2 = int(cost(n,newRandomBoard))

            # If the newRandomBoard's state is less then the current state
            if(collisionAmount2<collisionAmount1):
                newBoard = newRandomBoard;
            else:

                # If the current state is the lowest then set the lowest and lowestRow variables accordingly
                if(collisionAmount1<=lowest):
                    lowest = collisionAmount1
                    lowestRow = row;

        # Set the position of the queen to the lowest-cost row found
        newBoard[col]=lowestRow

    # Return the current state of the board
    return newBoard

## A function that initiates the program
def __init__():

    # Make sure the user enters the correct data types
    try:
        #Ask the user to input the size of the board
        print("Input the board size (n): ")
        n = int(input());

        #Ask the user which algorithm they would like to use?
        #(Hill Climbing, Hill Climbing Random Restart, Simulated Annealing, Genetic Algorithm, All of them)
        print("Which algorithm would you like to use? (h, hr, sa, ga, all)")
        command = input()

    except:
        print("You must input the correct values")
        return

    # Hill Climbing algorithm
    if(command=="h"):
        print("_____Hill climbing Algorithm_____  ")

        # Print the initial state and cost
        print("\nInitial Sate: ")
        # Create a board
        board = createBoard(n)
        printBoard(n, board)
        print("Cost %s" % (cost(n,board)))

        # Start a timer
        hillClimb_start = time.time()

        # Start the hillClimbing once
        newBoard = hillClimbing(n, board)
        i=0

        # Allow to iterate 100 times or until there is no more collisions
        while(i<100 and cost(n,newBoard)!=0):
            newBoard = hillClimbing(n, newBoard)
            i+=1

        # Print the new state,cost and the amount of time taken
        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - hillClimb_start))

    elif(command=='hr'):
        print("_____Hill climbing Random Restart Algorithm_____  ")

        # Print the initial state and cost
        print("\nInitial Sate: ")
        # Create a board
        randHillBoard = createBoard(n)
        printBoard(n, randHillBoard)
        print("Cost %s" % (cost(n,randHillBoard)))

        # Start a timer
        hillClimbRand_start = time.time()

        newBoard = hillClimbingRandomRestart(n, randHillBoard)
        i=0

        # Allow to iterate 100 times or until there is no more collisions
        while(i<100 and cost(n,newBoard)!=0):
            newBoard = hillClimbingRandomRestart(n, newBoard)
            i+=1

        # Print the new state,cost and the amount of time taken
        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - hillClimbRand_start))

    elif(command=="sa"):
        print("_____Simulated Annealing Algorithm_____  ")
        print("\nInitial Sate: ")
        # Create a board
        saBoard = createBoard(n)
        printBoard(n, saBoard)
        print("Cost %s" % (cost(n,saBoard)))

        # Start a timer
        saBoard_start = time.time()

        # Start SA Algorithm
        newBoard = simulatedAnnealing(n, saBoard)

        # Print the new state,cost and the amount of time taken
        print("\nNew State:")
        printBoard(n,newBoard)
        print("Cost %s" % (cost(n,newBoard)))

        print("Exection time = %s" % (time.time() - saBoard_start))

    elif(command=="ga"):
        print("_____Genetic Algorithm_____  ")
        print("\nInitial Sate: ")
        # Create a board
        gaBoard = createBoard(n)
        printBoard(n, gaBoard)
        print("Cost %s" % (cost(n,gaBoard)))

        # Start a timer
        gaBoard_start = time.time()

        # Population size
        k=200

        # Generation population
        population = generatePopulation(n, k)

        # Start GA
        newBoard = geneticAlgorithm(population, k, n)

        # Print the new state,cost,generations and the amount of time taken
        print("\nNew State:")
        printBoard(n,newBoard[0])
        print("Cost %s" % (cost(n,newBoard[0])))
        print("Generations: %s" % (newBoard[1]))

        print("Exection time = %s" % (time.time() - gaBoard_start))

    # Run all the algorthims on the same board
    elif(command=="all"):
        #Create a board
        board = createBoard(n)

        #HILL CLIMBING
        print("_____Hill climbing Algorithm_____  ")
        print("\nInitial Sate: ")
        printBoard(n, list(board))
        print("Cost %s" % (cost(n,list(board))))
        hillClimb_start = time.time()

        newBoard = hillClimbing(n, list(board))
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
        print("\n\n_____Hill climbing Random Restart Algorithm_____  ")
        print("\nInitial Sate: ")
        printBoard(n, list(board))
        print("Cost %s" % (cost(n,list(board))))
        hillClimbRand_start = time.time()

        newBoard2 = hillClimbingRandomRestart(n, list(board))
        i=0

        #Allow to iterate 100 times or until there is no more collisions
        while(i<100 and cost(n,newBoard2)!=0):
            newBoard2 = hillClimbingRandomRestart(n, newBoard2)
            i+=1

        print("\nNew State:")
        printBoard(n,newBoard2)
        print("Cost %s" % (cost(n,newBoard2)))

        print("Exection time = %s" % (time.time() - hillClimbRand_start))




        #SIMULATED ANNEALING
        print("\n\n_____Simulated Annealing Algorithm_____  ")
        print("\nInitial Sate: ")
        printBoard(n, list(board))
        print("Cost %s" % (cost(n,list(board))))
        saBoard_start = time.time()

        newBoard3 = simulatedAnnealing(n, list(board))

        print("\nNew State:")
        printBoard(n,newBoard3)
        print("Cost %s" % (cost(n,newBoard3)))

        print("Exection time = %s" % (time.time() - saBoard_start))




        #GENETIC ALGORITHM
        print("\n\n_____Genetic Algorithm_____  ")
        print("\nInitial Sate: ")
        printBoard(n, list(board))
        print("Cost %s" % (cost(n,list(board))))
        gaBoard_start = time.time()

        k=200
        population = generatePopulation(n, k)

        newBoard4 = geneticAlgorithm(population, k, n)

        print("\nNew State:")
        printBoard(n,newBoard4[0])
        print("Cost %s" % (cost(n,newBoard4[0])))
        print("Generations: %s" % (newBoard4[1]))

        print("Exection time = %s" % (time.time() - gaBoard_start))

    else:
        print("You must choose an option")





__init__()
