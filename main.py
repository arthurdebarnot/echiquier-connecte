import chess
from board_logic import gameTick
from magnetboard import MagnetBoard
import evaluation

fen = chess.STARTING_FEN
prev_fen = fen

chessBoard = chess.Board(fen)
magnetBoard = MagnetBoard(chessBoard)


while True:
    print(chessBoard)
    gameTick(magnetBoard, chessBoard)
    evaluation.evaluate(chessBoard)