from quarto.game_setup import GameEngine

def main() -> None:
    game_engine = GameEngine()

    game_engine.print_game_instructions()

    player_1_name = input("Enter the name of player 1: ")
    player_2_name = input("Enter the name of player 2: ")

    game_engine.run_game(player_1_name, player_2_name)

if __name__ == "__main__":
    main()
