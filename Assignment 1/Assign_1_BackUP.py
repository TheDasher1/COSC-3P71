import math
import numpy as np
import random

def main():
    playConnectFour()
    x = 4
    y = 5

    print(f'x = {x}, y = {y}')

    x, y = y, x

    print(f'x = {x}, y = {y}')

    print(f'Game over.')

def playConnectFour():
    ch = ['X', 'O'] # a list containing the representation of the two players that the first player will draw from
    
    #client_one.sendall("You are player 1, choose between 'X' or 'O' to play as: ".encode())
    #print("You are player 2, Player 1 is choosing between 'X' or 'O' to play as.\n")
    
    while len(ch) != 1:
        ##print("You are player 1, choose between 'X' or 'O' to play as: ")
        #client_two.sendall("You are player 2, Player 1 is choosing between 'X' or 'O' to play as.\n".encode())
        #data = client_one.recv(100)
        str_data = input("You are player 1, choose between 'X' or 'O' to play as: ")

        if str_data in ch:
            _ = ch.index(str_data)
            global player 
            player = ch.pop(_) # removes the chosen letter from the list if it was found and assigns it to player 1
            
            #player2 = ch.pop() # assigns the left over letter to player 2
            global cpu 
            cpu = ch.pop() # assigns the AI the left over character to play as
            
            print(f"You chose {player} to play as and CPU will play as {cpu}.\n")
            curPlayer = player
            #client_two.sendall(f"Player 1 chose to play as {player1} and you will play as {player2}.\n".encode())
            break # lets players know about their letters and breaks out of the loop
    
    # the board data is held within the main game method and passed to any helper methods to modify and return, this way each 2 players have their own unique board
    newBoard = np.array([
                        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        #[' ', ' ', ' ', ' ', ' ', ' ', ' ']
                        ]) # This array will represent the connect 4 board of 6 rows and 7 columns, standard size
    
    drawBoard(newBoard)

    #curPlayer = player1 # sets the current players chosen letter to play as

    #currentClient = client_one # sets the current user as the client to send and recv data from

    while True:
        try:
            #client_one.sendall(f"Player {curPlayer}'s turn.\n".encode())
            #client_two.sendall(f"Player {curPlayer}'s turn.\n".encode())

            #currentClient.sendall("Enter row number between 1-6: ".encode())
            #r = int(currentClient.recv(100))
            ##print("Enter column number between 1-7 to drop your token into: ")
            c = int(input("Enter column number between 1-7 to drop your token into: "))
            
            #if (r >= 1 and r <= 6) and (c >= 1 and c <= 7):
            if (c >= 1 and c <= 7):
                #r -= 1 # indexing
                c -= 1 # indexing
                
                # -------------------------------------------------
                #enterSuc = enterSpot(r, c, newBoard, curPlayer)
                # -------------------------------------------------

                enterSuc = dropPiece(c, newBoard, curPlayer)

                drawBoard(newBoard)

                if enterSuc == 1: # if the current players move was successfully completed, checks for win or changes current player.
                    if checkForWin(newBoard, curPlayer): # checks for win condition based on the current player's move
                        #client_one.sendall(f"Player {curPlayer} has won the game.\n".encode())
                        #client_two.sendall(f"Player {curPlayer} has won the game.\n".encode())
                        print(f'{curPlayer} has won the game.')
                        break

                    elif isBoardFull(newBoard):
                        #client_one.sendall(f"No more empty spots remaining. Game ends in a draw.\n".encode())
                        #client_two.sendall(f"No more empty spots remaining. Game ends in a draw.\n".encode())
                        print(f'No more empty spots remaining. Game ends in a draw.')
                        break

                    else:
                        if curPlayer == player: # swaps players on successful previous move
                            print('CPU turn.')
                            curPlayer = cpu
                            cpuWin = cpuTurn(newBoard, curPlayer)
                            
                            if cpuWin == 1:
                                break

                            elif cpuWin == 0:
                                print('No more empty spots remaining, game ends in a draw.')
                                break
                            
                            else:
                                curPlayer = player
                            # currentClient = client_two

                        # else:
                        #     curPlayer = player
                            # currentClient = client_one
                            
                elif enterSuc == 0:
                    #client_one.sendall(f'Spot already taken. {curPlayer} goes again.\n'.encode())
                    #client_two.sendall(f'Spot already taken. {curPlayer} goes again.\n'.encode())
                    print(f'Spot already taken.')

                elif enterSuc == -1: # test branch, delete and reinstate else method below if this one doesnt work
                    # client_one.sendall(f'Invalid move. {curPlayer} goes again.\n'.encode())
                    # client_two.sendall(f'Invalid move. {curPlayer} goes again.\n'.encode())
                    print(f'Invalid move.')
                # else: # Old method of elif above, uncomment if that one doesnt work
                #     #print(f'{curPlayer} goes again.') # if move was unsuccessful, lets the player go again
                #     currentClient.sendall(f'{curPlayer} goes again.'.encode())
            
        except ValueError as err:
            print(f'Invalid input. {err}')


