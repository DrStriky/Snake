from typing import Tuple, Type
import numpy as np

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

    def __init__(self, board_dim: np.ndarray, snake_start: Tuple[int, int], food_start: Tuple[int, int]):
        self.game_store = 0
        self.board = Board(board_dim)
        self.snake = Snake(snake_start)
        self.food = Apple(food_start)

    def run_game(self, Interaction_Handler: Type[Interaction_Handler]) -> None:
        """
        Updates the current score using the discount function.

        :return:
        """
        inter_handler= Interaction_Handler()

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
            self.food.update()
            self.self.game_store += self.food.score

            snake update
            apple update
            score update

            write new besetzungsmatrix

            next tick

    def get_occupying_matrix():
        print('blavlalv')




