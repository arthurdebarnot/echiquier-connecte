import numpy as np
import board_logic
import chess
import stockfish_interface


prev_fen = chess.STARTING_FEN

#Game loop
while True:
    reading_fen = board_logic.gameTick() #renvoie une fen

    if reading_fen != prev_fen: #une coup vient d'être effectué
        eval1 = stockfish_interface.stockfish_evaluation(prev_fen)
        eval2 = stockfish_interface.stockfish_evaluation(reading_fen)

        print("Une coup a été joué !")


        #mate in x > 0 : blancs peuvent ganger
        # < 0 : noirs peuvent gagner 

        if eval1['type'] == 'cp' and eval2['type'] == 'cp':
            deltaAvantage_blanc = eval2['value'] - eval1['value']
            print("L'avantage pour les blancs à augmenté de : ", deltaAvantage_blanc)

        elif eval1['type'] == 'cp' and eval2['type'] == 'mate': #Il y a eu une apparition d'une possible checkmate inévitable
            mateValue = eval2['value']
            if mateValue > 0: #blancs peuvent gagner
                print("Les blancs peuvent gagner en", mateValue, "coups")
            else: #noirs peuvent gagner
                print("Les noirs peuvent gagner en", -mateValue, "coups")

        elif eval1['type'] == 'mate' and eval2['type'] == 'cp': #quelqu'un vient de perdre leur possibilité de checkmate...
            oldMateValue = eval1['value']
            if oldMateValue > 0: #les blancs ont pu gagner, mais ont perdu cette avantage
                print("Les blancs ont pu gagner, mais ont perdu leur avantage !")
            else:
                print("Les noirs ont pu gagner, mais ont perdu leur avantage !")

        else: #çàd les deux evaluations sont en 'mate'
            oldMateValue = eval1['value']
            newMateValue = eval2['value']

            if oldMateValue > 0 and newMateValue > 0: 
                print("Les blancs conservent leur avantage, et peuvent gagner en", newMateValue, "coups")
            elif oldMateValue < 0 and newMateValue < 0: 
                print("Les noirs conservent leur avantage, et peuvent gagner en", -newMateValue, "coups")
            elif oldMateValue < 0 and newMateValue > 0:
                print("Les noirs ont perdu leur avantage: maintenant, les blancs peuvent gagner en", newMateValue, "coups")
            else: #çàd oldMateValue > 0 and newMateValue < 0
                print("Les blancs ont perdu leur avantage: maintenant, les noirs peuvent gagner en", -newMateValue, "coups")

        prev_fen = reading_fen

    


        
        