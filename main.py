from random import *
def placeQueens(board):
    for y in range(n):
        x = randint(0,n-1)
        board[x][y] = 1
    return board

def createBoard(n):
    Matrix = [[0 for n in range(n)] for y in range(n)];
    for x in range(n):
        for y in range(n):
            Matrix[x][y]=0
    return Matrix


print("Input the board size (n): ")
n = int(input());

board = createBoard(n)
newBoard = placeQueens(board)

for row in range(n):
    print(newBoard[row][:])
