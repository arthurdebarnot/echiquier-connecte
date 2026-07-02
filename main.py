import chess
from board_logic import gameTick
from magnetboard import MagnetBoard
import evaluation

fen = "rnbqk1nr/1ppp1Qpp/p7/2b1p3/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1"
prev_fen = fen

chessBoard = chess.Board(fen)
magnetBoard = MagnetBoard(chessBoard)

prev_value = evaluation.evaluate(chessBoard.fen())


while True:
    print(chessBoard)
    gameTick(magnetBoard, chessBoard)

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

    evaluation.judge_move(chessBoard, prev_fen, prev_value)