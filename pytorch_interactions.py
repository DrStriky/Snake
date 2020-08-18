import pygame
import numpy as np
from interaction_handler import InteractionHandler, BoardEncodingDict, direction
from typing import Dict, Tuple, TypedDict, Optional
from player import Player

class ConfigurationError(Exception):
    """
    Raised if configuration is inconsistent.
    """
    pass


class BlockFormat(TypedDict):
    """
    Formatting instructions for the different fields on the board (e.g. snake, wall, head, food)

    :var code: integer code representing the element type in the geometry matrix
    :var color: (R, G, B)-tuple for color of element
    :var picture: path to picture, if the element should be filled with a picture (e.g. apple or head)
    """
    code: int
    color: Tuple[int, int, int]
    picture: str


class PyGamePyTorchInteractionHandler(InteractionHandler):
    """
    Implements Interaction with AI
    """

    def __init__(self, player: Player, display: Optional[pygame.Surface] = None,
                 block_length: Optional[int] = None, ticks_per_second: Optional[int] = None,
                 formatting_file: Optional[str] = None):
        """
        Initializes the board and loads the formatting parameters.

        :param player: AI that plays the game
        :param display: display that should be used for user interaction
        :param block_length: length of one block of the board in px
        :param ticks_per_second: duration for each tick of the game; if set to None, then the game is not
            displayed and answers are immediately passed to the game
        :param formatting_file: path to a formatting file specifying the display styles; if not file is given,
            default values are set
        """
        self.player = player
        self.ticks_per_second = None
        self.block_length = block_length
        self.font = pygame.font.SysFont("comicsansms", 15, bold=True)
        self.display = None
        self.clock = None
        self.block_length = None
        self.show_game = False

        self.set_display(display, block_length)
        self.set_ticks_per_second(ticks_per_second)

        if formatting_file is not None:
            # ToDo: Load format from formatting file
            raise Exception('Loading of formatting file is not yet implemented!')
        else:
            self.board_formatting: Dict[str, BlockFormat] = {
                'head': {'code': 101, 'color': (0, 0, 255), 'picture': None},
                'wall': {'code': 1, 'color': (0, 0, 0), 'picture': None},
                'valid': {'code': 0, 'color': (255, 255, 255), 'picture': None},
                'snake': {'code': 100, 'color': (0, 0, 255), 'picture': None},
                'food': {'code': 200, 'color': (255, 0, 0), 'picture': None}
            }

    def set_display(self, display: Optional[pygame.Surface] = None, block_length: Optional[int] = None):
        """
        Set the display and assert that block_length and display are compatible.

        :param display:
        :param block_length:
        :return:
        """
        # both must be set or not set
        if not ((display is None and block_length is None)
                or (display is not None and block_length is not None)):
            raise ConfigurationError('Display and block_length must both be either defined or not defined.')

        self.display = display
        self.block_length = block_length

        # validate that block length and window_size are consistent
        display_size = self.display.get_size()
        if not display_size[0] % block_length == 0 and display_size[1] % block_length == 0:
            raise ConfigurationError('Display dimensions are not multiples of block length.')

    def set_ticks_per_second(self, ticks_per_second: Optional[int] = None) -> None:
        """
        Update ticks per second. If it is set to a value other than None, assert that all elements
        to display the game are available

        :param ticks_per_second:
        """
        if ticks_per_second is not None:
            if self.display is None:
                raise ConfigurationError('No display available to show the game.')
            else:
                self.ticks_per_second = ticks_per_second
                self.clock = pygame.time.Clock()
                self.show_game = True
        else:
            self.ticks_per_second = None
            self.clock = None
            self.show_game = False

    def get_encoding_dict(self) -> BoardEncodingDict:
        """Returns the encoding for different board elements."""
        encoding_dict: BoardEncodingDict = {field: formats['code'] for field, formats in self.board_formatting.items()}
        return encoding_dict

    def push_board_status(self, geometry_matrix: np.array, moving_direction: Tuple[int, int], current_score: int,
                          food_score: int) -> None:
        """
        Gets response from AI player and updates the GUI for the next tick, if the game is shown..
        """
        self.player.push_board_status(geometry_matrix, moving_direction, current_score, food_score)

        if self.show_game:
            for kind, formatting in self.board_formatting.items():
                x, y = np.where(geometry_matrix == formatting['code'])

                block: Tuple[int, int]
                for block in zip(x, y):
                    self._draw_block(block, kind)

            self.display.blit(self.font.render(f'{current_score}', True, (0, 255, 255)),  (25, 0))
            pygame.display.update()
            self.clock.tick(self.ticks_per_second)

            for event in pygame.event.get():
                # ToDo: remove this crap that is caused by fucking OS X/PyGame Interaction Error
                pass

    def _draw_block(self, block: Tuple[int, int], kind: str) -> None:
        """
        Draws a specific block on display.

        :param block: (x, y) - (block) coordinates of the block to draw
        :param kind: kind of block to draw; must be key of self.board_formatting
        """
        # ToDo: implement display picture: https://pythonprogramming.net/displaying-images-pygame/
        if self.board_formatting[kind]['picture'] is not None:
            raise Exception('Displaying pictures has not yet been implemented!')
        else:
            rectangle = [block[0] * self.block_length, block[1] * self.block_length,
                         self.block_length, self.block_length]
            pygame.draw.rect(self.display, self.board_formatting[kind]['color'], rectangle)

    def get_interaction(self) -> direction:
        """
        Waits for player's input and returns the moving direction for the next snake
        """
        return self.player.get_response()