def checkForWin(brd, player):
    return checkHorizontal(brd, player) or checkVertical(brd, player) or checkDiagonal(brd, player) # checks if the current players token has 4 pieces in line on an horizontal, vertical and diagonal level

def checkHorizontal(brd, player): # Checks 4 spots horizontally, takes the board to check and player token to check for, returns True if there are 4 pieces lined up, or False
    for i in range(len(brd)):
        for j in range((len(brd[0]) - 3)): 
            if brd[i][j] == player and brd[i][j + 1] == player and brd[i][j + 2] == player and brd[i][j + 3] == player:
                return True

    return False

def checkVertical(brd, player):# Checks 4 spots vertical, takes the board to check and player token to check for, returns True if there are 4 pieces lined up, or False
    for i in range(len(brd[0]) - 4):
        for j in range(len(brd)): 
            if brd[i][j] == player and brd[i + 1][j] == player and brd[i + 2][j] == player and brd[i + 3][j] == player:
                return True

    return False

def checkDiagonal(brd, player):
    for i in range(len(brd[0]) - 4):# Checks 4 spots diagonally going right
        for j in range(len(brd) - 2): 
            if brd[i][j] == player and brd[i + 1][j + 1] == player and brd[i + 2][j + 2] == player and brd[i + 3][j + 3] == player:
                return True

    # for i in range(len(brd[0]) - 2, 0, -1): # checks for 4 spots diagonally going left ----- doesnt work right -----
    #     for j in range(len(brd) - 1, 0, -1):
    #         if brd[i][j] == player and brd[i - 1][j + 1] == player and brd[i - 2][j + 2] == player and brd[i - 3][j + 3] == player:
    #             return True

    for i in range(7 - 3): # checks for 4 spots diagonally going left
        for j in range(3, 6):
            if brd[i][j] == player and brd[i - 1][j + 1] == player and brd[i - 2][j + 2] == player and brd[i - 3][j + 3] == player:
                return True
    
    return False

def dropPiece(col, board, playerRep): # drops the piece of the player in the chosen column in their board
    try:
        for i in range(len(board) - 1, -1, -1):
            if board[i][col] == ' ':
                board[i][col] = playerRep
                return 1
        
        return 0

    except IndexError:
        return -1

def cpuTurn(brd, token):
    #columToDrop = random.randint(0, 6)
    #columToDrop = pickBestMove(brd, token)
    columToDrop, MiniMaxReturn = miniMax(brd, 2, True)

    print(f'CPU chose column {columToDrop + 1}') # + 1 to for indexing

    SuccesFullEnter = dropPiece(columToDrop, brd, token)

    drawBoard(brd)

    if SuccesFullEnter == 1: # if the current players move was successfully completed, checks for win or changes current player.
        if checkForWin(brd, token): # checks for win condition based on the current player's move
            print(f'CPU has won the game.')
            return 1

        elif isBoardFull(brd):
            print(f'No more empty spots remaining. Game ends in a draw.')
            return 0
    
