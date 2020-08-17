import pytest
from snake import Snake
from typing import List, Tuple

@pytest.mark.parametrize(
    'body,moving_direction,got_food,expected_body,expected_success',
    [([(10, 10)], (0, 0), False, [(10, 10)], True),  # missing propagation with default init values
     ([(10, 10)], (0, 1), False, [(10, 11)], True),  # propagation of initial value
     ([(10, 10), (10, 9), (10, 8), (9, 8), (8, 8)],  # propagation of long snake without food
      (0, 1), False, [(10, 9), (10, 8), (9, 8), (8, 8), (8, 9)], True),
     ([(10, 10), (10, 9), (10, 8), (9, 8), (8, 8)], (0, 1), True,  # propagation of long snake with foot
      [(10, 10), (10, 9), (10, 8), (9, 8), (8, 8), (8, 9)], True),
     ([(1, 1), (1, 2), (1, 3), (2, 3), (2, 2)], (-1, 0), False,  # propagation of long snake with crash
      [(1, 2), (1, 3), (2, 3), (2, 2), (1, 2)], False)
     ])
def test_snake_update(body: List[Tuple[int, int]], moving_direction: Tuple[int, int], got_food: bool,
                      expected_body: List[Tuple[int, int]], expected_success
                      ):
    """
    Tests propagation of the snake.

    :return:
    """
    my_snake = Snake(body=body)
    my_snake.change_moving_direction(new_direction=moving_direction)
    success = my_snake.update(got_food=got_food)

    assert my_snake.body == expected_body and success == expected_success


def test_snake_get_propagated_head():
    """
    Tests propagation of head.

    :return:
    """
    body = [(0, 0), (1, 0), (2, 0)]
    moving_direction = (0, 1)
    expected_propagated_head = (body[-1][0] + moving_direction[0], body[-1][1] + moving_direction[1])

    my_snake = Snake(body=body)
    my_snake.change_moving_direction(moving_direction)
    new_head = my_snake.get_propagated_head()

    assert expected_propagated_head == new_head
