## Code pour gérer la plateau de jeu: quelles pièces sont où, etc.
import numpy as np
import chess
import time
from magnetboard import MagnetBoard
from chesswindow import ChessWindow

# Game Loop
def gameTick(magnetBoard: MagnetBoard, chessBoard: chess.Board, chessWindow: ChessWindow):
    """Effectue toutes les actions pour détecter de potentiels nouveaux coups joués"""

    previous_magnetBoard = magnetBoard.board.copy() # copie du dernier état du magnetBoard

    magnetBoard.update(chessBoard, chessWindow) # collecte de l'état des reed switches

    move = None

    if magnetBoard.is_invalid: # cas où un coup invalide aurait été joué et qu'on attend que le plateau revienne dans la dernière position valide
        if np.array_equal(magnetBoard.board, magnetBoard.last_valid_board):
            if magnetBoard.validation_start_time < 0:
                magnetBoard.validation_start_time = time.time() # premier instant où le plateau est revenu dans une position valide
            elif time.time() - magnetBoard.validation_start_time >= 2: # si le plateau est dans la dernière posiiton valide depuis plus de 2 secondes, on reprend le fonctionnement normal
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
        else: # si on n'est pas dans la dernière position valide, on attend
            magnetBoard.validation_start_time = -1
        return

    if np.array_equal(magnetBoard.board, previous_magnetBoard): # s'il n'y a eu aucun changement sur le plateau on ne fait rien
        return
    
    # on détecte les différences entre l'état précédents et le nouvel état

    difference_magnetBoard = magnetBoard.board - previous_magnetBoard 
    difference_magnetBoard_nonzero = difference_magnetBoard.nonzero()

    if len(difference_magnetBoard_nonzero[0]) > 1: # si il y a plus d'une modification, on ne peut rien interpréter donc on rentre dans un cas invalide
        print("[INVALIDE] plusieurs pièces bougées en même temps")
        magnetBoard.is_invalid = True
        return
    
    modified_square = chess.square(difference_magnetBoard_nonzero[1][0], difference_magnetBoard_nonzero[0][0]) # on stocke la case modifiée

    if magnetBoard.is_promoting: # si une promotion est en cours
        tampon_squares = [chess.square(i, 7*(1 - chessBoard.turn)) for i in range(4)]

        if modified_square == magnetBoard.current_move.to_square: # la case du pion promu est en jeu
            if difference_magnetBoard[difference_magnetBoard_nonzero][0] == -1: # pion soulevé
                return
            else: # pion posé
                magnetBoard.is_promotion_done = True # variable qui retient si le pion a bien été promu en une autre pièce sur l'échiquier physique
        elif modified_square not in tampon_squares: # on touche à une case random pendant la promotion
            print("[INVALIDE] Tu ne peux pas modifier l'état d'une case random pendant la promotion")
            magnetBoard.is_invalid = True
            return
        else: # on modifie l'état d'une des 4 cases tampon
            if magnetBoard.friendly_piece_up_square is not None and magnetBoard.friendly_piece_up_square != modified_square:
                print("[INVALIDE] Tu as déjà touché une autre pièce")
                magnetBoard.is_invalid = True
                return

            magnetBoard.friendly_piece_up_square = modified_square # on stocke la case tampon modifiée, aucun rapport avec friendly ou que la pièce soit soulevée ou posée
            
            if magnetBoard.board[difference_magnetBoard_nonzero] != magnetBoard.last_valid_board[difference_magnetBoard_nonzero]: # tant qu'on n'est pas revenu dans l'état initial de la case tampon, on ne fait rien
                return
            
            # on est revenu à un état normal

            magnetBoard.promoting_piece_type = chess.Board(chess.STARTING_FEN).piece_at(modified_square).piece_type # on regarde alors la pièce qui correspond à la case tampon

        if not magnetBoard.is_promotion_done or magnetBoard.promoting_piece_type is None: # si la promotion n'est pas effectuée ou que la pièce n'est pas sélectionnée, on ne fait rien
            return
            
        magnetBoard.current_move.promotion = magnetBoard.promoting_piece_type # on modifie le coup à applique pour indiquer que c'est une promotion en la pièce choisie

        chessBoard.push(magnetBoard.current_move) # on ajoute le coup au chessBoard
        magnetBoard.last_valid_board = magnetBoard.board.copy() # on modifie le dernier magnetBoard valide

        magnetBoard.friendly_piece_up_square = None
        magnetBoard.is_promoting = False
        magnetBoard.is_promotion_done = False
        magnetBoard.current_move = None
        magnetBoard.promoting_piece_type = None
        return

    
    if difference_magnetBoard[difference_magnetBoard_nonzero][0] == -1: # une pièce est soulevée
        if chessBoard.color_at(modified_square) == chessBoard.turn: # pièce alliée
            if magnetBoard.friendly_piece_up_square is not None: # si une pièce alliée avait déjà été soulevée
                print("[INVALIDE] pièce alliée déjà soulevée")
                magnetBoard.is_invalid = True
                magnetBoard.friendly_piece_up_square = None
                magnetBoard.opponent_piece_up_square = None
                return
            magnetBoard.friendly_piece_up_square = modified_square
            return
        else: # pièce adverse
            if magnetBoard.opponent_piece_up_square is not None: # si une pièce adverse avait déjà été soulevée
                print("[INVALIDE] pièce adverse déjà soulevée")
                magnetBoard.is_invalid = True
                magnetBoard.friendly_piece_up_square = None
                magnetBoard.opponent_piece_up_square = None
                return
            magnetBoard.opponent_piece_up_square = modified_square
            if magnetBoard.current_move is None:
                return
    else: # une pièce est posée
        if magnetBoard.friendly_piece_up_square is None: # aucune pièce alliée n'a été soulevée
            if magnetBoard.opponent_piece_up_square == modified_square: # une pièce adverse a été prise puis reposée, on ne fait rien
                magnetBoard.opponent_piece_up_square = None
                return
                
            print("[INVALIDE] aucune pièce alliée n'a été soulevée")
            magnetBoard.is_invalid = True
            return
        elif magnetBoard.friendly_piece_up_square == modified_square: # la pièce alliée est reposée au même endroit
                if magnetBoard.opponent_piece_up_square is not None: # si une pièce adverse avait été soulevée, c'est un cas invalide
                    print("[INVALIDE] Repose la pièce adverse")
                    magnetBoard.is_invalid = True
                magnetBoard.friendly_piece_up_square = None
                return
        
        move = chess.Move(magnetBoard.friendly_piece_up_square, modified_square, promotion=None) # on enregistre le coup
        promotion_move = chess.Move(magnetBoard.friendly_piece_up_square, modified_square, promotion=chess.QUEEN) # on enregistre le coup dans le cas où c'est une promotion (important lors de la vérification de la légalité du coup)

        if not chessBoard.is_legal(move) and not chessBoard.is_legal(promotion_move): # vérification de la légalité du coup
            print("[INVALIDE] coup illégal")
            magnetBoard.is_invalid = True
            return
    
        if not chessBoard.is_capture(move) and magnetBoard.opponent_piece_up_square is not None: # vérification qu'on n'a pas soulevé une pièce adverse alors qu'on ne capture pas
            print("[INVALIDE] le coup n'est pas une capture mais une pièce adverse a été soulevée")
            magnetBoard.is_invalid = True
            return
        
        if magnetBoard.current_move is None:
            magnetBoard.current_move = move
        
    if move is None: # lors de la prise en passant, on peut vouloir que le coup soit enregistré lors du soulèvement de la pièce adverse, dans ce cas, le coup n'est à ce stade pas enregistré dans la variable move mais uniqement dans magnetBoard.current_move, on traite alors ce cas ici
        move = magnetBoard.current_move
    
    if chessBoard.is_en_passant(move) and magnetBoard.opponent_piece_up_square is None: # si le coup est une prise en passant mais que la pièce adverse n'est toujours pas soulevée, on attend
        return
    
    if chessBoard.piece_at(move.from_square).piece_type == chess.PAWN and (chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7): # on vérifie si le coup est une promotion
        magnetBoard.is_promoting = True
        magnetBoard.friendly_piece_up_square = None
        magnetBoard.opponent_piece_up_square = None
        return
    
    if chessBoard.is_kingside_castling(move) or chessBoard.is_queenside_castling(move): # on vérifie si le coup est un roque
        magnetBoard.is_castling = True
        if chess.square_file(move.to_square) == 6:
            magnetBoard.castling_rook_squares = chess.square(7, chess.square_rank(move.to_square)), chess.square(5, chess.square_rank(move.to_square))
        elif chess.square_file(move.to_square) == 2:
            magnetBoard.castling_rook_squares = chess.square(0, chess.square_rank(move.to_square)), chess.square(3, chess.square_rank(move.to_square))
        magnetBoard.friendly_piece_up_square = None
        magnetBoard.current_cmove = move
        return
    
    if magnetBoard.is_castling: # le roque se fait en deux coups : mouvement du roi puis de la tour, il faut donc le traiter à part, enregistrer qu'on est en train de roquer, puis exécuter ces instructions précises lorsqu'on bouge la tour pour vérifier la légalité du coup
        if chessBoard.piece_at(move.from_square).piece_type != chess.ROOK or move.from_square != magnetBoard.castling_rook_squares[0] or move.to_square != magnetBoard.castling_rook_squares[1]: # on s'assure que la pièce est une tour, qu'elle part de la bonne case et qu'elle arrive à la bonne case
            print("[INVALIDE] la tour n'a pas été placée au bon endroit")
            magnetBoard.is_invalid = True
            return
            
        move = magnetBoard.current_move # overwrite le move actuel pour compléter le roque
        magnetBoard.is_castling = False
        magnetBoard.current_move = None
        magnetBoard.castling_rook_squares = None

    chessBoard.push(move) # finalement on rentre le coup dans le chessBoard
    magnetBoard.last_valid_board = magnetBoard.board.copy() # on enregistre le dernier magnetBoard valide
    magnetBoard.friendly_piece_up_square = None
    magnetBoard.opponent_piece_up_square = None
    magnetBoard.current_move = None
    return
