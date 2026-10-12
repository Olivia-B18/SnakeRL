import pygame
import random
import numpy as np
import sys
from enum import Enum
from collections import namedtuple
from .events import socketio
from flask_socketio import emit
from flask_login import current_user
from flask import request
import time

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 1000
GAMES = 0

#publisher of training data
def send_data(data):
    socketio.emit("snake_data", {"data": data}, to=request.sid, callback=acknowledgment)

def acknowledgment(running):
    if (not running):
        global GAMES
        GAMES = 1000
        time.sleep(0.3)
        GAMES = 0

class SnakeGameAI:

    def __init__(self, eat_apple, stay_alive, die, w=640, h=480):
        self.w = w
        self.h = h
        self.eat_apple = eat_apple
        self.stay_alive = stay_alive
        self.die = die
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action, games, total_score, record, score):
        global GAMES
        if (GAMES == 1000):
            games = 1000
            GAMES = 0

        self.frame_iteration += 1

        # 1. collect user input
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()

        # OLIVIA'S EDIT:
        # No user input to collect since training runs in a
        # socketio background. Thread and the board is drawn
        # in the browser, not by pygame. Pumping SDL events
        # off the main thread aborts the process on macOS.

        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = self.stay_alive                           # REWARD FUNCTION IF IS ALIVE
        game_over = False
        if self.is_collision() or self.frame_iteration > 60*len(self.snake): # if collision
            game_over = True
            reward = self.die                     # REWARD FUNCTION IF DIES
            return reward, game_over, self.score, games

        # 4. place new food or just move
        if self.head == self.food: # if eats food
            self.score += 1
            reward = self.eat_apple                        # REWARD FUNCTION IF EATS FOOD
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui(games, total_score, record, score)
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score, games

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self, games, total_score, record, score):

        data = {}
        data['snake'] = []
        data['stats'] = {'games': games, 'record': record, 'score': score}

        i = 0
        for pt in self.snake:
            data['snake'].append({'x': pt.x, 'y': pt.y})
            if ((data['snake'][i]['x'] != pt.x) or (data['snake'][i]['y'] != pt.y)):
                print(f"DATA INCONSISTENT")
                print(f"SNAKE: x: {pt.x}, y: {pt.y}")
                print(f"JSON DATA: x: {data['snake'][i]['x']}, y: {data['snake'][i]['x']}")

            i = i + 1

        data['apple'] = {'x': self.food.x, 'y': self.food.y}
        if((data['apple']['x'] != self.food.x) or (data['apple']['y'] != self.food.y)):
            print(f"DATA INCONSISTENT")
            print(f"APPLE: x: {self.food.x}, y: {self.food.y}")
            print(f"JSON DATA: x: {data['apple']['x']}, y: {data['apple']['y']}")
            
        send_data(data)

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
