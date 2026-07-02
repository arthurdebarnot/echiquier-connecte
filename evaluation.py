import numpy as np
import chess
import stockfish_interface

def evaluate(chessBoard: chess.Board):
    current_fen = chessBoard.fen()
    if len(chessBoard.move_stack) > 0:
        last_move = chessBoard.pop()
        prev_fen = chessBoard.fen()
        chessBoard.push(last_move)
    else:
        prev_fen = current_fen

    if current_fen != prev_fen: # un coup vient d'être effectué
        prev_eval = stockfish_interface.stockfish_evaluation(prev_fen)
        current_eval = stockfish_interface.stockfish_evaluation(current_fen)

        if prev_eval['type'] == 'mate':
            prev_value = np.inf * np.sign(prev_eval['value'])
        else:
            prev_value = prev_eval['value'] / 100
        
        if current_eval['type'] == 'mate':
            current_value = np.inf * np.sign(current_eval['value'])
        else:
            current_value = current_eval['value'] / 100

        print(- np.arcsinh(current_value) - np.arcsinh(prev_value))
        print(prev_value, -current_value)


        # #mate in x > 0 : blancs peuvent ganger
        # # < 0 : noirs peuvent gagner

        # if prev_eval['type'] == 'cp' and current_eval['type'] == 'cp':
        #     deltaAvantage_blanc = current_eval['value'] - prev_eval['value']
        #     print("L'avantage pour les blancs à augmenté de : ", deltaAvantage_blanc)

        # elif prev_eval['type'] == 'cp' and current_eval['type'] == 'mate': #Il y a eu une apparition d'une possible checkmate inévitable
        #     mateValue = current_eval['value']
        #     if mateValue > 0: #blancs peuvent gagner
        #         print("Les blancs peuvent gagner en", mateValue, "coups")
        #     else: #noirs peuvent gagner
        #         print("Les noirs peuvent gagner en", -mateValue, "coups")

        # elif prev_eval['type'] == 'mate' and current_eval['type'] == 'cp': #quelqu'un vient de perdre leur possibilité de checkmate...
        #     oldMateValue = prev_eval['value']
        #     if oldMateValue > 0: #les blancs ont pu gagner, mais ont perdu cette avantage
        #         print("Les blancs pouvaient gagner, mais ont perdu leur avantage !")
        #     else:
        #         print("Les noirs pouvaient gagner, mais ont perdu leur avantage !")

        # else: #çàd les deux evaluations sont en 'mate'
        #     oldMateValue = prev_eval['value']
        #     newMateValue = current_eval['value']

        #     if oldMateValue > 0 and newMateValue > 0: 
        #         print("Les blancs conservent leur avantage, et peuvent gagner en", newMateValue, "coups")
        #     elif oldMateValue < 0 and newMateValue < 0: 
        #         print("Les noirs conservent leur avantage, et peuvent gagner en", -newMateValue, "coups")
        #     elif oldMateValue < 0 and newMateValue > 0:
        #         print("Les noirs ont perdu leur avantage: maintenant, les blancs peuvent gagner en", newMateValue, "coups")
        #     else: #çàd oldMateValue > 0 and newMateValue < 0
        #         print("Les blancs ont perdu leur avantage: maintenant, les noirs peuvent gagner en", -newMateValue, "coups")
