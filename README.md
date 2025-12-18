# Battleship — simplified classic

## How to run

1. Create a project folder and copy files.
2. Make sure you have Python 3.8+.
3. Run:
```bash
python main.py
```

## Input format (player ships)
When prompted input each ship as space-separated coordinates. Example for a size-4 ship:
```
A1 A2 A3 A4
```
Order of required ships: `4,3,3,2,2,2,1,1,1,1`.

## Validation rules
- Ships must be in straight lines (horizontal or vertical), contiguous, correct sizes.
- Ships must not touch another ship even diagonally.
- Ships must be within board rows `A-J` and columns `1-10`.

If validation fails you'll be asked to re-enter the ship.

## CSV formats
- `data/player_ships.csv` and `data/bot_ships.csv` — lines like:
```
1,4,A1 A2 A3 A4
2,3,B1 B2 B3
```
- `data/game_state.csv` contains per-turn snapshots with player & bot moves and compact boards.

## Gameplay and design decisions
- Boards are 10x10, rows A-J, columns 1-10.
- Player input is interactive for clarity.
- Bot generation places ships randomly and ensures no adjacency.
- Bot AI implements random fire, follow-ups after a hit, and axis locking after second hit.
- When a ship is sunk, surrounding cells are marked as misses automatically for clarity and to follow the rule.

## Notes & improvements
- The project is kept dependency-free.
- You can modify serialization formats or provide a file-based player setup for non-interactive runs.
```

