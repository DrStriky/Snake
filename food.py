from typing import Tuple, Callable


class Apple:
    """
    Model of food.

    :ivar position: (x, y) coordinate of apple's position
    :ivar score: current score of food
    :ivar discount_function: function that updates the score after each round (penalty for longer turns)
    """

    def __init__(self, position: Tuple[int, int], score: int = 100, discount_function: Callable[[int], int] = lambda x: x-1):
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
