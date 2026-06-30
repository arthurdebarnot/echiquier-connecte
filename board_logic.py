## Code pour gérer la plateau de jeu: quelles pièces sont où, etc.
import numpy as np
import chess
import time

def createStartingMagnetBoard():
    board = np.zeros((8,8), dtype = int)
    board[0:2,:]=1
    board[6:,:]=1
    return board

chessBoard = chess.Board(chess.STARTING_FEN)

CASTLE_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R w KQkq - 0 1'

startingMagnetBoard = createStartingMagnetBoard()

magnetBoard_prev = np.copy(startingMagnetBoard)
magnetBoard_new = np.copy(startingMagnetBoard)

currentPlayerColour = chess.WHITE

modifiedSquareStack = None #with convention [(file, rank), colour, moveType]


illegalSituationInAction = False
lastlegalBoard = np.copy(startingMagnetBoard)

legalPositionTimeCounter = 0
currentTime = time.time()


def updateBoard(removedMagnet, addedMagnet):
    """
    removedMagnet and addedMagnet are two tuples (.,.) and (.,.), indicating grid-position of concerned squares
    """
    
    move = chess.Move(chess.square(removedMagnet[1], removedMagnet[0]), chess.square(addedMagnet[1], addedMagnet[0])) #NB: Syntax for chess.py is file then rank (ie colonne then ligne mdr les batards)


    if move not in chessBoard.legal_moves:
        global illegalSituationInAction
        global currentTime

        print("ERROR: illegal move. Please undo")
        illegalSituationInAction = True
        currentTime = time.time()
        return chessBoard.fen()
    
    chessBoard.push(move)

    global lastlegalBoard
    lastlegalBoard = np.copy(magnetBoard_new)

    global currentPlayerColour

    #Change current player colour
    currentPlayerColour = chessBoard.turn
        
    return chessBoard.fen()

def readMagnetBoard():
    """
    Returns the current magnet board (0s and 1s) (at the moment, only simulated...)
    """
    board = magnetBoard_new

    #NB: if input "READ", will print board
    user_input = input("Input the changes: ")
    
    if user_input == "READ":
        print(chessBoard)
    elif user_input == "":
        return board
    else:
        list_of_changes = user_input.split("_") #Syntax: enter a string of type "430_131_160", where grid position (4,3) becomes 1, (1,3) becomes 1, and (1,6) becomes 0
    
        for change in list_of_changes:
            board[int(change[0]), int(change[1])] = int(change[2])
            print(change)

    return board


def getModifiedSquare(differenceBoard):
    """
    Returns tuple of grid position of modified square
    """
    return differenceBoard.nonzero()[0][0], differenceBoard.nonzero()[1][0]


# Game Loop
def gameTick():

    #globalise the variables (cursed maybe...)
    global chessBoard

    global startingMagnetBoard

    global magnetBoard_prev
    global magnetBoard_new

    global currentPlayerColour

    global modifiedSquareStack

    global illegalSituationInAction
    global lastlegalBoard

    global legalPositionTimeCounter
    global currentTime


    currentFen = chessBoard.fen()


    if not illegalSituationInAction:

        magnetBoard_new = readMagnetBoard()

        if not np.array_equal(magnetBoard_new, magnetBoard_prev):
            differenceBoard = magnetBoard_new - magnetBoard_prev
            numberofDifferences = int(np.sum(np.abs(differenceBoard), axis = (0,1)))

            #Update board
            magnetBoard_prev = np.copy(magnetBoard_new)
            
            if numberofDifferences > 1:
                print("ERROR: more than 1 difference detected")
                illegalSituationInAction = True
                currentTime = time.time()
                return currentFen
            else:
                modifiedSquare = getModifiedSquare(differenceBoard) #tuple of grid position of modified square
                modifiedSquare_chess = chess.square(modifiedSquare[1], modifiedSquare[0])  #NB: Syntax for chess.py is file then rank (ie colonne then ligne mdr les batards)
                
                moveType = differenceBoard[modifiedSquare[0], modifiedSquare[1]] #1 if piece added, -1 if piece removed

                
                #Move detector logic
                if moveType == -1:
                    modifiedSquareColour = chessBoard.piece_at(modifiedSquare_chess).color
                    if currentPlayerColour == modifiedSquareColour:
                        modifiedSquareStack = [modifiedSquare, modifiedSquareColour, moveType]

                else:
                    # if currentPlayerColour != modifiedSquareColour:
                    #     print("ERROR: player played out of turn. Please return to the last position") #Allumer les lumières
                    #     illegalSituationInAction = True
                    #     currentTime = time.time()
                    #     continue

                    if modifiedSquareStack == None:
                        print("ERROR: piece placed, but no piece removed")
                        illegalSituationInAction = True
                        currentTime = time.time()
                        return currentFen

                    if modifiedSquareStack[2] == 1:
                        print("ERROR: two pieces of same colour were placed")
                        illegalSituationInAction = True
                        currentTime = time.time()
                        return currentFen

                    startPos = modifiedSquareStack[0]
                    endPos = modifiedSquare
                        
                    if startPos == endPos:
                        modifiedSquareStack = None
                        return currentFen
                    
                    currentFen = updateBoard(startPos, endPos)
                    modifiedSquareStack = None





    else: #Illegal situation in action
    
        currentMagnetBoard = readMagnetBoard()
        

        if np.array_equal(currentMagnetBoard,lastlegalBoard):

            #Cette boucle if détecte l'instant exact où le board a été bien remise en bon état 
            if legalPositionTimeCounter == 0:
                legalPositionTimeCounter = 0.001
                currentTime = time.time()

            legalPositionTimeCounter += time.time() - currentTime

            currentTime = time.time()
        else:
            legalPositionTimeCounter = 0


        if legalPositionTimeCounter > 5: #time to wait in seconds
            print("All green!")
            illegalSituationInAction = False
            modifiedSquareStack = None
            legalPositionTimeCounter = 0
            magnetBoard_new = np.copy(currentMagnetBoard)
            magnetBoard_prev = np.copy(currentMagnetBoard)
            return currentFen

        print("legalPositionTime counter is : ", legalPositionTimeCounter)




    return currentFen

        







