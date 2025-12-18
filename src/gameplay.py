import csv
from typing import Dict, Tuple, List, Set
from .utils import rc_to_label, label_to_rc, neighbors4, neighbors8, in_bounds, ROWS
import random

GAME_STATE_PATH = "data/game_state.csv"


def make_empty_board():
    return [[None for _ in range(10)] for _ in range(10)]


def print_board(board, reveal=False):
    header = '   ' + ' '.join([f"{i:2d}" for i in range(1,11)])
    print(header)
    for r in range(10):
        row_label = ROWS[r]
        cells = []
        for c in range(10):
            v = board[r][c]
            ch = '.'
            if v is None:
                ch = '~'
            elif v == 'M':
                ch = 'o'
            elif v == 'H':
                ch = 'X'
            elif v == 'S':
                ch = 'S' if reveal else '~'
            cells.append(ch)
        print(f"{row_label}  " + '  '.join(cells))


def ships_cells_map(ships: Dict[int, dict]) -> Dict[Tuple[int,int], int]:
    m = {}
    for sid, s in ships.items():
        for cell in s['cells']:
            m[cell] = sid
    return m


def mark_surrounding_misses(board, ship_cells: List[Tuple[int,int]]):
    for r,c in ship_cells:
        for nr,nc in neighbors8(r,c):
            if board[nr][nc] is None:
                board[nr][nc] = 'M'


def record_state(turn, p_move, p_res, b_move, b_res, player_board, bot_board):
    def board_to_str(b):
        rows = []
        for r in b:
            rows.append(''.join([('.' if x is None else x) for x in r]))
        return '|'.join(rows)
    line = [str(turn), p_move or '', p_res or '', b_move or '', b_res or '', board_to_str(player_board), board_to_str(bot_board)]
    header = ['turn','player_move','player_result','bot_move','bot_result','player_board','bot_board']
    exists = False
    try:
        with open(GAME_STATE_PATH, 'r', encoding='utf-8') as f:
            exists = True
    except FileNotFoundError:
        exists = False
    with open(GAME_STATE_PATH, 'a', encoding='utf-8') as f:
        if not exists:
            f.write(','.join(header) + '\n')
        f.write(','.join([f'"{x}"' for x in line]) + '\n')


def is_ship_sunk(sid, ships, hits_map):
    for cell in ships[sid]['cells']:
        if cell not in hits_map:
            return False
    return True


class BotAI:
    def __init__(self):
        self.mode = 'random'
        self.to_check = [] 
        self.hits_current_ship = []
        self.tried = set()

    def pick(self):
        if self.to_check:
            return self.to_check.pop(0)
        choices = [(r,c) for r in range(10) for c in range(10) if (r,c) not in self.tried]
        return random.choice(choices)

    def feedback(self, coord, hit, sunk):
        self.tried.add(coord)
        if hit:
            self.hits_current_ship.append(coord)
            if sunk:
                self.to_check = []
                self.hits_current_ship = []
                self.mode = 'random'
            else:
                if len(self.hits_current_ship) == 1:
                    r,c = coord
                    for nr,nc in neighbors4(r,c):
                        if (nr,nc) not in self.tried and (nr,nc) not in self.to_check:
                            self.to_check.append((nr,nc))
                elif len(self.hits_current_ship) >= 2:
                    (r1,c1) = self.hits_current_ship[0]
                    (r2,c2) = self.hits_current_ship[1]
                    if r1 == r2:
                        row = r1
                        cols = sorted([c for _,c in self.hits_current_ship])
                        left = (row, cols[0]-1)
                        right = (row, cols[-1]+1)
                        candidates = []
                        for cand in (left, right):
                            r,c = cand
                            if 0 <= r < 10 and 0 <= c < 10 and cand not in self.tried:
                                candidates.append(cand)
                        self.to_check = candidates + self.to_check
                    elif c1 == c2:
                        col = c1
                        rows = sorted([r for r,_ in self.hits_current_ship])
                        up = (rows[0]-1, col)
                        down = (rows[-1]+1, col)
                        candidates = []
                        for cand in (up, down):
                            r,c = cand
                            if 0 <= r < 10 and 0 <= c < 10 and cand not in self.tried:
                                candidates.append(cand)
                        self.to_check = candidates + self.to_check
        else:
            pass


