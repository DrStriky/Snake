import numpy as np

from game import Game
from pygame_interactions import PygameInteractions
import pygame
from pytorch_interactions import PyGamePyTorchInteractionHandler
from pytorch_player import PyTorchPlayer


def edge_mask(x: np.ndarray):
    mask = np.ones(x.shape, dtype=bool)
    mask[x.ndim * (slice(1, -1),)] = False
    return mask


def main():
    width = 15
    height = 10
    block_size = 25
    board_dim = (width+2, height+2)  # +2 for the borders in each direction
    dummy = np.zeros(board_dim, dtype=int)
    dummy[edge_mask(dummy)] = 1

    pygame.init()
    pygame.font.init()

    display = pygame.display.set_mode((board_dim[0] * block_size, board_dim[1] * block_size))
    our_player = PyTorchPlayer()
    interacter = PyGamePyTorchInteractionHandler(player=our_player, display=display, block_length=block_size,
                                                 ticks_per_second=5)

    game = Game(dummy, 25, (3, 3), (3, 10), 42)

    game.run_game(interacter)


if __name__ == "__main__":
    main()
