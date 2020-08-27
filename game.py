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

    def __init__(self, board_dim: np.ndarray, snake_start: Tuple[int, int] = None, food_start: Tuple[int, int] = None, random_seed: int = 42):
        self.game_score = 0
        self.random = random.Random(random_seed)
        self.board = Board(board_dim)

        if snake_start is None:
            self.snake = Snake([self.seed_element()])
        else:
            self.snake = Snake([snake_start])

        if food_start is None:
            self.food = Apple(self.seed_element())
        else:
            self.food = Apple(food_start)

    def seed_element(self) -> Tuple[int, int]:
        valid_fields = [tuple(coord) for coord in np.argwhere(self.board.board_matrix == 0).tolist()]

        occupied_fields = []
        if hasattr(self, 'snake'):
            occupied_fields = occupied_fields+self.snake.body
        if hasattr(self, 'food'):
            occupied_fields = occupied_fields + [self.food.position]

        free_fields = [item for item in valid_fields if item not in occupied_fields]

        return self.random.choice(free_fields)

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
                self.food = Apple(self.seed_element())
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
