from typing import Tuple
import numpy as np


class Board(object):
    """
    Model of gaming board.

    :ivar board_matrix: matrix of the playing field; 0 = valid; 1 = invalid
    :ivar cube_size: size of one board position
    """

    def __init__(self, board_matrix: np.ndarray, cube_size: int):
        self.board_matrix = board_matrix
        self.cube_size = cube_size

    def check_border_collision(self, new_head: Tuple[int, int]) -> bool:
        """
        Check if new coordinate (new_head) is on valid grid point on the board

        :param new_head: new coordinate to check against the valid points

        :return: True if a collision happened, False if new_head is within the field
        """
        if new_head < self.board_matrix.shape:  # Check if coordinates are valid
            if self.board_matrix[new_head] == 1:
                return True
            else:
                return False
