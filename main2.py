import numpy as np
import chess
from board_logic2 import gameTick
from magnetboard import MagnetBoard

fen = "1nbqkbnr/Pppppppp/8/4r3/4p3/8/1PPPPPPP/RNBQKBNR w KQk - 0 1"

chessBoard = chess.Board(fen)
magnetBoard = MagnetBoard(chessBoard)

while True:
    print(chessBoard)

    gameTick(magnetBoard, chessBoard)
    print(np.flip(magnetBoard.board, axis=0))

