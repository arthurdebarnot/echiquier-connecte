import chess
from stockfish import Stockfish

from app import db
from app.models.models_echecs import EchecsDefi, EchecsPartie, EchecsElo

STOCKFISH_PATH = 'stockfish'

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


def _stockfish(fen: str) -> chess.Move:
    sf = _get_engine()
    sf.set_fen_position(fen)
    bestmove = sf.get_best_move_time(500)

    if bestmove is None:
        raise ValueError("Stockfish n'a pas retourné de coup")

    return chess.Move.from_uci(bestmove)