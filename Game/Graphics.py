from __future__ import annotations

import pygame
import sys


WIDTH = 800
FIELD_WIDTH = WIDTH // 8
pieces = {'P': pygame.transform.scale(pygame.image.load('images/white_pawn.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'R': pygame.transform.scale(pygame.image.load('images/white_rook.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'N': pygame.transform.scale(pygame.image.load('images/white_knight.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'B': pygame.transform.scale(pygame.image.load('images/white_bishop.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'Q': pygame.transform.scale(pygame.image.load('images/white_queen.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'K': pygame.transform.scale(pygame.image.load('images/white_king.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'p': pygame.transform.scale(pygame.image.load('images/black_pawn.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'r': pygame.transform.scale(pygame.image.load('images/black_rook.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'n': pygame.transform.scale(pygame.image.load('images/black_knight.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'b': pygame.transform.scale(pygame.image.load('images/black_bishop.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'q': pygame.transform.scale(pygame.image.load('images/black_queen.png'), (FIELD_WIDTH, FIELD_WIDTH)),
          'k': pygame.transform.scale(pygame.image.load('images/black_king.png'), (FIELD_WIDTH, FIELD_WIDTH))}


class Window:
    def __init__(self, mode: int):
        # Values for mode:
        # 0: Only visualize board
        # 1: Visualize board and get the move for one color
        # 2: Visualize board and get moves for both colors
        self._mode = mode
        self._window = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Chess")

    def show_board(self, board: list, turn: int, is_check: bool) -> None:
        for y, row in enumerate(board):
            for x, field in enumerate(row):
                pygame.draw.rect(self._window, (255, 250, 200) if (x + y) % 2 == 0 else (150, 50, 0),
                                 (x * FIELD_WIDTH, y * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
                if pieces.get(field):
                    self._window.blit(pieces[field], (x * FIELD_WIDTH, y * FIELD_WIDTH))
                if is_check and field == chr(75 + turn * 32):
                    pygame.draw.rect(self._window, (240, 0, 0), (x * FIELD_WIDTH,
                                                                   y * FIELD_WIDTH,
                                                                   FIELD_WIDTH + 1,
                                                                   FIELD_WIDTH + 1),
                                     5)
        for x in range(8):
            pygame.draw.line(self._window, (0, 0, 0), (0, x * FIELD_WIDTH), (WIDTH, x * FIELD_WIDTH))
            for y in range(8):
                pygame.draw.line(self._window, (0, 0, 0), (y * FIELD_WIDTH, 0), (y * FIELD_WIDTH, WIDTH))
        pygame.display.update()
        #TODO: Add visualizations for pawn promotions

    def get_move(self, board: list, turn: int, possible_moves: list, is_check: bool) -> tuple[int, int, int]:
        piece_is_selected = False
        piece_x, piece_y = None, None
        while True:
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x = x // FIELD_WIDTH
                    y = y // FIELD_WIDTH

                    if not piece_is_selected:
                        if board[y][x].isupper() != (turn == 0):
                            continue
                        field = chr(97 + x) + str(8 - y)
                        if field not in set([move[:2] for move in possible_moves]):
                            continue
                        piece_x, piece_y = x, y
                        piece_is_selected = True
                        fields_to_move = set([move[2:] for move in possible_moves if move[:2] == field])
                        for target_field in fields_to_move:
                            target_x = ord(target_field[0]) - 97
                            target_y = 8 - int(target_field[1])
                            pygame.draw.rect(self._window, (204, 204, 0), (target_x * FIELD_WIDTH,
                                                                           target_y * FIELD_WIDTH,
                                                                           FIELD_WIDTH + 1,
                                                                           FIELD_WIDTH + 1),
                                             5)

                        pygame.display.update()
                    else:
                        field = chr(97 + piece_x) + str(8 - piece_y)
                        target_field = chr(97 + x) + str(8 - y)
                        if field + target_field in possible_moves:
                            return field + target_field  #TODO: Change move representation to the one from alphazero paper
                        else:
                            piece_is_selected = False
                            piece_x, piece_y = None, None
                            self.show_board(board, turn, is_check)
        #TODO: Add input for pawn promotions

    def run(self, board: list, turn: int, is_checked: bool,
            possible_moves: list | None = None) -> tuple[int, int, int] | None:
        self.show_board(board, turn, is_checked)
        if self._mode > 0:
            return self.get_move(board, turn, possible_moves, is_checked)
        return None
