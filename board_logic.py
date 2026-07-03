## Code pour gérer la plateau de jeu: quelles pièces sont où, etc.
import numpy as np
import chess
import time
from magnetboard import MagnetBoard
from chesswindow import ChessWindow

# Game Loop
def gameTick(magnetBoard: MagnetBoard, chessBoard: chess.Board, chessWindow: ChessWindow):
    previous_magnetBoard = magnetBoard.board.copy()
    magnetBoard.update(chessBoard, chessWindow)

    move = None

    if magnetBoard.is_invalid:
        print("Invalide !")
        if np.array_equal(magnetBoard.board, magnetBoard.last_valid_board):
            if magnetBoard.validation_start_time < 0:
                magnetBoard.validation_start_time = time.time()
            elif time.time() - magnetBoard.validation_start_time >= 2:
                magnetBoard.is_invalid = False
                magnetBoard.validation_start_time = -1
                magnetBoard.friendly_piece_up_square = None
                magnetBoard.opponent_piece_up_square = None
                magnetBoard.is_castling = None
                magnetBoard.castling_rook_squares = None
                magnetBoard.is_promoting = False
                magnetBoard.promoting_piece_type = None
                magnetBoard.is_promotion_done = False
                magnetBoard.current_move = None
                print("La partie peut continuer !")
        else:
            magnetBoard.validation_start_time = -1
        return

    if np.array_equal(magnetBoard.board, previous_magnetBoard):
        return
    
    difference_magnetBoard = magnetBoard.board - previous_magnetBoard
    difference_magnetBoard_nonzero = difference_magnetBoard.nonzero()

    if len(difference_magnetBoard_nonzero[0]) > 1: # compte combien il y a de modification
        print("plusieurs pièces bougées en même temps")
        magnetBoard.is_invalid = True
        return
    
    modified_square = chess.square(difference_magnetBoard_nonzero[1][0], difference_magnetBoard_nonzero[0][0])

    if magnetBoard.is_promoting: # promotion en cours
        tampon_squares = [chess.square(i, 7*(1 - chessBoard.turn)) for i in range(4)]

        if modified_square == magnetBoard.current_move.to_square:
            if difference_magnetBoard[difference_magnetBoard_nonzero][0] == -1: # pion soulevé
                return
            else:
                magnetBoard.is_promotion_done = True
        elif modified_square not in tampon_squares: # on touche à une case random pendant la promotion
            print("Tu ne peux pas modifier l'état d'une case random pendant la promotion")
            magnetBoard.is_invalid = True
            return
        else: # on modifie l'état d'une des 4 cases tampon
            if magnetBoard.friendly_piece_up_square is not None and magnetBoard.friendly_piece_up_square != modified_square:
                print("Tu as déjà touché une autre pièce")
                magnetBoard.is_invalid = True
                return

            magnetBoard.friendly_piece_up_square = modified_square # on stocke la case modifiée, aucun rapport avec friendly ou que la pièce soit soulevée ou posée
            
            if magnetBoard.board[difference_magnetBoard_nonzero] != magnetBoard.last_valid_board[difference_magnetBoard_nonzero]:
                return
            
            # on est revenu à un état normal

            magnetBoard.promoting_piece_type = chess.Board(chess.STARTING_FEN).piece_at(modified_square).piece_type

        if magnetBoard.is_promotion_done and magnetBoard.promoting_piece_type is not None:
            
            magnetBoard.current_move.promotion = magnetBoard.promoting_piece_type

            chessBoard.push(magnetBoard.current_move)
            magnetBoard.last_valid_board = magnetBoard.board.copy()

            magnetBoard.friendly_piece_up_square = None
            magnetBoard.is_promoting = False
            magnetBoard.is_promotion_done = False
            magnetBoard.current_move = None
            magnetBoard.promoting_piece_type = None
        
        return

    
    if difference_magnetBoard[difference_magnetBoard_nonzero][0] == -1: # une pièce est soulevée
        if chessBoard.color_at(modified_square) == chessBoard.turn: # pièce alliée
            if magnetBoard.friendly_piece_up_square is not None:
                print("pièce alliée déjà soulevée")
                magnetBoard.is_invalid = True
                magnetBoard.friendly_piece_up_square = None
                magnetBoard.opponent_piece_up_square = None
                return
            magnetBoard.friendly_piece_up_square = modified_square
            return
        else: # pièce adverse
            if magnetBoard.opponent_piece_up_square is not None:
                print("pièce adverse déjà soulevée")
                magnetBoard.is_invalid = True
                magnetBoard.friendly_piece_up_square = None
                magnetBoard.opponent_piece_up_square = None
                return
            magnetBoard.opponent_piece_up_square = modified_square
            if magnetBoard.current_move is None:
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
        
        move = chess.Move(magnetBoard.friendly_piece_up_square, modified_square, promotion=None)
        promotion_move = chess.Move(magnetBoard.friendly_piece_up_square, modified_square, promotion=chess.QUEEN)

        if not chessBoard.is_legal(move) and not chessBoard.is_legal(promotion_move):
            print("move illégal")
            magnetBoard.is_invalid = True
            return
    
        if not chessBoard.is_capture(move) and magnetBoard.opponent_piece_up_square is not None:
            print("pas une capture mais pièce adverse soulevée")
            magnetBoard.is_invalid = True
            return
        
        if magnetBoard.current_move is None:
            magnetBoard.current_move = move
        
    if move is None:
        move = magnetBoard.current_move
    
    if chessBoard.is_en_passant(move) and magnetBoard.opponent_piece_up_square is None:
        return
    
    if chessBoard.piece_at(move.from_square).piece_type == chess.PAWN and (chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7):
        magnetBoard.is_promoting = True
        magnetBoard.friendly_piece_up_square = None
        magnetBoard.opponent_piece_up_square = None
        return
    
    if chessBoard.is_kingside_castling(move) or chessBoard.is_queenside_castling(move):
        magnetBoard.is_castling = True
        if chess.square_file(move.to_square) == 6:
            magnetBoard.castling_rook_squares = chess.square(7, chess.square_rank(move.to_square)), chess.square(5, chess.square_rank(move.to_square))
        elif chess.square_file(move.to_square) == 2:
            magnetBoard.castling_rook_squares = chess.square(0, chess.square_rank(move.to_square)), chess.square(3, chess.square_rank(move.to_square))
        magnetBoard.friendly_piece_up_square = None
        magnetBoard.current_cmove = move
        return
    
    if magnetBoard.is_castling:
        if chessBoard.piece_at(move.from_square).piece_type != chess.ROOK or move.from_square != magnetBoard.castling_rook_squares[0] or move.to_square != magnetBoard.castling_rook_squares[1]:
            print("la tour n'a pas été placée au bon endroit")
            magnetBoard.is_invalid = True
            return
            
        move = magnetBoard.current_move # overwrite le move actuel pour compléter le castling
        magnetBoard.is_castling = False
        magnetBoard.current_cmove = None
        magnetBoard.castling_rook_squares = None

    chessBoard.push(move)
    magnetBoard.last_valid_board = magnetBoard.board.copy()
    magnetBoard.friendly_piece_up_square = None
    magnetBoard.opponent_piece_up_square = None
    magnetBoard.current_move = None
    return
