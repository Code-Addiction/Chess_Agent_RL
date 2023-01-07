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
            self._board.push_san(self.move_to_str(move))
            self._turn = (self._turn + 1) % 2

        if self._window.finished('WHITE' if (self._turn - 1) % 2 == 0 else 'BLACK', self.get_board(), self._turn, True):
            self.reset()
            self.run()

    def get_board(self) -> list:
        #TODO: Switch perspective so that the color of the current player is always at the bottom
        return [[piece for piece in row.strip().split(' ')] for row in str(self._board).strip().split('\n')]

    def get_moves(self) -> list:
        #TODO: Check if moves have to be adopted to perspective change
        return [str(move) for move in self._board.legal_moves]

    def move_to_str(self, move: tuple[int, int, int] | None) -> str:
        #TODO: Adopt to perspective change
        if move is None:
            return ''

        x, y, move_type = move
        field = chr(97 + x) + str(y + 1)

        if move_type < 7:
            target_field = chr(97 + x) + str(y + move_type + 2)
        elif move_type < 14:
            target_field = chr(91 + x + move_type) + str(y + move_type - 5)
        elif move_type < 21:
            target_field = chr(84 + x + move_type) + str(y + 1)
        elif move_type < 28:
            target_field = chr(77 + x + move_type) + str(y +  21 - move_type)
        elif move_type < 35:
            target_field = chr(97 + x) + str(y + 28 - move_type)
        elif move_type < 42:
            target_field = chr(131 + x - move_type) + str(y + 35 - move_type)
        elif move_type < 49:
            target_field = chr(138 + x - move_type) + str(y + 1)
        elif move_type < 56:
            target_field = chr(145 + x - move_type) + str(y + move_type - 47)
        elif move_type < 58:
            x_move = move_type - 55
            target_field = chr(97 + x + x_move) + str(y + 4 - x_move)
        elif move_type < 60:
            y_move = 57 - move_type
            target_field = chr(100 + x + y_move) + str(y + 1 + y_move)
        elif move_type < 62:
            x_move = 59 - move_type
            target_field = chr(97 + x + x_move) + str(y - 2 - x_move)
        elif move_type < 64:
            y_move = move_type - 61
            target_field = chr(94 + x + y_move) + str(y + 1 + y_move)
        else:
            pass  #TODO: Underpromotions to str for perspective change

        return field  + target_field


if __name__ == '__main__':
    game = Game(2, True)
    game.run()
