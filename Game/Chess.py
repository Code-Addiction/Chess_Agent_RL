from __future__ import annotations

import chess
from Graphics import Window


class Game:
    #TODO: Implement gym interface for multi-agent training
    def __init__(self, mode: int, draw: bool = False) -> None:
        self._board = chess.Board()
        self._mode = mode
        self._turn = 0
        self._draw = draw
        self._window = None
        if self._draw:
            self._window = Window(self._mode)

    def reset(self) -> None:
        self._board.reset()
        self._turn = 0
        if self._draw:
            self._window = Window(self._mode)

    def run(self) -> None:
        while not self._board.is_game_over():
            move = self._window.run(self.get_board(), self._turn, self._board.is_check(), self.get_moves())
            self._board.push_san(move)
            self._turn = (self._turn + 1) % 2

        if self._window.finished('WHITE' if (self._turn - 1) % 2 == 0 else 'BLACK', self.get_board(), self._turn, True):
            self.reset()
            self.run()

    def get_board(self) -> list:
        return [[piece for piece in row.strip().split(' ')] for row in str(self._board).strip().split('\n')]

    def get_moves(self) -> list:
        return [str(move) for move in self._board.legal_moves]


if __name__ == '__main__':
    game = Game(2, True)
    game.run()
