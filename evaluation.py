import numpy as np
import chess
import stockfish_interface

def evaluate(fen: str):
    eval = stockfish_interface.stockfish_evaluation(fen)
        
    if eval['type'] == 'mate':
        value = np.inf * np.sign(eval['value'])
    else:
        value = eval['value'] / 100

    return value

def judge_move(chessBoard: chess.Board, prev_fen, prev_value):
    current_fen = chessBoard.fen()

    if current_fen == prev_fen: # aucun coup n'a été effectué
        return prev_fen, prev_value
    
    current_value = evaluate(current_fen)

    print(- np.arcsinh(current_value) - np.arcsinh(prev_value))
    print(prev_value, -current_value)

    return current_fen, current_value