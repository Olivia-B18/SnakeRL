import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple
from .events import socketio
from flask_socketio import emit
from flask import request

# Initialize PyGame
pygame.init()

# Constants
BLOCK_SIZE = 20
INIT_LENGTH = 3

# Create Point data type
Point = namedtuple('Point', 'x, y')

# Create Direction class
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# Map direction snake is facing with how coordinates of head change
STEPS = {
    "RIGHT": (BLOCK_SIZE, 0),
    "LEFT": (-BLOCK_SIZE, 0),
    "UP": (0, -BLOCK_SIZE),
    "DOWN": (0, BLOCK_SIZE),
}

def send_data(data):
    """
    Publisher of training data
    """
    socketio.emit("snake_data", {"data": data}, to=request.sid)

class SnakeGameAI:

    def __init__(self, eat, alive, die, speed=1000, width=640, height=480):
        """
        A game of snake.
        """
        self.w=width
        self.h=height
        self.eat = eat
        self.alive = alive
        self.die = die
        self.speed = speed
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        """
        Reset the game for the next episode of snake.
        """
        self._place_snake()
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        """
        Randomly place apple within bounds of the game board.
        """

        # Make apple from randomly selected x- and y-coordinates.
        x_food = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y_food = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x_food, y_food)

        # Do not place food on the snake
        while self.food in self.snake:
            self._place_food()

    def _place_snake(self):
        """
        Randomly place the snake within bounds of the game board.
        """

        # Randomly select x and y for head.
        # Multiply by an offset so snake always fits on board.
        x_min = (0 + (INIT_LENGTH - 1) * BLOCK_SIZE) // BLOCK_SIZE
        x_max = (self.w - INIT_LENGTH * BLOCK_SIZE) // BLOCK_SIZE
        x_head = random.randint(x_min, x_max) * BLOCK_SIZE
        y_min = (0 + (INIT_LENGTH - 1) * BLOCK_SIZE) // BLOCK_SIZE
        y_max = (self.h - INIT_LENGTH * BLOCK_SIZE) // BLOCK_SIZE
        y_head = random.randint(y_min, y_max) * BLOCK_SIZE
        self.head = Point(x_head, y_head)

        # Randomly pick direction
        self.direction = np.random.choice(list(Direction))

        # Get dx and dy according to direction
        dx, dy = STEPS[self.direction.name]

        # Fill body of snake with just head
        self.snake = [self.head]

        # Append body of snake
        for i in range(1, INIT_LENGTH):
            x_body = self.head.x - i * dx
            y_body = self.head.y - i * dy
            self.snake.append(Point(x_body, y_body))

    def play_step(self, action, games, record):
        """
        Apply an action from the snake to the game.
        """

        self.frame_iteration += 1

        # Move the snake
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # Check if game is over
        reward = self.alive # reward function: alive
        game_over = False
        if self.is_collision() or self.frame_iteration > 60*len(self.snake):
            game_over = True
            reward = self.die # reward function: die
            return reward, game_over, self.score, games

        # Place new food or just move
        if self.head == self.food: 
            self.score += 1
            reward = self.eat # reward function: food
            self._place_food()
        else:
            self.snake.pop()
        
        # Update UI and clock
        self._update_ui(games, record)
        self.clock.tick(self.speed)

        # Return reward, game over and score
        return reward, game_over, self.score, games

    def is_collision(self, pt=None):
        """
        Detect if the snake has collided with itself or a wall.
        """

        # Ensure point is not empty
        if pt is None:
            pt = self.head
        # Hits wall
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self, games, record):
        """
        Update the snake UI.
        """

        data = {}
        data['snake'] = []
        # Send this step's score (self.score), not the previous step's. The
        # record only updates when a game ends, so show the current score
        # if it has already beaten it.
        data['stats'] = {'games': games,
                         'record': max(record, self.score),
                         'score': self.score}

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
        """
        Move the snake according to which direction it went.
        """
        
        # Find new direction where array encoding is [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # straight
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        # Assign new direction
        self.direction = new_dir

        # Update head
        dx, dy = STEPS[self.direction.name]
        x = self.head.x
        y = self.head.y
        self.head = Point(self.head.x + dx, self.head.y + dy)