def play_game(player_ships: Dict[int, dict], bot_ships: Dict[int, dict]):
    player_board = make_empty_board()
    bot_board = make_empty_board()

    player_ship_map = ships_cells_map(player_ships)
    bot_ship_map = ships_cells_map(bot_ships)

    for (r,c), sid in player_ship_map.items():
        player_board[r][c] = 'S'
    for (r,c), sid in bot_ship_map.items():
        bot_board[r][c] = 'S'

    player_hits: Set[Tuple[int,int]] = set()
    bot_hits: Set[Tuple[int,int]] = set()
    bot_ai = BotAI()

    turn = 1
    while True:
        print('\n' + '='*10 + f" TURN {turn} " + '='*10)
        print("Your board (you):")
        print_board(player_board, reveal=True)
        print("Bot board (what you see):")
        # build view of bot_board for player: hide 'S'
        view_bot = [[None for _ in range(10)] for _ in range(10)]
        for r in range(10):
            for c in range(10):
                v = bot_board[r][c]
                if v == 'H':
                    view_bot[r][c] = 'H'
                elif v == 'M':
                    view_bot[r][c] = 'M'
                else:
                    view_bot[r][c] = None
        print_board(view_bot, reveal=False)

        while True:
            try:
                mv = input("Enter your move (e.g. A5): ")
                mv = mv.strip().upper()
                pr, pc = label_to_rc(mv)
                break
            except Exception as e:
                print("Invalid move:", e)
        p_move_label = mv
        if bot_board[pr][pc] == 'S':
            bot_board[pr][pc] = 'H'
            player_hits.add((pr,pc))
            p_res = 'hit'
            sid = bot_ship_map[(pr,pc)]
            if is_ship_sunk(sid, bot_ships, player_hits):
                p_res = 'sunk'
                mark_surrounding_misses(bot_board, bot_ships[sid]['cells'])
        elif bot_board[pr][pc] in ('H','M'):
            p_res = 'already'
        else:
            bot_board[pr][pc] = 'M'
            p_res = 'miss'

        bot_remaining = any(cell == 'S' for row in bot_board for cell in row)
        if not bot_remaining:
            print("You win!")
            record_state(turn, p_move_label, p_res, '', '', player_board, bot_board)
            break

        br, bc = bot_ai.pick()
        b_move_label = rc_to_label(br, bc)
        while (br,bc) in bot_ai.tried:
            br,bc = bot_ai.pick()
            b_move_label = rc_to_label(br, bc)
        if player_board[br][bc] == 'S':
            player_board[br][bc] = 'H'
            bot_hits.add((br,bc))
            sunk = False
            sid = player_ship_map[(br,bc)]
            if is_ship_sunk(sid, player_ships, bot_hits):
                sunk = True
                mark_surrounding_misses(player_board, player_ships[sid]['cells'])
                b_res = 'sunk'
            else:
                b_res = 'hit'
            bot_ai.feedback((br,bc), True, sunk)
        elif player_board[br][bc] in ('H','M'):
            b_res = 'already'
            bot_ai.feedback((br,bc), False, False)
        else:
            player_board[br][bc] = 'M'
            b_res = 'miss'
            bot_ai.feedback((br,bc), False, False)

        record_state(turn, p_move_label, p_res, b_move_label, b_res, player_board, bot_board)

        player_remaining = any(cell == 'S' for row in player_board for cell in row)
        if not player_remaining:
            print("Bot wins!")
            break

        turn += 1