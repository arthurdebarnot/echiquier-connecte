## Code pour gérer la plateau de jeu: quelles pièces sont où, etc.
import numpy as np
import chess
import time
from magnetboard import MagnetBoard

# Game Loop
def gameTick(magnetBoard: MagnetBoard, chessBoard: chess.Board):
    previous_magnetBoard = magnetBoard.board.copy()
    magnetBoard.update()

    if magnetBoard.is_invalid:
        print(magnetBoard.validation_start_time)
        print("last_valid_board \n", np.flip(magnetBoard.last_valid_board, axis=0))
        if not (magnetBoard.board - magnetBoard.last_valid_board).any():
            if magnetBoard.validation_start_time < 0:
                magnetBoard.validation_start_time = time.time()
            elif time.time() - magnetBoard.validation_start_time >= 5:
                magnetBoard.is_invalid = False
                magnetBoard.validation_start_time = -1
                magnetBoard.friendly_piece_up_square = None
                magnetBoard.opponent_piece_up_square = None
                magnetBoard.castling_move = None
                magnetBoard.is_castling = None
                magnetBoard.castling_rook_squares = None
        else:
            magnetBoard.validation_start_time = -1
        return

    if not (magnetBoard.board - previous_magnetBoard).any():
        print("pas de changement")
        return
    
    difference_magnetBoard = magnetBoard.board - previous_magnetBoard
    difference_magnetBoard_nonzero = difference_magnetBoard.nonzero()

    if len(difference_magnetBoard_nonzero[0]) > 1: # compte combien il y a de modification
        print("plusieurs pièces bougées en même temps")
        magnetBoard.is_invalid = True
        return
    
    modified_square = chess.square(difference_magnetBoard_nonzero[1][0], difference_magnetBoard_nonzero[0][0])
    
    if difference_magnetBoard[difference_magnetBoard_nonzero][0] == -1: # une pièce est soulevée
        if chessBoard.color_at(modified_square) == chessBoard.turn: # pièce alliée
            if magnetBoard.friendly_piece_up_square is not None:
                print("pièce alliée déjà soulevée")
                magnetBoard.is_invalid = True
                magnetBoard.friendly_piece_up_square = None
                magnetBoard.opponent_piece_up_square = None
                return
            magnetBoard.friendly_piece_up_square = modified_square
        else: # pièce adverse
            if magnetBoard.opponent_piece_up_square is not None:
                print("pièce adverse déjà soulevée")
                magnetBoard.is_invalid = True
                magnetBoard.friendly_piece_up_square = None
                magnetBoard.opponent_piece_up_square = None
                return
            magnetBoard.opponent_piece_up_square = modified_square
        return
    else: # une pièce est posée
        if magnetBoard.friendly_piece_up_square is None: # aucune pièce alliée n'avait été soulevée
            if magnetBoard.opponent_piece_up_square == modified_square: # une pièce adverse a été prise puis reposée
                magnetBoard.opponent_piece_up_square = None
                return
                
            print("aucune pièce alliée n'avait été soulevée")
            magnetBoard.is_invalid = True
            return
        elif magnetBoard.friendly_piece_up_square == modified_square:
                if magnetBoard.opponent_piece_up_square is not None:
                    print("Repose la pièce adverse")
                    magnetBoard.is_invalid = True
                magnetBoard.friendly_piece_up_square = None
                return

        move = chess.Move(magnetBoard.friendly_piece_up_square, modified_square)

        if move not in chessBoard.legal_moves:
            print("move illégal")
            magnetBoard.is_invalid = True
            return
        
        if not chessBoard.is_capture(move) and magnetBoard.opponent_piece_up_square is not None:
            print("pas une capture mais pièce adverse soulevée")
            magnetBoard.is_invalid = True
            return
        
        if chessBoard.is_kingside_castling(move) or chessBoard.is_queenside_castling(move):
            magnetBoard.is_castling = True
            magnetBoard.castling_move = move
            if chess.square_file(move.to_square) == 6:
                magnetBoard.castling_rook_squares = chess.square(7, chess.square_rank(move.to_square)), chess.square(5, chess.square_rank(move.to_square))
            elif chess.square_file(move.to_square) == 2:
                magnetBoard.castling_rook_squares = chess.square(0, chess.square_rank(move.to_square)), chess.square(3, chess.square_rank(move.to_square))
            magnetBoard.friendly_piece_up_square = None
            return
        
        if magnetBoard.is_castling:
            if chessBoard.piece_at(move.from_square).piece_type != chess.ROOK or move.from_square != magnetBoard.castling_rook_squares[0] or move.to_square != magnetBoard.castling_rook_squares[1]:
                print("la tour n'a pas été placée au bon endroit")
                magnetBoard.is_invalid = True
                return
                
            move = magnetBoard.castling_move # overwrite le move actuel pour compléter le castling
            magnetBoard.is_castling = False
            magnetBoard.castling_move = None
            magnetBoard.castling_rook_squares = None
            
        
        chessBoard.push(move)
        magnetBoard.friendly_piece_up_square = None
        magnetBoard.opponent_piece_up_square = None
        magnetBoard.last_valid_board = magnetBoard.board.copy()
        return
