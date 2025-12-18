import random
from typing import Dict, Tuple, List, Set
from .utils import neighbors8, in_bounds, ROWS, COLS, rc_to_label, cells_adjacent_any

DATA_PATH = "data/bot_ships.csv"

REQUIRED_SIZES = [4,3,3,2,2,2,1,1,1,1]


def place_ship_random(size: int, occupied: Set[Tuple[int,int]]) -> List[Tuple[int,int]]:
    attempts = 0
    while attempts < 2000:
        attempts += 1
        orientation = random.choice(['H', 'V']) if size > 1 else 'H'
        if orientation == 'H':
            r = random.randrange(0,10)
            c = random.randrange(0, 10 - size + 1)
            cells = [(r, c+i) for i in range(size)]
        else:
            r = random.randrange(0,10 - size + 1)
            c = random.randrange(0,10)
            cells = [(r+i, c) for i in range(size)]
        if any(cell in occupied for cell in cells):
            continue
        bad = False
        for (r0,c0) in cells:
            for nr,nc in neighbors8(r0,c0):
                if (nr,nc) in occupied:
                    bad = True
                    break
            if bad:
                break
        if bad:
            continue
        return cells
    raise RuntimeError("Unable to place ship after many attempts")


def generate_bot_ships():
    occupied: Set[Tuple[int,int]] = set()
    ships: Dict[int, dict] = {}
    sid = 1
    for size in REQUIRED_SIZES:
        cells = place_ship_random(size, occupied)
        for c in cells:
            occupied.add(c)
        ships[sid] = {'size': size, 'cells': cells}
        sid += 1
    lines = []
    for sid, s in ships.items():
        coords = [rc_to_label(r,c) for r,c in s['cells']]
        lines.append(f"{sid},{s['size']},{' '.join(coords)}")
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Saved bot ships to {DATA_PATH}")
    return ships