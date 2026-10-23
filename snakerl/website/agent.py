import torch
import random
import numpy as np
from collections import deque
from flask_login import current_user
from .game import SnakeGameAI, Direction, Point, BLOCK_SIZE
from .model import Linear_QNet, QTrainer
from .dbmodels import AI
from .extensions import db
from flask_socketio import emit
import os

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
MAX_GAMES = 100

QNET_INPUT_SIZE = 11
QNET_HIDDEN_SIZE = 256
QNET_OUTPUT_SIZE = 3

class Agent:
    """
    An Agent that uses a linear neural network and a QTrainer.
    """

    def __init__(self, alpha, gamma, epsilon):
        """
        Create an Agent.
        """
        self.n_games = 0 # counter
        self.max_games = MAX_GAMES
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon_start = epsilon
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(QNET_INPUT_SIZE, QNET_HIDDEN_SIZE, QNET_OUTPUT_SIZE)
        self.trainer = QTrainer(self.model, lr=self.alpha, gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        """
        Add observation to memory deque.

        Popleft if MAX_MEMORY reached. Works like a circular queue.
        """
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """
        Train the QTrainer (long-term memory?).

        Takes a minibatch from the memory deque.
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Train short-term memory with the most recent observation.
        """
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, is_training=True):
        """
        Get an action.

        Action depends on exploration rate and whether Agent is
        in training or evaluation.
        """

        # Get epsilon by taking either 0 or the next decayed epsilon
        self.epsilon = max(0, self.epsilon_start - ((self.n_games / self.max_games) * self.epsilon_start))

        # Initialize final action
        final_move = [0,0,0]

        # With some change, explore with random moves.
        # Else, exploit with best known policy so far.
        if random.random() * 100 < self.epsilon and is_training:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train(alpha, gamma, epsilon, eat, alive, die, should_stop):
    """
    Training process for an Agent.
    """

    # Set up score and record
    total_score = 0
    record = 0

    # Make Agent and a Game
    agent = Agent(alpha, gamma, epsilon)
    game = SnakeGameAI(eat, alive, die, speed=1000)

    # Train for MAX_GAMES episodes
    while agent.n_games < agent.max_games:

        # Stop if "stop training" button is clicked
        if should_stop():
            print("training stopped at game", agent.n_games)
            return None

        # Get state
        state_old = get_state(game)

        # Get action
        final_move = agent.get_action(state_old, is_training=True)

        # Do action and get new state
        reward, done, score, games = game.play_step(final_move, agent.n_games, record)
        state_new = get_state(game)
        agent.n_games = games

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Put newest observation into memory deque
        agent.remember(state_old, final_move, reward, state_new, done)

        # If episode is done, learn from the entire episode, reset game,
        # and update scores and records
        if done:
            agent.train_long_memory()
            game.reset()
            agent.n_games += 1

            if score > record:
                record = score
            total_score += score

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

    # Get averages score from entire training process
    mean_score = total_score / agent.n_games

    # Return
    return agent.n_games, record, mean_score, agent.model

def evaluate(agent, episodes, speed, should_stop):
    """
    Evlaluation process for an agent.
    """

    # Set up score
    scores = []

    # Set game speed
    speed = speed

    # Make Snake game
    game = SnakeGameAI(0, 0, 0, speed=speed) # reward values don't matter since no training

    # Evaluate for however many episodes
    while len(scores) < episodes:

        # Stop if "stop eval" button is clicked
        if should_stop():
            print("evaluation stopped at game", agent.n_games)
            return None

        # Get state
        state = get_state(game)

        # Get move
        move = agent.get_action(state, is_training=False)

        # Perform move and get points
        _, done, score, games = game.play_step(move, len(scores), 0)

        # If episode is done, reset game and add episode's score
        if done:
            game.reset()
            scores.append(score)

            print("END EVALUATION")
            print('Scores', scores)

    # Return scores from each episode
    return scores

def load_agent(file_name):
    """
    Load an agent from the given filename.
    """

    # Create full file path
    file_path = os.path.join("./website/model/", file_name)
    if not os.path.exists(file_path):
        return None

    # Path to "model_20.pth"
    model_20_path = "./website/model/model_20.pth"

    # Load saved weights into a Agent
    model = Linear_QNet(QNET_INPUT_SIZE, QNET_HIDDEN_SIZE, QNET_OUTPUT_SIZE)
    model.load_state_dict(torch.load(model_20_path, map_location="cpu", weights_only=True))
    agent = Agent(0 ,0, 0) # this is for evaluation, so hyperparameters don't matter
    agent.model = model

    # Return the agent
    return agent

def get_state(game):
    """
    Return state of the game.
    """

    # Get head of snake
    head = game.snake[0]

    # Get squares adjacent to head
    point_l = Point(head.x - BLOCK_SIZE, head.y)
    point_r = Point(head.x + BLOCK_SIZE, head.y)
    point_u = Point(head.x, head.y - BLOCK_SIZE)
    point_d = Point(head.x, head.y + BLOCK_SIZE)

    # Get directions as variables
    dir_l = game.direction == Direction.LEFT
    dir_r = game.direction == Direction.RIGHT
    dir_u = game.direction == Direction.UP
    dir_d = game.direction == Direction.DOWN

    # Create list of the game state
    state = [
        # Danger straight
        (dir_r and game.is_collision(point_r)) or 
        (dir_l and game.is_collision(point_l)) or 
        (dir_u and game.is_collision(point_u)) or 
        (dir_d and game.is_collision(point_d)),

        # Danger right
        (dir_u and game.is_collision(point_r)) or 
        (dir_d and game.is_collision(point_l)) or 
        (dir_l and game.is_collision(point_u)) or 
        (dir_r and game.is_collision(point_d)),

        # Danger left
        (dir_d and game.is_collision(point_r)) or 
        (dir_u and game.is_collision(point_l)) or 
        (dir_r and game.is_collision(point_u)) or 
        (dir_l and game.is_collision(point_d)),
        
        # Move direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,
        
        # Food location 
        game.food.x < game.head.x,  # food left
        game.food.x > game.head.x,  # food right
        game.food.y < game.head.y,  # food up
        game.food.y > game.head.y  # food down
        ]

    # Return the state
    return np.array(state, dtype=int)    

def log_to_db(high_score, avg_score, alpha, gamma, epsilon, eat, alive, die, user_id):
    """
    Log the AI agent hyperparamters, reward function, score stats, and id's, to the database.
    """
    ai = AI(high_score=int(high_score), avg_score=int(avg_score), user_id=user_id,
            alpha=float(alpha), gamma=float(gamma), epsilon=int(epsilon),
            eat=int(eat), alive=int(alive), die=int(die),
            )
    db.session.add(ai)
    db.session.commit()
    return ai.id

def start(alpha, gamma, epsilon, eat, alive, die, should_stop):
    """
    Train an Agent and log the result.
    Returns True if training ran to completion.
    """

    # Ensure training results are not empty
    result = train(alpha, gamma, epsilon, eat, alive, die, should_stop)
    if result is None:
        print("training stopped -- result not saved")
        return (False, -1)

    # Save hyperparameters to database and save weights to a file
    num_games, high_score, avg_score, model = result
    if current_user.is_authenticated:
        ai_id = log_to_db(high_score, avg_score, alpha, gamma, epsilon, eat, alive, die, current_user.id)
        model_filename = "model_" + str(ai_id) + ".pth"
        model.save(file_name=model_filename)
    else:
        print("not signed in -- training result not saved")

    return (True, num_games)

if __name__ == '__main__':
    start()