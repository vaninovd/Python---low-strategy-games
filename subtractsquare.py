
from game_state import GameState

class SubtractSquareCurrentState(GameState):

    current_value: int
    def __init__(self) -> None:
        """
        Create a current state for Subtract square
        """
        GameState.__init__(self)

    def __repr__(self) -> str:
        """
        Return a string representation of the current state
        """
        return 'Current Player: {}, Current value: {}'.format(
            self.current_player, self.current_value)

    def get_possible_moves(self) -> list:
        """
        Return a list of all the possible moves available for the playing player
        """
        list_of_moves = list(range(1, int(self.current_value ** 0.5) + 1))
        self.possible_moves = [x ** 2 for x in list_of_moves]
        return self.possible_moves

    def make_move(self, move_to_make) -> object:
        """
        Make a move and create a new state for the game
        """

        # Making a new current state to return
        new_current_player = "p2"
        if self.current_player == 'p1':
            new_current_player = "p2"
        else:
            new_current_player = "p1"

        new_current_value = self.current_value - (move_to_make)

        new_gameover_status = False
        if new_current_value == 0:
            new_gameover_status = True

        # We make a new object and fill it in with the correct values
        new_current_state = SubtractSquareCurrentState()
        new_current_state.current_player = new_current_player
        new_current_state.current_value = new_current_value
        new_current_state.possible_moves = new_current_state.get_possible_moves()
        new_current_state.gameOver = new_gameover_status

        return new_current_state

class SubtractSquare():

    instructions = "1. A non-negative whole number is chosen as the starting value by some neutral entity. In our case, a" \
                   "player will choose it (i.e. through the use of input())." \
                   " 2. The player whose turn it is chooses some square of a positive whole number (such as 1, 4, 9, 16, . . . )" \
                   "to subtract from the value, provided the chosen square is not larger. After subtracting, we have a new" \
                   "value and the next player chooses a square to subtract from it." \
                   " 3. Play continues to alternate between the two players until no moves are possible. Whoever is about to" \
                   "play at that point loses!" \
                   " These instructions are taken from http://www.cdf.utoronto.ca/~csc148h/winter/A1/a1.pdf"

    current_state = SubtractSquareCurrentState

    def __init__(self, is_p1_turn) -> None:
        """
        Initialize the Game Subtract Square
        """

        self.current_state = SubtractSquareCurrentState()

        # Assuming this is the first creation of the object
        # Therefore manually initializing and querying user

        # Choose a player
        current_player = "p2"
        if is_p1_turn:
            current_player = "p1"

        # Set the current player
        self.current_state.current_player = current_player

        # No current value - user puts in a current value
        current_value = int(input("Please enter a number that is non-negative: "))

        # Obtained a sucessful user input - put it into the current state
        self.current_state.current_value = current_value

        # Use the current value to get the possibe moves
        self.current_state.possible_moves = self.current_state.get_possible_moves()

        # Set the victory condition to false
        if self.current_state.current_value == 0:
            self.current_state.gameOver = True
        else:
            self.current_state.gameOver = False

        return

    def str_to_move(self, move) -> int:
        """
        Return str to move in the correct type
        """
        return int(move)


    def get_instructions(self) -> str:
        """
        Return full instructions of the game
        """
        return self.instructions

    def is_over(self, current_state) -> bool:
        """
        Return whether the game is over
        """
        return current_state.gameOver

    def is_winner(self, player_string) -> bool:
        """
        Return whether player is winner
        """
        if self.current_state.current_value != 0:
            return False
        if player_string != self.current_state.current_player:
            return True
        else:
            return False








