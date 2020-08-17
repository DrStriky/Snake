from typing import Tuple, Type
import numpy as np
import random

from snake import Snake
from board import Board
from food import Apple
from interaction_handler import Interaction_Handler


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

    def __init__(self, board_dim: np.ndarray, cube_size: int, snake_start: Tuple[int, int], food_start: Tuple[int, int], random_seed: int):
        self.game_score = 0
        self.board = Board(board_dim, cube_size)
        self.snake = Snake([snake_start])
        self.food = Apple(food_start)

        self.random = random.Random(random_seed)

    def run_game(self, interaction_handler: Type[Interaction_Handler]) -> None:
        """
        Updates the current score using the discount function.

        :return:
        """
        alive = True
        inter_handler = interaction_handler()

        while alive:
            eaten = False
            # TODO inter_handler.probable wait()

            self.snake.change_moving_direction(inter_handler.get_interaction())

            # Get probable new position of snake (head) and check for validity
            new_position = self.snake.get_propagated_head()
            if self.board.check_border_collision(new_position):
                alive = False
                print('Your snake touched the wall!')
            if new_position == self.food.position:
                eaten = True
                print('Your snake has eaten.')

            # Update all game elements
            if self.snake.update(eaten):
                alive = False
                print('Your snake touched itself!')
            if eaten:
                self.game_score += self.food.score
                self.food = Apple((self.random.randint(1, self.board.board_matrix.shape[0]), self.random.randint(1, self.board.board_matrix.shape[1])))  # TODO random position for new food
            else:
                self.food.update()

            # TODO write new Besetzungsmatrix

    def get_occupying_matrix(self):
        self.board.board_matrix
        self.snake.body
        self.food.position
        return self
