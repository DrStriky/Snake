import numpy as np

from game import Game
from pygame_interactions import PygameInteractions
import pygame
import random


def edge_mask(x: np.ndarray):
    mask = np.ones(x.shape, dtype=bool)
    mask[x.ndim * (slice(1, -1),)] = False
    return mask


def main():
    # Define board
    width = 8
    height = 5
    block_size = 25

    dummy = np.zeros((height+2, width+2), dtype=int)
    dummy[edge_mask(dummy)] = 1

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Snake  (By Jonathan & Florian)')
    display = pygame.display.set_mode([dummy.shape[1]*block_size, dummy.shape[0]*block_size])

    interactor = PygameInteractions(display=display, block_length=block_size, ticks_per_second=5)

    snake_start_pos = (3, 3)
    valid_pos = [tuple(coord) for coord in np.argwhere(dummy == 0).tolist()]
    valid_pos.remove(snake_start_pos)
    food_start_pos = valid_pos[random.randint(0, len(valid_pos) - 1)]

    game = Game(dummy, snake_start_pos, food_start_pos, 42)

    game.run_game(interactor)


if __name__ == "__main__":
    main()
