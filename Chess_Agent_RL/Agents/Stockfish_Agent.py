import chess.engine


class StockfishAgent:
    def __init__(self, path: str, time_limit: float = 0.1):
        self._engine = chess.engine.SimpleEngine.popen_uci(path)
        self._time_limit = chess.engine.Limit(time=time_limit)

    def __del__(self):
        self._engine.quit()

    def compute_single_action(self, state: dict, board, *args, **kwargs) -> tuple[str, None, None]:
        return str(self._engine.play(board, self._time_limit).move), None, None
