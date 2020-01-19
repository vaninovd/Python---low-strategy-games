"""
Stonehenge Game classes
"""
from typing import Any
import math
import copy
from game import Game
from game_state import GameState

class StonehengeState(GameState):
    """
    A class for the current state of the Stonehenge Game
    which is a sublcass of GameState
    """
    ley_lines: list
    horizontal_rows: list
    upper_diagonal_rows: list
    lower_diagonal_rows: list

    def __init__(self, is_p1_turn: bool, board_size: int) -> None:
        """
        Initialize a Game State for Stonehenge Game and set
        the current platyer based on the is_p1_turn
        """
        super().__init__(is_p1_turn)
        self.current_player = "p2"
        if self.p1_turn:
            self.current_player = "p1"
        self.board_size = board_size
        s = self.board_size
        self.ley_lines = create_ley_lines(s)
        self.horizontal_rows = create_vertical_rows(s)
        self.upper_diagonal_rows = create_upper_diagonal_rows(s)
        self.lower_diagonal_rows = create_lower_diagonal_rows(s)

    def __str__(self) -> str:
        """
        Return a string representation of the current state
        of the Game Stonehenge
        """

        first_line = "{} {}".format(self.ley_lines[1][0], self.ley_lines[1][1])
        last_line = " ".join(self.ley_lines[2][:-1])
        number_of_following_lines = self.board_size + 1
        following_lines = ""
        for n in range(number_of_following_lines -2):
            following_lines += "\n" + self.ley_lines[0][n] + " " + \
                               " ".join(self.horizontal_rows[n]) + " " + \
                               self.ley_lines[0][n+2]
        following_lines += "\n" + self.ley_lines[0][-2] + " " + \
                           " ".join(self.horizontal_rows[-2])
        following_lines += "\n" + self.ley_lines[0][-1] + " " + " ".join(
            self.horizontal_rows[-1])
        following_lines += " " + self.ley_lines[2][-1]
        final_string = ""
        final_string += first_line + following_lines + "\n" +last_line

        return final_string
    def get_possible_moves(self) -> list:
        """
        Return all possible moves for the current state
        """
        one = 0
        two = 0
        winning_num = math.ceil(((self.board_size + 1) * 3) / 2)
        for row in self.ley_lines:
            one += row.count("1")
            two += row.count("2")
        if one >= winning_num or two >= winning_num:
            return []

        letters = []
        for row in self.horizontal_rows:
            for letter in row:
                if letter.isalpha():
                    letters.append(letter)
        return letters


    def make_move(self, move: str) -> "StonehengeState":
        """
        Return the game state that results from applyong the move to the current
        state
        """

        new_ley_lines = copy.deepcopy(self.ley_lines)
        new_vertical_rows = copy.deepcopy(self.horizontal_rows)
        new_upper_diagonal_rows = copy.deepcopy(self.upper_diagonal_rows)
        new_lower_diagonal_rows = copy.deepcopy(self.lower_diagonal_rows)
        cur_player = self.current_player
        new_vertical_rows = claim_rows(new_vertical_rows, move, cur_player)
        new_upper_diagonal_rows = claim_rows(new_upper_diagonal_rows, move,
                                             cur_player)
        new_lower_diagonal_rows = claim_rows(new_lower_diagonal_rows, move,
                                             cur_player)
        new_ley_lines = claim_ley_lines(new_vertical_rows, new_ley_lines,
                                        cur_player, 0)
        new_ley_lines = claim_ley_lines(new_upper_diagonal_rows, new_ley_lines,
                                        cur_player, 1)
        new_ley_lines = claim_ley_lines(new_lower_diagonal_rows, new_ley_lines,
                                        cur_player, 2)

        new_state = StonehengeState(not self.p1_turn, self.board_size)
        new_state.ley_lines = new_ley_lines
        new_state.horizontal_rows = new_vertical_rows
        new_state.upper_diagonal_rows = new_upper_diagonal_rows
        new_state.lower_diagonal_rows = new_lower_diagonal_rows

        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        """
        return "Current player playing {}. All the possible moves available" \
               "for this player are {}. Occupation of ley-lines is the " \
               "following " \
               "{}".format(self.current_player, self.get_possible_moves(),
                           self.ley_lines)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        """

        secondary_states = [self.make_move(move) for move in
                            self.get_possible_moves()]

        for state in secondary_states:
            if state.get_possible_moves() == []:
                return self.WIN

        losses = 0
        for second_state in secondary_states:
            final_states = [second_state.make_move(move) for move
                            in self.get_possible_moves()]
            for _state in final_states:
                if _state.get_possible_moves() == []:
                    losses += 1

        if len(secondary_states) == losses:
            return self.LOSE

        return self.DRAW


