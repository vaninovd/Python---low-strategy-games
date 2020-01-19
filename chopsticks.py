
from game_state import GameState

class ChopsticksCurrentState(GameState):

    current_value: list

    def __init__(self) -> None:
        """
        Initialize a game state for Any Game
        """
        GameState.__init__(self)

    def __repr__(self) -> str:
        """
        Return a string representation of the Current State
        """
        return 'Current Player Playing: {}, Player 1: {}-{};' \
               ' Player 2: {}-{}'.format(self.current_player, self.current_value[0],
                                                         self.current_value[1],
                                                         self.current_value[2],
                                                         self.current_value[3])

    def get_possible_moves(self) -> list:
        """
        Return a list of all the possible moves available
        for the current player
        """
        if self.current_player == "p1" :
            if self.current_value[0] == 0 and self.current_value[1] == 0:
                self.possible_moves = []
            elif self.current_value[0] == 0 and self.current_value[2] == 0:
                self.possible_moves = ["rr"]
            elif self.current_value[0] == 0 and self.current_value[3] == 0:
                self.possible_moves = ["rl"]
            elif self.current_value[1] == 0 and self.current_value[2] == 0:
                self.possible_moves = ["lr"]
            elif self.current_value[1] == 0 and self.current_value[3] == 0:
                self.possible_moves = ["ll"]
            elif self.current_value[2] == 0 and self.current_value[3] == 0:
                self.possible_moves = []
            elif self.current_value[0] == 0:
                self.possible_moves = ["rl", "rr"]
            elif self.current_value[1] == 0:
                self.possible_moves = ["ll", "lr"]
            elif self.current_value[2] == 0:
                self.possible_moves = ["lr", "rr"]
            elif self.current_value[3] == 0:
                self.possible_moves = ["ll", "rl"]
            else:
                self.possible_moves = ["rl", "rr", "lr", "ll"]

        elif self.current_player == "p2":
            if self.current_value[0] == 0 and self.current_value[1] == 0:
                self.possible_moves = []
            elif self.current_value[0] == 0 and self.current_value[2] == 0:
                self.possible_moves = ["rr"]
            elif self.current_value[0] == 0 and self.current_value[3] == 0:
                self.possible_moves = ["lr"]
            elif self.current_value[1] == 0 and self.current_value[2] == 0:
                self.possible_moves = ["rl"]
            elif self.current_value[1] == 0 and self.current_value[3] == 0:
                self.possible_moves = ["ll"]
            elif self.current_value[2] == 0 and self.current_value[3] == 0:
                self.possible_moves = []
            elif self.current_value[0] == 0:
                self.possible_moves = ["lr", "rr"]
            elif self.current_value[1] == 0:
                self.possible_moves = ["ll", "rl"]
            elif self.current_value[2] == 0:
                self.possible_moves = ["rr", "rl"]
            elif self.current_value[3] == 0:
                self.possible_moves = ["ll", "lr"]
            else:
                self.possible_moves = ["rl", "rr", "lr", "ll"]

        return self.possible_moves

    def make_move(self, move_to_make) -> object:
        """
        Make a move and create a new current state
        """

        # Making a new current state to return
        new_current_player = "p2"
        if self.current_player == 'p1':
            new_current_player = "p2"
        else:
            new_current_player = "p1"

        new_current_value = []
        for value in self.current_value:
            new_current_value.append(value)

        if move_to_make == 'll':
            sum = self.current_value[0] + self.current_value[2]
            if self.current_player == "p1":
                if sum > 5:
                    new_current_value[2] = sum - 5
                elif sum == 5:
                    new_current_value[2] = 0
                else:
                    new_current_value[2] = sum
            elif self.current_player == "p2":
                if sum > 5:
                    new_current_value[0] = sum - 5
                elif sum == 5:
                    new_current_value[0] = 0
                else:
                    new_current_value[0] = sum
        elif move_to_make == 'lr':
            if self.current_player == "p1":
                sum = self.current_value[0] + self.current_value[3]
                if sum > 5:
                    new_current_value[3] = sum - 5
                elif sum == 5:
                    new_current_value[3] = 0
                else:
                    new_current_value[3] = sum
            elif self.current_player == "p2":
                sum = self.current_value[1] + self.current_value[2]
                if sum > 5:
                    new_current_value[1] = sum - 5
                elif sum == 5:
                    new_current_value[1] = 0
                else:
                    new_current_value[1] = sum
        elif move_to_make == 'rl':
            if self.current_player == "p1":
                sum = self.current_value[1] + self.current_value[2]
                if sum > 5:
                    new_current_value[2] = sum - 5
                elif sum == 5:
                    new_current_value[2] = 0
                else:
                    new_current_value[2] = sum
            elif self.current_player == "p2":
                sum = self.current_value[3] + self.current_value[0]
                if sum > 5:
                    new_current_value[0] = sum - 5
                elif sum == 5:
                    new_current_value[0] = 0
                else:
                    new_current_value[0] = sum
        elif move_to_make == 'rr':
            sum = self.current_value[1] + self.current_value[3]
            if self.current_player == "p1":
                if sum > 5:
                    new_current_value[3] = sum - 5
                elif sum == 5:
                    new_current_value[3] = 0
                else:
                    new_current_value[3] = sum
            elif self.current_player == "p2":
                if sum > 5:
                    new_current_value[1] = sum - 5
                elif sum == 5:
                    new_current_value[1] = 0
                else:
                    new_current_value[1] = sum




        new_gameover_status = False
        if (new_current_value[0] == 0 and new_current_value[1] == 0) or \
                (new_current_value[2] == 0 and new_current_value[3] == 0) :
            new_gameover_status = True

        # We make a new object and fill it in with the correct values
        new_current_state = ChopsticksCurrentState()
        new_current_state.current_player = new_current_player
        new_current_state.current_value = new_current_value
        new_current_state.possible_moves = new_current_state.get_possible_moves()
        new_current_state.gameOver = new_gameover_status

        return new_current_state

