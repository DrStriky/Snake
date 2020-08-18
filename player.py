from typing import Tuple
import numpy as np

class Player:
    """
    Informal Interface for AI player
    """
    def push_board_status(self, occupation_matrix: np.array, moving_direction: Tuple[int, int],
                          score: int, food_score: int) -> None:
        """Player receives new board status"""
        pass

    def get_response(self) -> Tuple[int, int]:
        """Return new moving direction."""
        pass
