from __future__ import annotations

from Functions import convert_move, move_type_to_diff
import pygame
import sys


pygame.init()

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

    def get_move(self, board: list, turn: int, possible_moves: list, is_check: bool) -> tuple[int, int, int]:
        #TODO: Add possibility to claim draw
        piece_is_selected = False
        piece_x, piece_y = None, None
        promotion_active = False
        promotion_x, promotion_y = None, None
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
                        if (x, y) not in set([(move_x, 7 - move_y) for move_x, move_y, _ in possible_moves]):
                            continue
                        piece_x, piece_y = x, y
                        piece_is_selected = True
                        possible_move_types = set([move_type for tmp_x, tmp_y, move_type in possible_moves if
                                                   tmp_x == x and tmp_y == 7 - y])
                        for move_type in possible_move_types:
                            diff_x , diff_y = move_type_to_diff(move_type)
                            pygame.draw.rect(self._window, (204, 204, 0), ((x + diff_x) * FIELD_WIDTH,
                                                                           (y - diff_y) * FIELD_WIDTH,
                                                                           FIELD_WIDTH + 1,
                                                                           FIELD_WIDTH + 1),
                                             5)

                        pygame.display.update()
                    else:
                        if promotion_active:
                            if y != 4:
                                continue

                            if x == 2:
                                converted_move = convert_move(piece_x, 7 - piece_y, promotion_x, 7 - promotion_y)
                            elif x == 3:
                                converted_move = 65 + promotion_x - piece_x
                            elif x == 4:
                                converted_move = 68 + promotion_x - piece_x
                            elif x == 5:
                                converted_move = 71 + promotion_x - piece_x
                            else:
                                continue
                            if (piece_x, 7 - piece_y, converted_move) in possible_moves:
                                return piece_x, 7 - piece_y, converted_move
                            continue

                        move_type = convert_move(piece_x, 7 - piece_y, x, 7 - y)

                        if (piece_x, 7 - piece_y, move_type) in possible_moves:
                            promotion_possible = False
                            for types_moves in set([tmp_move_type for tmp_x, tmp_y, tmp_move_type in possible_moves if
                                                    tmp_x == piece_x and tmp_y == 7 - piece_y]):
                                if types_moves > 63:
                                    promotion_possible = True

                            if promotion_possible:
                                promotion_x, promotion_y = x, y
                                promotion_active = True

                                font = pygame.font.SysFont('Corbel', 35)
                                text = font.render('Promote to:' , True , (255, 255, 255))

                                pygame.draw.rect(self._window, (0, 0, 0), (2 * FIELD_WIDTH - 10, 3 * FIELD_WIDTH - 10,
                                                                           4 * FIELD_WIDTH + 20, 2 * FIELD_WIDTH + 20))
                                self._window.blit(text, (3.15 * FIELD_WIDTH, 3.3 * FIELD_WIDTH))
                                pygame.draw.rect(self._window, (255, 250, 200) if (x + y) % 2 == 0 else (150, 50, 0),
                                                 (2 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
                                self._window.blit(pieces[chr(81 + turn * 32)], (2 * FIELD_WIDTH, 4 * FIELD_WIDTH))
                                pygame.draw.rect(self._window, (255, 250, 200) if (x + y) % 2 == 0 else (150, 50, 0),
                                                 (3 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
                                self._window.blit(pieces[chr(82 + turn * 32)], (3 * FIELD_WIDTH, 4 * FIELD_WIDTH))
                                pygame.draw.rect(self._window, (255, 250, 200) if (x + y) % 2 == 0 else (150, 50, 0),
                                                 (4 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
                                self._window.blit(pieces[chr(66 + turn * 32)], (4 * FIELD_WIDTH, 4 * FIELD_WIDTH))
                                pygame.draw.rect(self._window, (255, 250, 200) if (x + y) % 2 == 0 else (150, 50, 0),
                                                 (5 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
                                self._window.blit(pieces[chr(78 + turn * 32)], (5 * FIELD_WIDTH, 4 * FIELD_WIDTH))
                                pygame.draw.line(self._window, (0, 0, 0), (3 * FIELD_WIDTH, 4 * FIELD_WIDTH),
                                                 (3 * FIELD_WIDTH, 5 * FIELD_WIDTH), 5)
                                pygame.draw.line(self._window, (0, 0, 0), (4 * FIELD_WIDTH, 4 * FIELD_WIDTH),
                                                 (4 * FIELD_WIDTH, 5 * FIELD_WIDTH), 5)
                                pygame.draw.line(self._window, (0, 0, 0), (5 * FIELD_WIDTH, 4 * FIELD_WIDTH),
                                                 (5 * FIELD_WIDTH, 5 * FIELD_WIDTH), 5)
                                pygame.display.update()
                            else:
                                return piece_x, 7 - piece_y, move_type
                        else:
                            piece_is_selected = False
                            piece_x, piece_y = None, None
                            self.show_board(board, turn, is_check)

    def run(self, board: list, turn: int, is_checked: bool,
            possible_moves: list | None = None) -> tuple[int, int, int] | None:
        self.show_board(board, turn, is_checked)
        if self._mode > 0:
            return self.get_move(board, turn, possible_moves, is_checked)
        return None

    def finished(self, winner: str, board: list, turn: int, is_check: bool) -> bool:
        self.show_board(board, turn, is_check)

        font = pygame.font.SysFont('Corbel', 25)
        font_winner = pygame.font.SysFont('Corbel', 40)
        text_restart = font.render('Restart' , True , (0, 0, 0))
        text_quit = font.render('Quit' , True , (0, 0, 0))
        text_winner_upper = font_winner.render(winner, True, (255, 255, 255))
        text_winner_lower = font_winner.render("has won", True, (255, 255, 255))

        pygame.draw.rect(self._window, (0, 0, 0), (3 * FIELD_WIDTH - 10, 3 * FIELD_WIDTH - 10,
                                                   2 * FIELD_WIDTH + 20, 2 * FIELD_WIDTH + 20))
        self._window.blit(text_winner_upper, (3.45 * FIELD_WIDTH, 3.05 * FIELD_WIDTH))
        self._window.blit(text_winner_lower, (3.35 * FIELD_WIDTH, 3.45 * FIELD_WIDTH))
        pygame.draw.rect(self._window, (255, 255, 255), (3 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
        self._window.blit(text_restart, (3.125 * FIELD_WIDTH, 4.4 * FIELD_WIDTH))
        pygame.draw.rect(self._window, (255, 255, 255), (4 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
        self._window.blit(text_quit, (4.275 * FIELD_WIDTH, 4.4 * FIELD_WIDTH))
        pygame.draw.line(self._window, (0, 0, 0), (4 * FIELD_WIDTH, 4 * FIELD_WIDTH),
                         (4 * FIELD_WIDTH, 5 * FIELD_WIDTH), 5)
        pygame.display.update()

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

                    if y != 4:
                        continue

                    if x == 3:
                        return True
                    elif x == 4:
                        pygame.quit()
                        sys.exit()

    def start(self, board: list) -> tuple[int, int]:
        self.show_board(board, 0, False)

        color = -1  # Color of the player: 0 = White, 1 = Black
        opponent = -1  # Id of the opponent software/agent

        font_color = pygame.font.SysFont('Corbel', 35)
        font_statement = pygame.font.SysFont('Corbel', 40)
        text_color = font_statement.render('Choose color', True, (255, 255, 255))
        text_white = font_color.render('White', True, (0, 0, 0))
        text_black = font_color.render('Black', True, (0, 0, 0))

        pygame.draw.rect(self._window, (0, 0, 0), (3 * FIELD_WIDTH - 10, 3 * FIELD_WIDTH - 10,
                                                   2 * FIELD_WIDTH + 20, 2 * FIELD_WIDTH + 20))
        self._window.blit(text_color, (2.95 * FIELD_WIDTH, 3.3 * FIELD_WIDTH))
        pygame.draw.rect(self._window, (255, 255, 255), (3 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
        self._window.blit(text_white, (3.075 * FIELD_WIDTH, 4.35 * FIELD_WIDTH))
        pygame.draw.rect(self._window, (255, 255, 255), (4 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
        self._window.blit(text_black, (4.135 * FIELD_WIDTH, 4.35 * FIELD_WIDTH))
        pygame.draw.line(self._window, (0, 0, 0), (4 * FIELD_WIDTH, 4 * FIELD_WIDTH),
                         (4 * FIELD_WIDTH, 5 * FIELD_WIDTH), 5)
        pygame.display.update()

        to_choose = True
        while to_choose:
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x = x // FIELD_WIDTH
                    y = y // FIELD_WIDTH

                    if y != 4:
                        continue

                    if x == 3:
                        color = 0
                        to_choose = False
                    elif x == 4:
                        color = 1
                        to_choose = False

        font_opponent = pygame.font.SysFont('Corbel', 25)
        text_opponent_upper = font_statement.render('Choose', True, (255, 255, 255))
        text_opponent_lower = font_statement.render('opponent', True, (255, 255, 255))
        text_opponent1 = font_opponent.render('Stockfish', True, (0, 0, 0))
        text_opponent2 = font_opponent.render('Agent', True, (0, 0, 0))

        pygame.draw.rect(self._window, (0, 0, 0), (3 * FIELD_WIDTH - 10, 3 * FIELD_WIDTH - 10,
                                                   2 * FIELD_WIDTH + 20, 2 * FIELD_WIDTH + 20))
        self._window.blit(text_opponent_upper, (3.35 * FIELD_WIDTH, 3.075 * FIELD_WIDTH))
        self._window.blit(text_opponent_lower, (3.2 * FIELD_WIDTH, 3.45 * FIELD_WIDTH))
        pygame.draw.rect(self._window, (255, 255, 255), (3 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
        self._window.blit(text_opponent1, (3.035 * FIELD_WIDTH, 4.4 * FIELD_WIDTH))
        pygame.draw.rect(self._window, (255, 255, 255), (4 * FIELD_WIDTH, 4 * FIELD_WIDTH, FIELD_WIDTH, FIELD_WIDTH))
        self._window.blit(text_opponent2, (4.2 * FIELD_WIDTH, 4.4 * FIELD_WIDTH))
        pygame.draw.line(self._window, (0, 0, 0), (4 * FIELD_WIDTH, 4 * FIELD_WIDTH),
                         (4 * FIELD_WIDTH, 5 * FIELD_WIDTH), 5)
        pygame.display.update()

        to_choose = True
        while to_choose:
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x = x // FIELD_WIDTH
                    y = y // FIELD_WIDTH

                    if y != 4:
                        continue

                    if x == 3:
                        opponent = 0
                        to_choose = False
                    elif x == 4:
                        opponent = 1
                        to_choose = False

        return color, opponent
