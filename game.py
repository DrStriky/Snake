from typing import Tuple, List, Optional
import numpy as np
from snake import Snake
from board import Board
from food import Apple


def edge_mask(x: np.ndarray):
    mask = np.ones(x.shape, dtype=bool)
    mask[x.ndim * (slice(1, -1),)] = False
    return mask


def main():
    board_dim = (15+2, 20+2)  # +2 for the borders in each direction
    dummy = np.zeros(board_dim, dtype=int)
    dummy[edge_mask(dummy)] = 1

    board = Board(dummy, 25)

    print(board.check_border_collision((2, 4)))
    print(board.check_border_collision((0, 3)))
    print(board.check_border_collision((4, 0)))


if __name__ == "__main__":
    main()
