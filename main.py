import numpy as np
import board_logic
import chess
import stockfish_interface


prev_fen = chess.STARTING_FEN

#Game loop
while True:
    reading_fen = board_logic.gameTick() #renvoie une fen

    if reading_fen != prev_fen: #une coup vient d'être effectué
        #eval1 = stockfish_interface.stockfish_evaluation(prev_fen)
        #eval2 = stockfish_interface.stockfish_evaluation(reading_fen)
        #print("La nouvelle position est évaluée à ", str(eval2))
        print("Une coup a été joué !")
        prev_fen = reading_fen

    

        
        