class StonehengeGame(Game):
    """
    A class for stonehenge game which is a sublclass of Game
    """
    current_state: StonehengeState

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize the Stonehenge Game, using p1_starts to find
        who the first player is
        """
        size_board = int(input("Please insert a board size: "))
        self.current_state = StonehengeState(p1_starts, size_board)

    def get_instructions(self) -> str:
        """
        Return the instructions for Game Stonehenge
        """
        instructions = "Players take turns claiming cells. The first player " \
                       "to claim at least half of the cells in the ley-line, " \
                       "captures the ley-line. The first player to claim at " \
                       "at least half of the ley-lines wins the game."
        return instructions

    def is_over(self, state: GameState) -> bool:
        """
        Return wether or not the game is over at the state
        """
        # Check if half of the ley-lines are climed or not
        one = 0
        two = 0
        winning_num = math.ceil(((state.board_size + 1) * 3)/2)
        for row in state.ley_lines:
            one += row.count("1")
            two += row.count("2")
        if one >= winning_num or two >= winning_num:
            return True
        if state.get_possible_moves() == []:
            return True
        return False

    def is_winner(self, player: str) -> bool:
        """
        Return wether the player has won the game
        """
        return self.is_over(self.current_state) and \
                self.current_state.get_current_player_name() != player


    def str_to_move(self, string: str) -> str:
        """
        Return the move that string represents. If the string is
        not a move return some invalid move
        """

        return string


#HELPER FUNCTIONS -------------------------------------------------------------
#------------------------------------------------------------------------------
def create_ley_lines(size) -> list:
    """
    Create a list of lists of ley-lines
    First list is row ley lines
    Second list is upper_diagonal ley lines
    Third list is lowe_diagonal ley lines

    >>>create_ley_lines(1)
    [['@', '@'], ['@', '@'], ['@', '@']]
    """
    ley_line_markers = []
    i = 0
    while i in range(3):
        ley_line_markers.append(["@"] * (size +1))
        i += 1
    return ley_line_markers

def create_vertical_rows(board_size: int) -> list:
    """
    Return lists of rows with all of the letters in each row

    >>>create_vertical_rows(1)
    [['A', 'B'], ['C']]
    >>>create_vertical_rows(2)
    [['A', 'B'], ['C', 'D', 'E'], ['F', 'G']]
    """
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
               "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
               "Y", "Z"]

    vertical_rows = [["A", "B"]]
    longest_row = board_size + 1
    row_num = 2
    first_letter = 2
    while row_num < longest_row:
        vertical_rows.append(letters[first_letter:first_letter + row_num +1])
        first_letter = first_letter + row_num + 1
        row_num += 1

    vertical_rows.append(letters[first_letter: first_letter + longest_row -1])

    return vertical_rows


def create_upper_diagonal_rows(size: int) -> \
        list:
    """
    Return lists of rows with all of the letters in each
    upper diagonal row.

    >>>create_upper_diagonal_rows(1, list_of_rows(1))
    [['A'], ['B', 'C']]
    >>>create_upper_diagonal_rows(2, list_of_rows(2))
    [['A', 'C'], ['B', 'D', 'F'], ['E', 'G']]
    """
    upper_diagonal_rows = []
    rows = create_vertical_rows(size)
    n = 0
    while n < size + 1:
        l = []
        for row in rows[:size]:
            if n < len(row):
                l.append(row[n])
        upper_diagonal_rows.append(l)
        n += 1

    last_row = rows[-1]
    k = 0
    for row in upper_diagonal_rows[1:]:
        row.append(last_row[k])
        k += 1

    return upper_diagonal_rows

def create_lower_diagonal_rows(size) -> list:
    """
    Retirn lists of rows with all of the letters in each
    lower diagonal row.
    >>>create_lower_diagonal_rows(1, list_of_rows(1))
    [['A', 'C'], ['B']]
    >>>create_lower_diagonal_rows(2, list_of_rows(2))
    [['C', 'F'], ['A', 'D', 'G'], ['B', 'E']]
    """
    lower_diagonal_rows = []
    rows = create_upper_diagonal_rows(size)
    n = 0
    while n < size + 1:
        l = []
        for row in rows[1:]:
            if n < len(row):
                l.append(row[n])
        lower_diagonal_rows.append(l)
        n += 1

    last_row = rows[0]
    k = 0
    for row in lower_diagonal_rows[1:]:
        row.insert(0, last_row[k])
        k += 1

    return lower_diagonal_rows[::-1]

def claim_rows(new_rows, move_, cur_player) -> list:
    """
    Claim all the new vertical rows
    """

    for row in new_rows:
        if move_ in row:
            index_of_letter = row.index(move_)
            if cur_player == "p1":
                row[index_of_letter] = "1"
            else:
                row[index_of_letter] = "2"
    return new_rows

def claim_ley_lines(new_rows, new_ley_lines, cur_player,
                    ind) -> list:
    """
    Return the ley_lines with claimed markers
    """
    def claim(_row, p) -> Any:
        """
        Claim the correct marker
        """
        if _row.count(p) >= math.ceil(len(_row) / 2):
            new_ley_lines[ind][new_rows.index(_row)] = p

    for row in new_rows:
        if not new_ley_lines[ind][new_rows.index(row)].isdigit():
            if cur_player == "p1":
                claim(row, "1")
            elif cur_player == "p2":
                claim(row, "2")


    return new_ley_lines


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
