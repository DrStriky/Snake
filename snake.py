from typing import Tuple, List, Optional, Callable
import numpy as np


class Snake:
    """
    Models the snake in the game.

    :ivar body: coordinates of the snakes body in reverse order (i.e. body[0] is tail, body[-1] is head)
    :ivar moving_direction: (x, y) coordinates of snake's moving direction
    """

    def __init__(self, body: List[Tuple[int, int]]):
        """
        Define snake's initial body and initialize moving direction attribute.
        :param body: List of (x, y) coordinates of snake's initial body
        """
        self.body = body
        self.moving_direction = (0, 9)

    def update(self, got_food: Optional[bool] = False) -> bool:
        """
        Propagates the snake's body by one field in the moving direction. If the snake got food, the body is extended by
        one field.

        :param got_food: True/False to indicate whether body should be extended or not.

        :return: True if propagation was successful, False if snake crashed into it's own body.
        """
        # add propagated head
        new_head = self.get_propagated_head()
        self.body = self.body + [new_head]

        # if snake did not eat, remove tail
        if not got_food:
            del self.body[0]

        # return whether snake crashed into itself
        crashed = new_head in self.body
        return crashed

    def get_propagated_head(self) -> Tuple[int, int]:
        """
        Returns the position of the snake's had after propagation.

        :return: (x, y) of propagated head
        """
        head = self.body[-1]
        return head[0] + self.moving_direction[0], head[1] + self.moving_direction[1]

    def change_moving_direction(self, new_direction: Tuple[int, int]) -> None:
        """
        Updates self.moving_direction with a new direction.

        :param new_direction: (x, y) of new direction
        """
        self.moving_direction = new_direction


class Apple:
    """
    Model of food.

    :ivar position: (x, y) coordinate of apple's position
    :ivar score: current score of food
    :ivar discount_function: function that updates the score after each round (penalty for longer turns)
    """

    def __init__(self, position: Tuple[int, int], score: int, discount_function: Callable[[int], int] = lambda x: x):
        self.position = position
        self.score = score
        self.discount_function = discount_function

    def get_score(self) -> int:
        """
        :return: Current Score
        """
        return self.score

    def update(self) -> None:
        """
        Updates the current score using the discount function.

        :return:
        """
        self.score = self.discount_function(self.score)


class Board(object):
    """
    Model of gaming board.

    :ivar board_matrix: matrix of the playing field; 0 = valid; 1 = invalid
    :ivar cube_size: size of one board position
    """

    def __init__(self, board_matrix: np.ndarray, cube_size: int):
        self.board_matrix = board_matrix
        self.cube_size = cube_size

    def check_border_collision(self, new_head: Tuple[int, int]) -> bool:
        """
        Check if new coordinate (new_head) is on valid grid point on the board

        :param new_head: new coordinate to check against the valid points

        :return: True if a collision happened, False if new_head is within the field
        """
        if new_head < self.board_matrix.shape:  # Check if coordinates are valid
            if self.board_matrix[new_head] == 1:
                return True
            else:
                return False


def edge_mask(x: np.ndarray):
    mask = np.ones(x.shape, dtype=bool)
    mask[x.ndim * (slice(1, -1),)] = False
    return mask


def main():
    board_dim = (15+2, 20+2)  # +2 for the borders in each direction
    dummy = np.zeros(board_dim, dtype=int)
    dummy[edge_mask(dummy)] = 1

    board = Board(dummy, 25)

    print(board.check_border_collision((2, 4)))
    print(board.check_border_collision((0, 3)))
    print(board.check_border_collision((4, 0)))

if __name__ == "__main__":
    main()