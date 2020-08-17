from snake import Apple

def test_apple_default_update():
    """
    validates that apple is updated correctly with default discount function
    :return:
    """
    pos = 10
    score = 10
    my_apple = Apple(position=pos, score=score)
    my_apple.update()
    assert my_apple.get_score() == score


def test_apple_discounted_update():
    """
    validates that apple is updated correctly with default discount function
    :return:
    """
    pos = 10
    score = 10
    discount_function = lambda x: x - 1
    my_apple = Apple(position=pos, score=score, discount_function=discount_function)
    my_apple.update()
    assert my_apple.get_score() == discount_function(score)