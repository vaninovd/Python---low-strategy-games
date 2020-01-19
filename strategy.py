"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from game import Game
from game_state import GameState
from stack import Stack


# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Game) -> str:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

def rough_outcome_strategy(game: Game) -> str:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2 # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent

    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move

# TODO: Implement a recursive version of the minimax strategy.

def recursive_minimax(game: Game) -> str:
    """
    Return a move with the highest guaranteed score through the
    implementation of recursion
    """

    def evaluate_state(curr_state: GameState) -> int:
        """
        Evaluate the curr state and return its score
        """
        if game.is_over(curr_state):
            prev_state = game.current_state
            game.current_state = curr_state
            if game.is_winner("p1"):
                if game.current_state.get_current_player_name() == "p1":
                    game.current_state = prev_state
                    return 1
                elif game.current_state.get_current_player_name() == "p2":
                    game.current_state = prev_state
                    return -1
            elif game.is_winner("p2"):
                if game.current_state.get_current_player_name() == "p2":
                    game.current_state = prev_state
                    return 1
                elif game.current_state.get_current_player_name() == "p1":
                    game.current_state = prev_state
                    return -1
            else:
                game.current_state = prev_state
                return 0
        else:
            scores = []
            for move in curr_state.get_possible_moves():
                score = evaluate_state(curr_state.make_move(move)) * -1
                scores.append(score)
            return max(scores)

    states_scores = []
    moves = game.current_state.get_possible_moves()
    for move_ in moves:
        state_score = evaluate_state(game.current_state.make_move(move_)) * -1
        states_scores.append(state_score)
    return moves[states_scores.index(max(states_scores))]


# TODO: Implement an iterative version of the minimax strategy.
def iterative_minimax(game: Game) -> str:
    """
    Return a move with the highest guaranteed score through the
    implementation of iteration
    """

    def evaluate_score_iterative(state: GameState) -> int:
        """
        Evaluate the state and return its score
        """
        # I have used a file from lab 3 that contains class
        # Stack and its funcitons

        def find_add_children(element, container) -> None:
            """
            Find children for a tree state and add it back
            into the stack
            """
            for move in element.cur_state.get_possible_moves():
                child_tree = Tree(element.cur_state.make_move(move))
                element.children.append(child_tree)
                container.add(child_tree)

        stk = Stack()
        tree_state = Tree(state)
        stk.add(tree_state)

        while not stk.is_empty():
            top_element = stk.remove()
            if game.is_over(top_element.cur_state):
                old_state = game.current_state
                game.current_state = top_element.cur_state
                if not (game.is_winner("p1") or game.is_winner("p2")):
                    top_element.state_score = 0
                elif game.is_winner\
                            (top_element.cur_state.get_current_player_name()):
                    top_element.state_score = 1
                else:
                    top_element.state_score = - 1
                game.current_state = old_state
            else:
                if top_element.children == []:
                    stk.add(top_element)
                    find_add_children(top_element, stk)
                else:
                    top_element.state_score = max([-1 *
                                                   child.state_score
                                                   for child in
                                                   top_element.children])
        return tree_state.state_score

    moves = game.current_state.get_possible_moves()
    states_ = [game.current_state.make_move(move) for move in moves]
    scores_ = [-1 * evaluate_score_iterative(state) for state in states_]
    max_index = scores_.index(max(scores_))
    return moves[max_index]

class Tree:
    """
    A node_like tree
    """
    def __init__(self, cur_state: GameState) -> None:
        """
        Create a Tree self with value, o or more children and state
        """
        self.cur_state = cur_state
        self.children = []
        self.state_score = None



if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
