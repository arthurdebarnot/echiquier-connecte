import tkinter as tk
import chess
from magnetboard import MagnetBoard


def clicked(magnetBoard: MagnetBoard, i, j):
    """la bibliothèque Tkinter oblige que la fonction à exécuter lors d'un clic ait 1 seul argument, d'où cette fonction pour contourner cette limite"""
    def modify_magnetboard(event):
        """fonction qui modifie le magnetBoard lorsqu'on clique sur une case"""
        magnetBoard.board[7-i, j] = 1 - magnetBoard.board[7-i, j]
    return modify_magnetboard

def case_color(i, j):
    """fonction pour récupérer la couleur d'une case en fonction de sa position"""
    if (i+j) % 2 == 0:
        return 'white'
    else:
        return 'gray'

def piece_symbol(chessBoard: chess.Board, i, j):
    """fonction pour récupérer le symbole représentant la pièce à une case donnée"""
    piece = chessBoard.piece_at(chess.square(j, 7-i))
    symbol = chess.PIECE_SYMBOLS[piece.piece_type]
    if piece.color == chess.WHITE:
        return symbol.capitalize()
    else:
        return symbol.lower()


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
                frame = tk.Frame(self.window, height=50, width=50, bg=case_color(i, j))
                frame.bind('<Button-1>', clicked(magnetBoard, i, j))
                frame.grid(column=j, row=i)
                frame.pack_propagate(False)

                label = tk.Label(frame, text="", bg=case_color(i, j))
                label.bind('<Button-1>', clicked(magnetBoard, i, j))
                label.pack()

                self.frame_list[i].append(frame)
                self.label_list[i].append(label)
            self.frame_list.append([])
            self.label_list.append([])


    def update(self, magnetBoard: MagnetBoard, chessBoard: chess.Board):
        """mise à jour de l'interface graphique"""

        for i in range(8):
            for j in range(8):
                if magnetBoard.board[7-i, j] == 1:
                    self.frame_list[i][j].config(bd=3, relief='solid')
                else:
                    self.frame_list[i][j].config(bd=0, relief='solid')

                if chessBoard.piece_at(chess.square(j, 7-i)) is not None:
                    self.label_list[i][j].config(text=piece_symbol(chessBoard, i, j))
                else:
                    self.label_list[i][j].config(text="")
                
        self.window.update_idletasks()
        self.window.update()