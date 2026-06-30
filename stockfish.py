import chess
from stockfish import Stockfish

from app import db
from app.models.models_echecs import EchecsDefi, EchecsPartie, EchecsElo

STOCKFISH_PATH = 'stockfish'


def _stockfish(fen: str) -> chess.Move:
    """Demande le meilleur coup à Stockfish via le wrapper Python."""
    sf = Stockfish(
        path=STOCKFISH_PATH,
        parameters={
            'UCI_LimitStrength': False,
            'Threads': 4,           # ajustable
            'Hash': 1024,           # ajustable
        },
    )
    sf.set_fen_position(fen)
    bestmove = sf.get_best_move_time(500)

    if bestmove is None:
        raise ValueError('Stockfish n\'a pas retourné de coup')

    return chess.Move.from_uci(bestmove)