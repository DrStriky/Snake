import numpy as np

from game import Game
from pygame_interactions import PygameInteractions
import pygame
from pytorch_interactions import PyGamePyTorchInteractionHandler
from pytorch_player import PyTorchPlayer
import random


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
    # ToDo: remove this crap that is caused by fucking OS X/PyGame Interaction Error
    for event in pygame.event.get():
        pass

    our_player = PyTorchPlayer()
    interacter = PyGamePyTorchInteractionHandler(player=our_player, display=display, block_length=block_size,
                                                 ticks_per_second=10)
    our_player.encoding = interacter.get_encoding_dict()

    total_score = 0
    while True:
        game = Game(dummy, 25, (3, 3), (random.randint(1,9), random.randint(1,9)), 42)
        our_player.counter_move = 0
        game.run_game(interacter)

        # One game is over, train on the memory and plot the result.
        total_score += game.game_score
        our_player.train_long_memory(our_player.memory)
        print('Game', our_player.counter_games, '      Score:', game.game_score)


    if sc > record:
        record = sc
        name = 'best_model.pth'.format(sc)
        dir = os.path.join(model_folder_path, name)
        torch.save(our_player.model.state_dict(), dir)
    print('record: ', record)
    score_plot.append(sc)
    mean = total_score / agent.counter_games
    mean_plot.append(mean)
    agent.plot(score_plot, mean_plot)

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
