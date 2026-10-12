import pygame
import random
import numpy as np
import sys
from enum import Enum
from collections import namedtuple
from .events import socketio
from flask_socketio import emit
from flask import request
import time

pygame.init()

BLOCK_SIZE = 20
SPEED = 1000
GAMES = 0
INIT_LENGTH = 3

Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# map direction snake is facing with how coordinates of head change
STEPS = {
    "RIGHT": (BLOCK_SIZE, 0),
    "LEFT": (-BLOCK_SIZE, 0),
    "UP": (0, -BLOCK_SIZE),
    "DOWN": (0, BLOCK_SIZE),
}

# publisher of training data
def send_data(data):
    socketio.emit("snake_data", {"data": data}, to=request.sid, callback=acknowledgment)

def acknowledgment(running):
    if (not running):
        global GAMES
        GAMES = 1000
        time.sleep(0.3)
        GAMES = 0

class SnakeGameAI:

    def __init__(self, eat, alive, die, width=640, height=480):
        self.w=width
        self.h=height
        self.eat = eat
        self.alive = alive
        self.die = die
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self._place_snake()
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x_food = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y_food = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x_food, y_food)
        while self.food in self.snake:
            self._place_food()

    def _place_snake(self):
        # randomly select x and y for head
        # multiply by an offset so snake always fits on board
        x_min = (0 + (INIT_LENGTH - 1) * BLOCK_SIZE) // BLOCK_SIZE
        x_max = (self.w - INIT_LENGTH * BLOCK_SIZE) // BLOCK_SIZE
        x_head = random.randint(x_min, x_max) * BLOCK_SIZE
        y_min = (0 + (INIT_LENGTH - 1) * BLOCK_SIZE) // BLOCK_SIZE
        y_max = (self.h - INIT_LENGTH * BLOCK_SIZE) // BLOCK_SIZE
        y_head = random.randint(y_min, y_max) * BLOCK_SIZE
        self.head = Point(x_head, y_head)

        # randomly pick direction
        self.direction = np.random.choice(list(Direction))

        # get dx and dy according to direction
        dx, dy = STEPS[self.direction.name]

        # fill body of snake with just head
        self.snake = [self.head]

        # append body of snake
        for i in range(1, INIT_LENGTH):
            x_body = self.head.x - i * dx
            y_body = self.head.y - i * dy
            self.snake.append(Point(x_body, y_body))

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

        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = self.alive                            # REWARD FUNCTION IF IS ALIVE
        game_over = False
        if self.is_collision() or self.frame_iteration > 60*len(self.snake):
            game_over = True
            reward = self.die                               # REWARD FUNCTION IF DIES
            return reward, game_over, self.score, games

        # 4. place new food or just move
        if self.head == self.food: # if eats food
            self.score += 1
            reward = self.eat                         # REWARD FUNCTION IF EATS FOOD
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
        
        # find new direction where array encoding is [straight, right, left]
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

        # assign new direction
        self.direction = new_dir

        # update head
        dx, dy = STEPS[self.direction.name]
        x = self.head.x
        y = self.head.y
        self.head = Point(self.head.x + dx, self.head.y + dy)
