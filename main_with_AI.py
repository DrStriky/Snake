import random

import numpy as np
import pygame

from game import Game
from pytorch_interactions import PyGamePyTorchInteractionHandler
from pytorch_player import PyTorchPlayer


def edge_mask(x: np.ndarray):
    mask = np.ones(x.shape, dtype=bool)
    mask[x.ndim * (slice(1, -1),)] = False
    return mask


def main():
    # Define board
    width = 15
    height = 10
    block_size = 25

    dummy = np.zeros((height+2, width+2), dtype=int)
    dummy[edge_mask(dummy)] = 1

    # init pygame display
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Snake  (By Jonathan & Florian)')
    display = pygame.display.set_mode([dummy.shape[1]*block_size, dummy.shape[0]*block_size])

    # set up player
    ai_player = PyTorchPlayer()
    interacter = PyGamePyTorchInteractionHandler(player=ai_player, display=display, block_length=block_size,
                                                 ticks_per_second=2000)
    ai_player.encoding = interacter.get_encoding_dict()

    total_score = 0
    record = 0
    while True:
        # initialise game ...... should be done in ini of game
        snake_start_pos = (3, 3)
        valid_pos = [tuple(coord) for coord in np.argwhere(dummy == 0).tolist()]
        valid_pos.remove(snake_start_pos)
        food_start_pos = valid_pos[random.randint(0, len(valid_pos) - 1)]

        game = Game(dummy, snake_start_pos, food_start_pos, 42)
        ai_player.counter_move = 0
        game.run_game(interacter)

        total_score += game.game_score
        ai_player.closing_action()
        print('Game:', ai_player.counter_games, '\tScore:', game.game_score,  '\tTurns:', ai_player.counter_move)
        if game.game_score > record:
            record = game.game_score
        print('Record:\t\t\t', record)


if __name__ == "__main__":
    main()
