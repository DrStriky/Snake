from typing import Tuple

import numpy as np


class Board(object):
    """
    Model of gaming board.

    :ivar board_matrix: matrix of the playing field; 0 = valid; 1 = invalid
    """

    def __init__(self, board_matrix: np.ndarray):
        self.board_matrix = np.ones((board_matrix.shape[0]+4, board_matrix.shape[1]+4), dtype=int)
        self.board_matrix[2:-2, 2:-2] = board_matrix

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

    # old and unused but maybe useful in the future
    @staticmethod
    def edge_mask(x: np.ndarray):
        mask = np.ones(x.shape, dtype=bool)
        mask[x.ndim * (slice(2, -2),)] = False
        return mask
