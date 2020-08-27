import time

import numpy as np
import pygame

from game import Game
from pytorch_interactions import PyGamePyTorchInteractionHandler
from pytorch_player import PyTorchPlayer

block_size = 25


def main():
    # Define board
    width = 25
    height = 20
    board = np.zeros((height+2, width+2), dtype=int)

    # init pygame display
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Snake AI (By Jonathan & Florian)')

    # set up player
    ai_player = PyTorchPlayer()

    total_score = 0
    record = 0
    while True:
        game = Game(board_dim=board, random_seed=time.time_ns())
        #display = pygame.display.set_mode([game.board.board_matrix.shape[1] * block_size, game.board.board_matrix.shape[0] * block_size])
        #interacter = PyGamePyTorchInteractionHandler(player=ai_player, display=display, block_length=block_size, ticks_per_second=100)
        interacter = PyGamePyTorchInteractionHandler(player=ai_player)
        ai_player.encoding = interacter.get_encoding_dict()
        ai_player.new_round()
        game.run_game(interacter)
        ai_player.closing_action(game.game_score)

        total_score += game.game_score
        if game.game_score > record:
            record = game.game_score
        print('Game:', ai_player.counter_games, '\tScore:', game.game_score, '\tTurns:', ai_player.counter_move)
        print('Record:\t\t\t', record)


if __name__ == "__main__":
    main()
