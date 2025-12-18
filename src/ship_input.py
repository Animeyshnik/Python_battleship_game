from typing import Dict
from .utils import *
import os

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def draw_board(ship_cells):
    board = [["." for _ in range(10)] for _ in range(10)]
    for (r, c) in ship_cells:
        board[r][c] = "■"
    print("\nYour current board:")
    print("   1 2 3 4 5 6 7 8 9 10")
    for i, row in enumerate(board):
        print(f"{ROWS[i]}  " + " ".join(row))
    print()

def validate_and_build(ships_input):
    ships = {}
    all_cells = set()
    ship_id = 1

    for size, labels in ships_input:
        cells = ship_cells_from_labels(labels)

        rows_ = sorted(c[0] for c in cells)
        cols_ = sorted(c[1] for c in cells)
        if not (
            (len(set(rows_)) == 1 and cols_ == list(range(cols_[0], cols_[0] + size)))
            or
            (len(set(cols_)) == 1 and rows_ == list(range(rows_[0], rows_[0] + size)))
        ):
            raise ValueError(f"Ship {labels} is not straight or wrong length")

        if cells_adjacent_any(cells, all_cells):
            raise ValueError(
                f"WARNING: Ship {labels} touches another ship! Please choose other coordinates."
            )

        ships[ship_id] = {"size": size, "cells": cells}
        ship_id += 1
        all_cells.update(cells)

    return ships

def get_player_ships() -> Dict[int, dict]:
    ships_input = []

    for size in SHIP_SIZES:
        while True:
            print(f"Enter ship of size {size}: ", end="")
            raw = input().strip().upper().split()

            if len(raw) != size:
                print(f"Expected {size} coordinates, got {len(raw)}")
                continue

            try:
                preview_cells = ship_cells_from_labels(raw)
                draw_board([c for _, cells in ships_input for c in ship_cells_from_labels(cells)] + preview_cells)
                ships_input.append((size, raw))

                validate_and_build(ships_input)  # temporary validation
                break
            except Exception as e:
                print("ERROR:", e)
                print("Try again.")
                continue

    ships = validate_and_build(ships_input)

    os.makedirs("data", exist_ok=True)
    with open("data/player_ships.csv", "w") as f:
        f.write(serialize_ships(ships))

    print("Player ships saved!\n")
    return ships