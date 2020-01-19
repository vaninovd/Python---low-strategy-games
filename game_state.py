class GameState():
    current_player: str
    possible_moves: list
    gameOver: bool
    current_value: object

    def __init__(self) -> None:
        """
        Initialize a game state for Any Game
        """
        self.possible_moves = []
        return

    def __repr__(self) -> str:
        """
        Return a string representation of the current state
        """
        raise NotImplementedError

    def get_possible_moves(self) -> list:
        """
        Get all of the possible moves for the current player playing
        """
        raise NotImplementedError

    def is_valid_move(self, move_to_make) -> bool:
        """
        Return whether the move to make is a valid move
        """
        if move_to_make in self.possible_moves:
            return True
        else:
            return False

    def get_current_player_name(self)  -> str:
        return self.current_player

    def make_move(self, move_to_make) -> object:
        raise NotImplementedError
