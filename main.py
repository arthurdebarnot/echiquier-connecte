import chess
from board_logic import gameTick
from magnetboard import MagnetBoard
import evaluation as evaluation
from chesswindow import ChessWindow

fen = chess.STARTING_FEN
prev_fen = fen

chessBoard = chess.Board(fen)
magnetBoard = MagnetBoard(chessBoard)
chessWindow = ChessWindow(magnetBoard, chessBoard)

prev_value = evaluation.evaluate(chessBoard.fen())


while True:
    gameTick(magnetBoard, chessBoard, chessWindow)

    if chessBoard.is_checkmate():
        print("Fin de partie par échec et mat !")
        break
    if chessBoard.is_stalemate():
        print("Fin de partie par pat !")
        break
    if chessBoard.is_insufficient_material():
        print("Fin de partie par manque de matériel !")
        break
    if chessBoard.can_claim_draw():
        print("La nulle peut être réclamée !")
        break

    prev_fen, prev_value = evaluation.judge_move(chessBoard, prev_fen, prev_value)