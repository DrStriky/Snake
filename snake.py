from typing import Tuple, List, Optional, Callable


class Snake:
    """
    Models the snake in the game.

    :ivar body: coordinates of the snakes body in reverse order (i.e. body[0] is tail, body[-1] is head)
    :ivar moving_direction: (x, y) coordinates of snakes's moving direction
    """

    def __init__(self, body: List[int, int]):
        """
        Define snake's initial body and initalize moving direction attribute.
        :param body: List of (x, y) coordinates of snake's inital body
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
        """
        Sets position, inital scoare and discount function.

        :param position: (x, y) coordinate of apple's position
        :param score: current score of food
        :param discount_function: function that updates the score after each round (penalty for longer turns)
        """
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