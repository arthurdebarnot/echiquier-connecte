import tkinter as tk
import numpy as np
import chess
from magnetboard import MagnetBoard


def clicked(magnetBoard: MagnetBoard, i, j):
    def modify_magnetboard(event):
        magnetBoard.board[7-i, j] = 1 - magnetBoard.board[7-i, j]
    return modify_magnetboard

def color(i, j):
    if (i+j) % 2 == 0:
        return 'white'
    else:
        return 'gray'


class ChessWindow():
    def __init__(self, magnetBoard: MagnetBoard, chessBoard: chess.Board):
        self.magnetBoard = magnetBoard
        self.chessBoard = chessBoard

        self.window = tk.Tk()
        self.window.wm_attributes("-topmost", 1)
        self.window.geometry('500x500-5+40')

        # self.board = tk.Label(self.window, text=str(np.flip(magnetBoard.board, axis=0)))
        # self.board.pack()

        self.frame_list = [[]]
        self.label_list = [[]]

        for i in range(8):
            for j in range(8):
                frame = tk.Frame(self.window, height=50, width=50, bg=color(i, j))
                frame.bind('<Button-1>', clicked(magnetBoard, i, j))
                frame.grid(column=j, row=i)
                frame.pack_propagate(False)

                label = tk.Label(frame, text="", bg=color(i, j))
                label.bind('<Button-1>', clicked(magnetBoard, i, j))
                label.pack()

                self.frame_list[i].append(frame)
                self.label_list[i].append(label)
            self.frame_list.append([])
            self.label_list.append([])


    def update(self, magnetBoard: MagnetBoard, chessBoard: chess.Board):
        # self.board.config(text=str(np.flip(magnetBoard.board, axis=0)))
        # self.board.update_idletasks()

        for i in range(8):
            for j in range(8):
                if magnetBoard.board[7-i, j] == 1:
                    self.frame_list[i][j].config(bd=3, relief='solid')
                else:
                    self.frame_list[i][j].config(bd=0, relief='solid')

                if chessBoard.piece_at(chess.square(j, 7-i)) is not None:
                    self.label_list[i][j].config(text=chess.PIECE_SYMBOLS[chessBoard.piece_at(chess.square(j, 7-i)).piece_type])
                else:
                    self.label_list[i][j].config(text="")
                
        self.window.update_idletasks()
        self.window.update()