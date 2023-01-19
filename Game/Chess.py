from __future__ import annotations

import chess
from Graphics import Window
from Functions import convert_move
import random
from ray import rllib
import gymnasium as gym
import numpy as np


MIN_OBSERVATION_SPACE = np.asarray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.uint8)
MAX_OBSERVATION_SPACE = np.asarray([12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                                    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                                    12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                                    12, 12, 12, 12, 100, 75, 4, 4, 1], dtype=np.uint8)
CONVERSION_DICT = {0: {'.': 0, 'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
                       'p': 7, 'n': 8, 'b': 9, 'r': 10, 'q': 11, 'k': 12},
                   1: {'.': 0, 'p': 1, 'n': 2, 'b': 3, 'r': 4, 'q': 5, 'k': 6,
                       'P': 7, 'N': 8, 'B': 9, 'R': 10, 'Q': 11, 'K': 12}}


class Game(rllib.env.multi_agent_env.MultiAgentEnv):
    def __init__(self, mode: int, draw: bool = False, win_reward: int = 100) -> None:
        super().__init__()
        self._board = chess.Board()
        self._mode = mode
        self._turn = 0
        self._color = -1
        self._win_reward = win_reward
        self._draw = draw
        self._window = None
        if self._draw:
            self._window = Window(self._mode)
        self._opponents = {0: self.get_moves, 1: self.get_moves}
        self._opponent = None
        self.action_space = gym.spaces.Discrete(4673)  # Alphazero paper (8 x 8 x 73) + 1 for draw
        # 64 fields, 2 counters (moves, half moves since pawn move or capture), 2 castling right (for each color),
        # 1 can claim draw by repetition
        self.observation_shape = (69,)
        self.observation_space = gym.spaces.Dict({
            "action_mask": gym.spaces.Box(0, 1, shape=(4673,), dtype=np.uint8),
            'state': gym.spaces.Box(low=MIN_OBSERVATION_SPACE,
                                    high=MAX_OBSERVATION_SPACE,
                                    dtype=np.uint8)})

        self.state = self.get_state()

    def reset(self) -> dict:
        self._board.reset()
        self._turn = 0
        if self._draw:
            self._window = Window(self._mode)
        return self.get_state()

    def step(self, actions:dict) -> tuple[dict, dict, dict, dict]:
        claim_draw = False
        for color, move in actions.items():
            if color == 'white' and self._turn == 0 or color == 'black' and self._turn == 1:
                if move == 4672:
                    if self._board.can_claim_draw():
                        claim_draw = True
                    continue
                self._board.push_san(self.move_to_str(move))
                self._turn = (self._turn + 1) % 2
        new_obs = self.get_state()
        if self._board.is_game_over(claim_draw=claim_draw):
            outcome = self._board.outcome(claim_draw=claim_draw)
            if outcome.winner is None:
                rewards = {'white': 0, 'black': 0}
            elif outcome.winner:
                rewards = {'white': self._win_reward, 'black': -self._win_reward}
            else:
                rewards = {'white': -self._win_reward, 'black': self._win_reward}
            dones = {'__all__': True}
        else:
            rewards = {'white': 0, 'black': 0}
            dones = {'__all__': False}
        infos = {}
        return new_obs, rewards, dones, infos

    def run(self) -> None:
        if self._mode == 1:
            self._color, opponent_id = self._window.start(self.get_board())
            self._opponent = self._opponents[opponent_id]
        while not self._board.is_game_over():
            if self._mode == 1:
                if self._turn == self._color:
                    move = self._window.run(self.get_board(), self._turn, self._board.is_check(), self.get_moves())
                else:
                    opponents_move = self._opponent()
                    chosen_move = random.randint(0, len(opponents_move) - 1)
                    move = opponents_move[chosen_move]
                self._board.push_san(self.move_to_str(move))
                self._turn = (self._turn + 1) % 2
            elif self._mode == 2:
                move = self._window.run(self.get_board(), self._turn, self._board.is_check(), self.get_moves())
                self._board.push_san(self.move_to_str(move))
                self._turn = (self._turn + 1) % 2

        self._turn = (self._turn + 1) % 2

        outcome = self._board.outcome()
        if outcome.winner is None:
            winner = None
        elif outcome.winner:
            winner = 'WHITE'
        else:
            winner = 'BLACK'

        if self._window.finished(winner, self.get_board(), self._turn, False):
            self.reset()
            self.run()

    def get_board(self) -> list:
        if self._turn == 0:
            return [[piece for piece in row.strip().split(' ')] for row in str(self._board).strip().split('\n')]
        return [[piece for piece in row.strip().split(' ')[::-1]] for row in str(self._board).strip().split('\n')[::-1]]

    def get_moves(self) -> list:
        return [self.move_from_str(str(move)) for move in self._board.legal_moves]

    def get_state(self) -> dict:
        color = 'white' if self._turn == 0 else 'black'
        fields = []
        board = self.get_board()
        for row in range(8):
            for column in range(8):
                fields.append(CONVERSION_DICT[self._turn][board[row][column]])

        counters = [self._board.fullmove_number, self._board.halfmove_clock]

        player = chess.WHITE if self._turn == 0 else chess.BLACK
        opponent = chess.BLACK if self._turn == 0 else chess.WHITE
        king_side_castling_player = self._board.has_kingside_castling_rights(player)
        king_side_castling_opponent = self._board.has_kingside_castling_rights(opponent)
        queen_side_castling_player = self._board.has_queenside_castling_rights(player)
        queen_side_castling_opponent = self._board.has_queenside_castling_rights(opponent)

        if king_side_castling_player and queen_side_castling_player:
            castling_player = 3
        elif king_side_castling_player:
            castling_player = 1
        elif queen_side_castling_player:
            castling_player = 2
        else:
            castling_player = 0

        if king_side_castling_opponent and queen_side_castling_opponent:
            castling_opponent = 3
        elif king_side_castling_opponent:
            castling_opponent = 1
        elif queen_side_castling_opponent:
            castling_opponent = 2
        else:
            castling_opponent = 0

        castling = [castling_player, castling_opponent]
        can_claim_draw_repetition = [self._board.can_claim_threefold_repetition()]

        state = np.asarray(fields + counters + castling + can_claim_draw_repetition, dtype=np.uint8)

        return {color: {"action_mask": self.get_action_mask(), "state": state}}

    def get_action_mask(self) -> np.ndarray:
        action_mask = np.zeros(shape=(4673,), dtype=np.uint8)
        moves = self.get_moves()

        base = 0
        for x in range(8):
            for y in range(8):
                for move_type in range(73):
                    if (x, y, move_type) in moves:
                        action_mask[base + move_type] = 1
                base = base + 73

        if self._board.can_claim_draw():
            action_mask[4672] = 1

        return action_mask

    def move_to_str(self, move: tuple[int, int, int] | int | None) -> str:
        if move is None:
            return ''

        try:
            x, y, move_type = move
        except TypeError:
            x = move // 584
            move = move % 584
            y = move // 73
            move_type = move % 73
        y_promotion = 1
        if self._turn == 1:
            x = 7 - x
            y = 7 - y
            if move_type < 56:
                move_type = (move_type + 28) % 56
            elif move_type < 64:
                move_type = 56 + ((move_type - 52) % 8)
            else:
                y_promotion = -1
                tmp_move_type = (move_type - 64) % 3
                if tmp_move_type == 0:
                    move_type = move_type + 2
                elif tmp_move_type == 2:
                    move_type = move_type - 2
        field = chr(97 + x) + str(y + 1)

        if move_type < 7:
            target_field = chr(97 + x) + str(y + move_type + 2)
            if self._turn == 0 and move_type == 0 and self.get_board()[7 - y][x] == 'P' and y == 6:
                target_field += 'q'
        elif move_type < 14:
            target_field = chr(91 + x + move_type) + str(y + move_type - 5)
            if self._turn == 0 and move_type == 7 and self.get_board()[7 - y][x] == 'P' and y == 6:
                target_field += 'q'
        elif move_type < 21:
            target_field = chr(84 + x + move_type) + str(y + 1)
        elif move_type < 28:
            target_field = chr(77 + x + move_type) + str(y +  21 - move_type)
            if self._turn == 1 and move_type == 21 and self.get_board()[y][7 - x] == 'p' and y == 1:
                target_field += 'q'
        elif move_type < 35:
            target_field = chr(97 + x) + str(y + 28 - move_type)
            if self._turn == 1 and move_type == 28 and self.get_board()[y][7 - x] == 'p' and y == 1:
                target_field += 'q'
        elif move_type < 42:
            target_field = chr(131 + x - move_type) + str(y + 35 - move_type)
            if self._turn == 1 and move_type == 35 and self.get_board()[y][7 - x] == 'p' and y == 1:
                target_field += 'q'
        elif move_type < 49:
            target_field = chr(138 + x - move_type) + str(y + 1)
        elif move_type < 56:
            target_field = chr(145 + x - move_type) + str(y + move_type - 47)
            if self._turn == 0 and move_type == 49 and self.get_board()[7 - y][x] == 'P' and y == 6:
                target_field += 'q'
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
        elif move_type == 64:
            target_field = chr(96 + x) + str(y + 1 + y_promotion) + 'r'
        elif move_type == 65:
            target_field = chr(97 + x) + str(y + 1 + y_promotion) + 'r'
        elif move_type == 66:
            target_field = chr(98 + x) + str(y + 1 + y_promotion) + 'r'
        elif move_type == 67:
            target_field = chr(96 + x) + str(y + 1 + y_promotion) + 'b'
        elif move_type == 68:
            target_field = chr(97 + x) + str(y + 1 + y_promotion) + 'b'
        elif move_type == 69:
            target_field = chr(98 + x) + str(y + 1 + y_promotion) + 'b'
        elif move_type == 70:
            target_field = chr(96 + x) + str(y + 1 + y_promotion) + 'n'
        elif move_type == 71:
            target_field = chr(97 + x) + str(y + 1 + y_promotion) + 'n'
        else:
            target_field = chr(98 + x) + str(y + 1 + y_promotion) + 'n'
        return field  + target_field


    def move_from_str(self, move: str, as_int: bool = False) -> tuple[int, int, int] | int:
        x = ord(move[0]) - 97
        y = int(move[1]) - 1
        target_x = ord(move[2]) - 97
        target_y = int(move[3]) - 1
        if self._turn == 1:
            x = 7 - x
            y = 7 - y
            target_x = 7 - target_x
            target_y = 7 - target_y
        move_type = convert_move(x, y, target_x, target_y)
        if len(move) > 4:
            if move[4] == 'r':
                move_type = 65 + target_x - x
            elif move[4] == 'b':
                move_type = 68 + target_x - x
            elif move[4] == 'n':
                move_type = 71 + target_x - x

        if as_int:
            return x * 584 + y * 73 + move_type
        return x, y, move_type


if __name__ == '__main__':
    game = Game(2, True)
    game.run()
