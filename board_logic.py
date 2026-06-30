## Code pour gérer la plateau de jeu: quelles pièces sont où, etc.

import numpy as np
import chess
import time

chessBoard = chess.Board(chess.STARTING_FEN)
magnetBoard_prev = np.zeros((8,8), dtype = int)
magnetBoard_new = np.zeros((8,8), dtype = int)

currentPlayerColour = chess.WHITE

def updateBoard(removedMagnet, addedMagnet):
    """
    removedMagnet and addedMagnet are two tuples (.,.) and (.,.), indicating grid-position of concerned squares
    """
    move = chess.Move(chess.square(removedMagnet[0], removedMagnet[1]), chess.square(addedMagnet[0], addedMagnet[1]))

    if move not in chessBoard.legal_moves:
        print("ERROR: illegal move. Please undo")
        return
    
    chessBoard.push(move)

def readMagnetBoard():
    """
    Returns the current magnet board (0s and 1s)
    """
    return np.zeros((8,8), dtype = int)

def getModifiedSquare(differenceBoard):
    """
    Returns tuple of grid position of modified square
    """
    return differenceBoard.nonzero()[0][0], differenceBoard.nonzero()[1][0]

modifiedSquareStack = None #with convention [(file, rank), colour, moveType]


illegalSituationInAction = False
lastlegalBoard = None

legalPositionTimeCounter = 0
currentTime = time.time()

# Game Loop
while True:

    if not illegalSituationInAction:
        magnetBoard_new = readMagnetBoard()

        if magnetBoard_new != magnetBoard_prev:
            differenceBoard = magnetBoard_new - magnetBoard_prev
            numberofDifferences = int(np.sum(np.abs(differenceBoard), axis = (0,1)))
            
            if numberofDifferences > 1:
                print("ERROR: more than 1 difference detected")
                illegalSituationInAction = True
                continue
            else:
                modifiedSquare = getModifiedSquare(differenceBoard) #tuple of grid position of modified square
                modifiedSquare_chess = chess.square(modifiedSquare[0], modifiedSquare[1])
                
                moveType = differenceBoard[modifiedSquare[0], modifiedSquare[1]] #1 if piece added, -1 if piece removed
                modifiedSquareColour = chessBoard.piece_at(modifiedSquare_chess).color

                #Update board
                magnetBoard_prev = magnetBoard_new
                
                #Move detector logic
                if moveType == -1:
                    if currentPlayerColour == modifiedSquareColour:
                        modifiedSquareStack = [modifiedSquare, modifiedSquareColour, moveType]
                
                else:
                    if currentPlayerColour != modifiedSquareColour:
                        print("ERROR: player played out of turn. Please return to the last position") #Allumer les lumières
                        illegalSituationInAction = True
                        continue

                    if modifiedSquareStack == None:
                        print("ERROR: piece placed, but no piece removed")
                        illegalSituationInAction = True
                        continue

                    if modifiedSquareStack[2] == 1:
                        print("ERROR: two pieces of same colour were placed")
                        illegalSituationInAction = True
                        continue

                    startPos = modifiedSquareStack[0]
                    endPos = modifiedSquare
                        
                    if startPos == endPos:
                        modifiedSquareStack = None
                        continue
                    
                    updateBoard(startPos, endPos)
                    modifiedSquareStack = None


        lastlegalBoard = magnetBoard_new




    else: #Illegal situation in action
        currentMagnetBoard = readMagnetBoard()

        if currentMagnetBoard == lastlegalBoard:
            legalPositionTimeCounter += time.time() - currentTime
        else:
            legalPositionTimeCounter = 0


        if legalPositionTimeCounter > 2: #time to wait in seconds
            illegalSituationInAction = False
            modifiedSquareStack = None
            legalPositionTimeCounter = 0
            continue

        currentTime = time.time()
        







