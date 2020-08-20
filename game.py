import random
from typing import Tuple

import numpy as np

from board import Board
from food import Apple
from interaction_handler import InteractionHandler
from snake import Snake


class Game:
    """
    Model of the snake game.
    update for each 'tick' in a game.
        * checks for various collisions
    check for user update
    draw the game HOW????

    :ivar game_score: current score of the snake
    :ivar board: instance of class board
    :ivar snake: instance of the snake
    :ivar food: instance of the food
    """

    def __init__(self, board_dim: np.ndarray, snake_start: Tuple[int, int], food_start: Tuple[int, int], random_seed: int):
        self.game_score = 0
        self.board = Board(board_dim)
        self.snake = Snake([snake_start])
        self.food = Apple(food_start)

        self.random = random.Random(random_seed)

    def run_game(self, interaction_handler: InteractionHandler) -> None:
        """
        Updates the current score using the discount function.

        :return:
        """
        alive = True
        eaten = False

        while alive:
            occupying_matrix = self.get_occupying_matrix(interaction_handler)
            interaction_handler.push_board_status(occupying_matrix, self.snake.get_moving_direction(),
                                                  self.game_score, self.food.get_score())
            self.snake.change_moving_direction(interaction_handler.get_interaction())

            # Get probable new position of snake (head) and check for validity
            new_position = self.snake.get_propagated_head()
            if self.board.check_border_collision(new_position):
                alive = False
                print('Your snake touched the wall!')
            if new_position == self.food.position:
                eaten = True
                print('Your snake has eaten.')

            # Update all game elements
            if not self.snake.update(eaten):
                alive = False
                print('Your snake touched itself!')

            if eaten:
                self.game_score += self.food.score
                valid_fields = [tuple(coord) for coord in np.argwhere(occupying_matrix == interaction_handler.get_encoding_dict()['valid']).tolist()]
                self.food = Apple(self.random.choice(valid_fields))
                occupying_matrix = self.get_occupying_matrix(interaction_handler)
                eaten = False
            else:
                self.food.update()

        interaction_handler.push_board_status(occupying_matrix, self.snake.get_moving_direction(),
                                              self.game_score, self.food.get_score())
        print(f'\nYour final score is {self.game_score}')

    def get_occupying_matrix(self, interaction_handler: InteractionHandler) -> np.array:
        symbols = interaction_handler.get_encoding_dict()
        occupying_matrix = np.copy(self.board.board_matrix)

        occupying_matrix[occupying_matrix == 1] = symbols['wall']
        occupying_matrix[occupying_matrix == 0] = symbols['valid']

        if self.snake.body[0:-1]:  # just print body of snake if there is one
            occupying_matrix[tuple(np.array(self.snake.body[0:-1]).T)] = symbols['snake']
        occupying_matrix[self.snake.body[-1]] = symbols['head']
        occupying_matrix[self.food.position] = symbols['food']

        return occupying_matrix
