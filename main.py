from quarto.game_setup import GameEngine

def main() -> None:
    game_engine = GameEngine()
    # Print game instructions before getting player names
    game_engine.print_game_instructions()

    player_1_name = input("Enter the name of player 1: ")
    player_2_name = input("Enter the name of player 2: ")

    # It's surprising to me that there's both a start_game and a run_game method -- it's unclear to me what the difference would be
    game_engine.start_game(player_1_name, player_2_name)
    game_engine.run_game()

if __name__ == "__main__":
    main()
