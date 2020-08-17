import pygame
import numpy as np
from interaction_handler import InteractionHandler, BoardEncodingDict, direction
from typing import Dict, Tuple, TypedDict, Optional


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




class PygameInteractions(InteractionHandler):
    """
    Implements GUI and user interactions in PyGame.
    """

    def __init__(self, display: pygame.display, block_length: int, ticks_per_second: int = 30,
                 formatting_file: Optional[str] = None):
        """
        Initializes the board and loads the formatting parameters.
        :param display: display that should be used for user interaction
        :param block_length: length of one block of the board in px
        :param ticks_per_second: duration for each tick of the game.
        :param formatting_file: path to a formatting file specifying the display styles; if not file is given,
            default values are set
        """
        self.clock = pygame.time.Clock()
        self.display = display
        self.ticks_per_second = ticks_per_second
        self.moving_direction = (0, 0)
        self.block_length = block_length

        # validate that block length and window_size are consistent
        display_size = self.display.get_window_size()
        if not display_size[0] % block_length == 0 and display_size[1] % block_length == 0:
            raise ConfigurationError('Display dimensions are not multiples of block length.')

        if formatting_file is not None:
            # ToDo: Load format from formatting file
            raise Exception('Loading of formatting file is not yet implemented!')
        else:
            self.board_formatting: Dict[BlockFormat] = {
                'head': {'code': 500, 'color': (0, 0, 255) , 'file': None},
                'wall': {'code': 1, 'color': (0, 0, 0), 'file': None},
                'valid': {'code': 0, 'color': (255, 255, 255), 'file': None},
                'snake': {'code': 500, 'color': (0, 0, 255) , 'file': None},
                'food': {'code': 500, 'color': (255, 0, 0) , 'file': None}
            }



    def get_encoding_dict(self) -> BoardEncodingDict:
        """Returns the encoding for different board elements."""
        encoding_dict: BoardEncodingDict = {field: formats['code'] for field, formats in self.board_enconding.items()}
        return encoding_dict

    def draw_board(self, geometry_matrix: np.array, current_score: int) -> None:
        """
        Updates the GUI for the next tick.

        """
        for kind, formatting in self.board_formatting:
            x, y = np.where(geometry_matrix == formatting['code'])
            for block in zip(x, y):
                self._draw_block(block, kind)


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
            pygame.draw.rect(surface=self.display,
                             color=self.board_formatting[kind]['color'],
                             rectangle=rectangle)

    def get_interaction(self) -> direction:
        """
        Waits for player's input and returns the moving direction for the next snake
        """

        key_direction_map = {pygame.KEYDOWN: (0, 1),
                             pygame.K_RIGHT: (1, 0),
                             pygame.KEYUP: (0, -1),
                             pygame.K_LEFT: (-1, 0)
                             }

        self.clock.tick(self.ticks_per_second)

        for event in pygame.event.get():
            if event.type in key_direction_map.keys():
                self.moving_direction = key_direction_map[event.type]

        return self.moving_direction
