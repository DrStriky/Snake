from typing import Tuple, List, Optional
import numpy as np

from game import Game
from interaction_handler import InteractionHandler



def edge_mask(x: np.ndarray):
    mask = np.ones(x.shape, dtype=bool)
    mask[x.ndim * (slice(1, -1),)] = False
    return mask


def main():
    board_dim = (15+2, 20+2)  # +2 for the borders in each direction
    dummy = np.zeros(board_dim, dtype=int)
    dummy[edge_mask(dummy)] = 1

    interaction_handler = InteractionHandler()
    game = Game(dummy, 25, (3, 3), (3, 10), 42)

    game.run_game(interaction_handler)


if __name__ == "__main__":
    main()
