import numpy as np
import chess
from chesswindow import ChessWindow

def get_magnetBoard_from_chessBoard(chessBoard: chess.Board):
    board = np.zeros((8,8), dtype=int)
    for i in range(8):
        for j in range(8):
            if chessBoard.piece_at(chess.square(j, i)) is not None:
                board[i, j] = 1
    return board


class MagnetBoard():
    def __init__(self, chessBoard: chess.Board):
        self.board = get_magnetBoard_from_chessBoard(chessBoard)
        self.last_valid_board = self.board.copy()
        self.is_invalid = False
        self.validation_start_time = -1

        self.friendly_piece_up_square = None
        self.opponent_piece_up_square = None

        self.is_castling = False
        self.castling_move: chess.Move = None
        self.castling_rook_squares = None

        self.is_promoting = False
        self.promoting_move: chess.Move = None
        self.promoting_piece_type = None
        self.is_promotion_done = False

    def update(self, chessBoard: chess.Board, chessWindow: ChessWindow):
        """reads the switches"""
        # print(self.is_invalid, self.friendly_piece_up_square, self.opponent_piece_up_square)
        print(self.is_promoting, self.is_promotion_done, self.promoting_move, self.promoting_piece_type)
        # user_input = input("What has changed ? ")
        # if user_input == "":
        #     return self.board
        # else:
        #     list_of_changes = user_input.split("_")
        #     for change in list_of_changes:
        #         self.board[int(change[1]), int(change[0])] = int(change[2])

        chessWindow.update(self, chessBoard)
