import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from network import Linear_QNet2

from player import Player
from interaction_handler import BoardEncodingDict
import random
import numpy as np
from typing import Tuple, List
from collections import deque


class PyTorchPlayer(Player):
    def __init__(self):
        self.counter_games = 0
        self.counter_move = 0

        self.gamma = 0.9
        self.epsilon = 0
        self.memory = deque()
        self.lr = 1e-4
        self.model = Linear_QNet2(11, 256, 3)
        self.model.train()
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss_fn = nn.MSELoss()

    def push_board_status(self, occupation_matrix: np.array, moving_direction: Tuple[int, int],
                          score: int, food_score: int) -> None:
        """Player receives new board status"""
        self.new_status = {'matrix': occupation_matrix,
                       'moving_direction': moving_direction,
                       'score': score,
                       'food_score': food_score,
                       'predictor_vector': None,
                       'move': None}

    def get_response(self) -> Tuple[int, int]:
        self.get_state_vector()
        dummy = self.predict_action()

        if dummy[0] == 1:  # left
            self.new_status['move'] = (-self.new_status['moving_direction'][1], self.new_status['moving_direction'][0])
        elif dummy[1] == 1:  #straight
            self.new_status['move'] = (self.new_status['moving_direction'][0], self.new_status['moving_direction'][1])
        else:  # right
            self.new_status['move'] = (self.new_status['moving_direction'][1], self.new_status['moving_direction'][0])

        if self.counter_move == 0:
            self.previous_status = self.new_status
            self.previous_status['move'] = (0,1)

        # self.train_short_memory(state_old, final_move, reward, state_new, done)
        self.train_short_memory(self.previous_status['predictor_vector'], self.previous_status['move'], -self.previous_status['food_score'], self.new_status['predictor_vector'], False)
        # self.remember(state_old, final_move, reward, state_new, done)
        self.remember(self.previous_status['predictor_vector'], self.previous_status['move'], -self.previous_status['food_score'], self.new_status['predictor_vector'], False)

        self.previous_status = self.new_status
        self.counter_move += 1

        return self.new_status['move']

    def get_state_vector(self) -> None:
        predictor_vector = []
        head = np.where(self.new_status['matrix'] == self.encoding['head'])
        food = np.where(self.new_status['matrix'] == self.encoding['food'])

        # Check if left, straight and right are free
        predictor_vector.append(True if self.new_status['matrix'][tuple(p + q for p, q in zip(head, (-self.new_status['moving_direction'][1], self.new_status['moving_direction'][0])))] == self.encoding['valid'] else False)
        predictor_vector.append(True if self.new_status['matrix'][tuple(p + q for p, q in zip(head, (self.new_status['moving_direction'][0], self.new_status['moving_direction'][1])))] == self.encoding['valid'] else False)
        predictor_vector.append(True if self.new_status['matrix'][tuple(p + q for p, q in zip(head, (self.new_status['moving_direction'][1], self.new_status['moving_direction'][0])))] == self.encoding['valid'] else False)

        # Which direction are we running?
        predictor_vector.append(True if self.new_status['moving_direction'] == (0,1) else False)
        predictor_vector.append(True if self.new_status['moving_direction'] == (0,-1) else False)
        predictor_vector.append(True if self.new_status['moving_direction'] == (1,0) else False)
        predictor_vector.append(True if self.new_status['moving_direction'] == (-1,0) else False)

        # In which direction is the next food (
        predictor_vector.append(True if food[0] < head[0] else False)
        predictor_vector.append(True if food[0] > head[0] else False)
        predictor_vector.append(True if food[1] < head[1] else False)
        predictor_vector.append(True if food[1] > head[1] else False)

        self.new_status['predictor_vector'] = predictor_vector

    def predict_action(self) -> List:
        self.epsilon = 80 - self.counter_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
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
        target = reward
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