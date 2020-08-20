import random
from collections import deque
from typing import Tuple, List

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from network import Linear_QNet2
from player import Player


class PyTorchPlayer(Player):
    def __init__(self):
        self.counter_games = 0
        self.counter_move = 0

        self.gamma = 0.9
        self.epsilon = 0
        self.memory = deque()
        self.lr = 1e-4
        self.model = Linear_QNet2(12, 256, 4)
        self.model.train()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

        self.previous_status = None
        self.new_status = None
        self.encoding = None

    def push_board_status(self, occupation_matrix: np.array, moving_direction: Tuple[int, int],
                          score: int, food_score: int) -> None:
        """Player receives new board status"""
        self.new_status = {'matrix': occupation_matrix,
                           'moving_direction': moving_direction,
                           'score': score,
                           'food_score': food_score,
                           'predictor_vector': None,
                           'prediction': None,
                           'move': None}

        self.get_state_vector()

    def get_response(self) -> Tuple[int, int]:
        self.new_status['prediction'] = self.predict_action()

        if self.new_status['prediction'][0] == 1:  # up
            self.new_status['move'] = (-1, 0)
        elif self.new_status['prediction'][1] == 1:  # left
            self.new_status['move'] = (0, -1)
        elif self.new_status['prediction'][2] == 1:  # down
            self.new_status['move'] = (1, 0)
        elif self.new_status['prediction'][3] == 1:  # right
            self.new_status['move'] = (0, 1)

        if self.counter_move == 0:
            self.previous_status = self.new_status
            self.previous_status['move'] = (0, 1)

        reward = self.new_status['score']-self.previous_status['score']-1
        # self.train_short_memory(state_old, final_move, reward, state_new, done)
        self.train_short_memory(self.previous_status['predictor_vector'], self.previous_status['prediction'], reward, self.new_status['predictor_vector'], False)
        # self.remember(state_old, final_move, reward, state_new, done)
        self.remember(self.previous_status['predictor_vector'], self.previous_status['prediction'], reward, self.new_status['predictor_vector'], False)

        self.previous_status = self.new_status
        self.counter_move += 1

        return self.new_status['move']

    def closing_action(self):
        # One game is over, train on the memory
        self.get_state_vector()

        reward = -10

        self.train_short_memory(self.previous_status['predictor_vector'], self.previous_status['prediction'], reward, self.new_status['predictor_vector'], True)
        self.remember(self.previous_status['predictor_vector'], self.previous_status['prediction'], reward, self.new_status['predictor_vector'], True)
        self.train_long_memory(self.memory)

    def get_state_vector(self) -> None:
        predictor_vector = []
        head = np.asarray(np.where(self.new_status['matrix'] == self.encoding['head'])).flatten()
        food = np.asarray(np.where(self.new_status['matrix'] == self.encoding['food'])).flatten()

        # Check if left, straight and right are free
        predictor_vector.append(False if self.new_status['matrix'][head[0]-1, head[1]+0] == self.encoding['valid'] else True)
        predictor_vector.append(False if self.new_status['matrix'][head[0]+0, head[1]-1] == self.encoding['valid'] else True)
        predictor_vector.append(False if self.new_status['matrix'][head[0]+1, head[1]+0] == self.encoding['valid'] else True)
        predictor_vector.append(False if self.new_status['matrix'][head[0]+0, head[1]+1] == self.encoding['valid'] else True)

        # Which direction are we running?
        predictor_vector.append(True if self.new_status['moving_direction'] == (-1, 0) else False)  # up
        predictor_vector.append(True if self.new_status['moving_direction'] == (0, -1) else False)  # left
        predictor_vector.append(True if self.new_status['moving_direction'] == (1, 0) else False)  # down
        predictor_vector.append(True if self.new_status['moving_direction'] == (0, 1) else False)  # right

        # In which direction is the next food
        predictor_vector.append(True if food[0] < head[0] else False)  # above
        predictor_vector.append(True if food[1] < head[1] else False)  # left
        predictor_vector.append(True if food[0] > head[0] else False)  # down
        predictor_vector.append(True if food[1] > head[1] else False)  # right

        self.new_status['predictor_vector'] = np.asarray(list(map(int, predictor_vector)))

    def predict_action(self) -> List[int]:
        self.epsilon = 80 - self.counter_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] += 1
        else:
            state0 = torch.tensor(self.new_status['predictor_vector'], dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] += 1
        return final_move

    def train_long_memory(self, memory):
        self.counter_games += 1
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory

        state, action, reward, next_state, done = zip(*minibatch)
        state = torch.tensor(state, dtype=torch.float)  # [1, ... , 0]
        action = torch.tensor(action, dtype=torch.long)  # [1, 0, 0]
        reward = torch.tensor(reward, dtype=torch.float)  # int
        next_state = torch.tensor(next_state, dtype=torch.float)  # [True, ... , False]
        target = reward + self.gamma * torch.max(self.model(next_state), dim=1)[0]
        location = [[x] for x in torch.argmax(action, dim=1).numpy()]
        location = torch.tensor(location)
        pred = self.model(state).gather(1, location)  # [action]
        pred = pred.squeeze(1)
        loss = self.loss_fn(target, pred)
        loss.backward()
        self.optimizer.step()

    def train_short_memory(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        target = reward

        if not done:
            target = reward + self.gamma * torch.max(self.model(next_state))
        pred = self.model(state)
        target_f = pred.clone()
        target_f[torch.argmax(action).item()] = target
        loss = self.loss_fn(target_f, pred)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append([state, action, reward, next_state, done])
        if len(self.memory) > 100000:
            self.memory.popleft()
