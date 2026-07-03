import chess
from board_logic import gameTick
from magnetboard import MagnetBoard
import evaluation as evaluation
from chesswindow import ChessWindow

fen = chess.STARTING_FEN # sélection du fen de la position de départ
prev_fen = fen # stocke le FEN de la dernière position

chessBoard = chess.Board(fen) # plateau d'échec de l'ordinateur
magnetBoard = MagnetBoard(chessBoard) # plateau magnétique se mettant à jour en fonction des reed switches
chessWindow = ChessWindow(magnetBoard, chessBoard) # fenêtre graphique

prev_value = evaluation.evaluate(chessBoard.fen()) # évaluation de la dernière position


while True:
    gameTick(magnetBoard, chessBoard, chessWindow) # collecte les nouveaux états des reed switches et met à jour le magnetBoard et le chessBoard si besoin. Mets aussi à jour la gui

    # Vérification des conditions de fin de partie

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

    prev_fen, prev_value = evaluation.judge_move(chessBoard, prev_fen, prev_value) # mise à jour de la dernière évaluation et du dernier fen