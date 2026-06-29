## Code pour gérer la plateau de jeu: quelles pièces sont où, etc.

import numpy as np
import chess

board = chess.Board(chess.STARTING_FEN)

def updateBoard(removedMagnet, addedMagnet):
    """
    removedMagnet and addedMagnet are two tuples (.,.) and (.,.), indicating grid-position of concerned squares
    """
    move = chess.Move(chess.square(removedMagnet[0], removedMagnet[1]), chess.square(addedMagnet[0], addedMagnet[1]))
    board.push(move)