class Chopsticks():

    instructions = "1. Each of two players begins with one finger pointed up on each of their hands." \
                   " 2. Player A touches one hand to one of Player B's hands, increasing the number of fingers pointing up" \
                   "on Player B's hand by the number on Player A's hand. The number pointing up on Player A's hand" \
                   "remains the same." \
                   " 3. If Player B now has five fingers up, that hand becomes \dead or unplayable. If the number of finngers should exceed five, subtract five from the sum." \
                   " 4. Now Player B touches one hand to one of Player A's hands, and the distribution of fingers proceeds" \
                   "as above, including the possibility of a \dead hand. 5. Play repeats steps 2{4 until some player has two \dead" \
                   " hands, thus losing. These instructions are taken from http://www.cdf.utoronto.ca/~csc148h/winter/A1/a1.pdf"

    current_state = ChopsticksCurrentState
    is_p1_turn: bool

    def __init__(self, is_p1_turn) -> None:
        """
        Initialize tha game Chopsticks
        """

        self.current_state = ChopsticksCurrentState()

        # Assuming this is the first creation of the object
        # Therefore manually initializing and querying user

        # Choose a player
        current_player = "p2"
        if is_p1_turn:
            current_player = "p1"

        # Set the current player
        self.current_state.current_player = current_player

        # Current value is set in the beginnig of the game
        current_value = [1, 1, 1, 1]

        # Obtained a sucessful user input - put it into the current state
        self.current_state.current_value = current_value

        # Use the current value to get the possibe moves
        self.current_state.possible_moves = self.current_state.get_possible_moves()

        # Set the victory condition to false
        if (self.current_state.current_value[0] == 0 and
            self.current_state.current_value[1] == 0) or \
                (self.current_state.current_value[2] == 0 and
                 self.current_state.current_value[3] == 0) :
            self.current_state.gameOver = True
        else:
            self.current_state.gameOver = False

        return

    def str_to_move(self, move) -> str:
        """
        Return the  str to move in the correct type
        """
        return move


    def get_instructions(self) -> str:
        """
        Return full instructions of the game
        """
        return self.instructions

    def is_over(self, current_state) -> bool:
        """
        Return whether the Game is over
        """
        return current_state.gameOver

    def is_winner(self, player_string) -> bool:
        """
        Return whether the player is winner
        """
        if not (self.current_state.current_value[0] == 0 and
                self.current_state.current_value[1] == 0) or \
                (self.current_state.current_value[2] == 0 and
                 self.current_state.current_value[3] == 0):
            return False
        if player_string == self.current_state.current_player:
            return False
        else:
            return True
