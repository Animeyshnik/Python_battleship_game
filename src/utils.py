import string
from typing import List, Tuple, Set, Dict

ROWS = list(string.ascii_uppercase[:10])  # A-J
COLS = list(range(1, 11))  # 1-10

rows = ROWS
cols = COLS

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < 10 and 0 <= c < 10

def rc_to_label(r: int, c: int) -> str:
    return f"{ROWS[r]}{c+1}"

def label_to_rc(label: str) -> Tuple[int, int]:
    label = label.strip().upper()
    if len(label) < 2:
        raise ValueError("Invalid coordinate")
    row = label[0]
    col = int(label[1:])
    r = ROWS.index(row)
    c = col - 1
    if not in_bounds(r, c):
        raise ValueError("Coordinate out of bounds")
    return r, c

def neighbors8(r: int, c: int):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc):
                yield nr, nc

def neighbors4(r: int, c: int):
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc):
            yield nr, nc

def ship_cells_from_labels(labels: List[str]):
    return [label_to_rc(l) for l in labels]

def cells_adjacent_any(ship_cells: List[Tuple[int,int]], all_other_cells: Set[Tuple[int,int]]) -> bool:
    for (r, c) in ship_cells:
        for nr, nc in neighbors8(r, c):
            if (nr, nc) in all_other_cells:
                return True
    return False

def serialize_ships(ships: Dict[int, dict]) -> str:
    lines = []
    for sid, s in ships.items():
        coords = [rc_to_label(r, c) for (r, c) in s['cells']]
        lines.append(f"{sid},{s['size']},{' '.join(coords)}")
    return "\n".join(lines)

def deserialize_ships(text: str):
    ships = {}
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        sid, size, coords_s = line.split(',', 2)
        coords = coords_s.strip().split()
        ships[int(sid)] = {
            'size': int(size),
            'cells': ship_cells_from_labels(coords)
        }
    return ships