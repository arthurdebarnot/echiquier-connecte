import chess
from stockfish import Stockfish

STOCKFISH_PATH = 'stockfish/stockfish-windows-x86-64-avx2.exe'

_sf_instance = None

def _get_engine() -> Stockfish:
    global _sf_instance
    if _sf_instance is None:
        _sf_instance = Stockfish(
            path=STOCKFISH_PATH,
            parameters={
                'UCI_LimitStrength': False,
                'Threads': 4,
                'Hash': 1024,
            },
        )
    return _sf_instance


def stockfish_best_move(fen: str) -> chess.Move:
    sf = _get_engine()
    sf.set_fen_position(fen)
    bestmove = sf.get_best_move_time(500)

    if bestmove is None:
        raise ValueError("Stockfish n'a pas retourné de coup")

    return chess.Move.from_uci(bestmove)

def stockfish_evaluation(fen: str):
    sf = _get_engine()
    sf.set_fen_position(fen)
    return sf.get_evaluation(500)