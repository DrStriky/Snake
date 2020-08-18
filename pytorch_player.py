from player import Player

class PyTorchPlayer(Player):
    def __init__(self):
        self.responses = [(1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (0, -1), (0, -1)]
        self.current_response = -1

    def get_response(self):
        self.current_response = (self.current_response + 1) % 8
        return self.responses[self.current_response]