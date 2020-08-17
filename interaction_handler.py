import numpy as np
from typing import TypedDict, Literal


class BoardEncodingDict(TypedDict):
    """
    TypedDict class for encoding of different elements in board
    """
    head: int
    wall: int
    valid: int
    snake: int
    food: int


direction = Literal[(0, 1), (1, 0), (0, -1), (-1, 0)]


class InteractionHandler:
    """
    Informal interface for handling GUI and user interactions.
    """
    def get_encoding_dict(self) -> BoardEncodingDict:
        """Returns the encoding for different board elements."""
        pass

    def draw_board(self, geometry_matrix: np.array, current_score: int) -> None:
        """Updates the GUI for the next tick."""
        pass

    def get_interaction(self) -> direction:
        """Waits for player's input and returns the moving direction for the next snake"""
        pass