def miniMax(board, depth, maximizingPlayer):
    if depth == 0 or terminalNode(board): # checks if depth has reached 0(no more calls) or if this move is terminal(player/cpu wins, or if there are no more empty spots in the board)
        if terminalNode(board):
            if checkForWin(board, cpu): return (None, 1000000000)
            
            elif checkForWin(board, player): return (None, -1000000000) # if the player would win in this move, returns -100000000000 points to signify, it being a bad move

            else:
                return (None, 0)
        
        else:
            return (None, scorePosition(board, cpu))

    if maximizingPlayer: # Maximize CPU's score
        value = -math.inf # negative infinite value as a base score to work off of
        column = random.randint(0, 6) # init a random column to return

        for c in getOpenColumns(board): # only tests for columns that have empty spots remaining to drop a piece into, re-evaluated every recursive call
            tempBoard = board.copy() # creates a copy of the current board that was passed through to predict for

            dropPiece(c, tempBoard, cpu) # drops a piece into the temp board created

            tempScore = miniMax(tempBoard, depth - 1, False)[1] # use Min-Max algo to evaluate if dropping a piece into that column would be befenifital

            if tempScore > value: # if score was better than current value(good for CPU) then stores it to be returned after
                value = tempScore
                column = c # stores current column to return after

        return column, value

    else: # Minimize the player's score
        value = math.inf # positive infinite value as a base score to work off of
        column = random.randint(0, 6) # init a random column to return

        for c in getOpenColumns(board): # only tests for columns that have empty spots remaining to drop a piece into, re-evaluated every recursive call
            tempBoard = board.copy() # creates a copy of the current board that was passed through to predict for

            dropPiece(c, tempBoard, player) # drops a piece into the temp board created

            tempScore = miniMax(tempBoard, depth - 1, True)[1] # use Min-Max algo to evaluate if dropping a piece into that column would be detrimental

            if tempScore < value: # if score was worse than current value(bad for CPU) then stores it to be returned after
                value = tempScore
                column = c # stores current column to return after

        return column, value

def terminalNode(board):
    return isBoardFull(board) or checkForWin(board, player) or checkForWin(board, cpu)

def scorePosition(board, token):
    score = 0
    
    # Horizontal check
    for r in range(6):
        rowArray = [i for i in list(board[r, :])]

        for c in range(7 - 3):
            window = rowArray[c: c + 4]
            
            score += evaluateWindow(window, token)

    # Vertical check
    for c in range(7):
        colArray = [i for i in list(board[ :, c])]

        for r in range(6 - 3):
            window = colArray[r: r + 4]

            score += evaluateWindow(window, token)

    # Diagonal check going right
    for r in range(6 - 3):
        for c in range(7 - 3):
            diaArray = [board[r + i][c + i] for i in range(4)]

            score += evaluateWindow(diaArray, token)

    # Diagonal check going left
    for r in range(6 - 3):
        for c in range(7 - 3):
            diaArray = [board[r - i + 3][c + i] for i in range(4)]

            score += evaluateWindow(diaArray, token)

    return score

def pickBestMove(board, token):
    bestScore = -1000
    #getOpenSpots = getValidLocations(board)
    #bestColumn = random.choice(getOpenSpots)
    bestColumn = random.randint(0, 6) # init a random column to drop a piece on

    for c in range(7):
        tempBoard = board.copy()

        dropPiece(c, tempBoard, token)

        score = scorePosition(tempBoard, token)

        if score > bestScore:
            bestScore = score
            bestColumn = c

    return bestColumn

def evaluateWindow(checkArray, token):
    score = 0

    if checkArray.count(token) == 4:
        score += 100
            
    elif checkArray.count(token) == 3 and checkArray.count(' ') == 1:
        score += 10
    
    elif checkArray.count(token) == 2 and checkArray.count(' ') == 2:
        score += 5

    if checkArray.count(player) == 3 and checkArray.count(' ') == 1:
        score -= 80

    return score

def getOpenColumns(board):
    validLocations = []

    for c in range(7): # check is the top layer of the array has any empty spots, if so, adds that column as a possible location to drop piece in to
        if board[0][c] == ' ':
            validLocations.append(c)
    
    return validLocations

def drawBoard(brd): # this method just draws the board for both players, it takes both clients and the board as parameters
    # cl1.sendall('  1   2   3   4   5   6   7 \n'.encode())
    print('  1   2   3   4   5   6   7 ')

    # cl1.sendall('-----------------------------\n'.encode())
    print('-----------------------------')
    
    num = 1
    
    for i in range(len(brd)):
        # cl1.sendall('| '.encode())
        print('|', end =" ")

        for j in range(len(brd[0])):
            # cl1.sendall(brd[i][j].encode())
            print(brd[i][j], end =" ")

            # cl1.sendall(' | '.encode())
            print('|', end =" ")
        
        # cl1.sendall((str(num) + '\n').encode())
        print(str(num))
        
        num += 1
        
        # cl1.sendall('-----------------------------\n'.encode())
        print('-----------------------------')
        

    #print('-----------------------------') # this line does nothing

def isBoardFull(board): # method checks if there are any empty spots for the players to place their piece, if there is none, returns False to indicate the game is over
    val = True

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == ' ':
                val = False
                break

    return val

if __name__ == '__main__':
    main()