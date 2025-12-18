from src.ship_input import get_player_ships
from src.bot_generation import generate_bot_ships
from src.gameplay import play_game

def main():
    print("=== Battleship — simplified classic ===")
    print("Board: 10x10. Rows A-J, Columns 1-10.")
    print()

    player_ships = get_player_ships()

    bot_ships = generate_bot_ships()
    play_game(player_ships, bot_ships)
