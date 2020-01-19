from typing import Any
import random
# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Any) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

def random_strategy(game: Any) -> Any:
    """
    Return a random move
    """
    moves = game.current_state.get_possible_moves()
    return random.choice(moves)

