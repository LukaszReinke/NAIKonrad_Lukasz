# -*- coding: utf-8 -*-
"""bowling.ipynb

Authors: Łukasz Reinke <s15037@pjwstk.edu.pl>, Konrad Chrzanowski <s17404@pjwstk.edu.pl>

Problem: Train AI to play sbowling game

Followed by: github user @deepanshut041

# install os dependencies to display env
"""

# Commented out IPython magic to ensure Python compatibility.
# !apt-get install python-opengl -y

# !apt install xvfb -y

# !pip install pyvirtualdisplay

# !pip install piglet

# %pip install -U gym>=0.21.0
# %pip install -U gym[atari,accept-rom-license]

"""# Import python dependencies"""

# Commented out IPython magic to ensure Python compatibility.
# import minerl

# %matplotlib inline

"""# start virtual display"""

from stack_frame import preprocess_frame, stack_frame
from models import ActorCnn, CriticCnn
from agent import A2CAgent
import sys
import time
import gym
import random
import torch
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from IPython.display import clear_output
import math
from pyvirtualdisplay import Display
Display().start()

"""#import ai classes"""


"""# create environment"""

# loading ROM Collection for spaceinvader

env = gym.make('Bowling-v0')
env.seed(0)

"""# set accelerator """

# if gpu is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device: ", device)

# from google.colab import drive
# drive.mount('/content/drive')

"""# view Enviroment"""

print("The size of frame is: ", env.observation_space.shape)
print("No. of Actions: ", env.action_space.n)
env.reset()
plt.figure()
plt.imshow(env.reset())
plt.title('Original Frame')
plt.show()

"""### execute the code cell below to play with a random policy."""


def random_play():
    score = 0
    env.reset()
    while True:
        env.render()
        action = env.action_space.sample()
        state, reward, done, _ = env.step(action)
        score += reward
        if done:
            env.close()
            print("Your Score at end of game is: ", score)
            break


random_play()

"""

```
# Sformatowano jako kod
```

# preprocessing frame"""

env.reset()
plt.figure()
plt.imshow(preprocess_frame(env.reset(), (8, -12, -12, 4), 84), cmap="gray")
plt.title('Pre Processed image')
plt.show()

"""# stacking frame"""


def stack_frames(frames, state, is_new=False):
    frame = preprocess_frame(state, (8, -12, -12, 4), 84)
    frames = stack_frame(frames, frame, is_new)

    return frames


"""# creating agent"""

INPUT_SHAPE = (4, 84, 84)
ACTION_SIZE = env.action_space.n
SEED = 0
GAMMA = 0.99           # discount factor
ALPHA = 0.0001          # Actor learning rate
BETA = 0.0005          # Critic learning rate
UPDATE_EVERY = 100     # how often to update the network

agent = A2CAgent(INPUT_SHAPE, ACTION_SIZE, SEED, device, GAMMA,
                 ALPHA, BETA, UPDATE_EVERY, ActorCnn, CriticCnn)

"""# run untrained agent play"""

state = stack_frames(None, env.reset(), True)
for j in range(200):
    env.render()
    action, _, _ = agent.act(state)
    next_state, reward, done, _ = env.step(action)
    state = stack_frames(state, next_state, False)
    if done:
        break

env.close()

"""# loading agent
Uncomment line to load a pretrained agent
"""

start_epoch = 0
scores = []
scores_window = deque(maxlen=20)

"""# train the agent with DQN"""


def train(n_episodes=1000):
    """
    Params
    ======
        n_episodes (int): maximum number of training episodes
    """
    for i_episode in range(start_epoch + 1, n_episodes+1):
        state = stack_frames(None, env.reset(), True)
        score = 0
        while True:
            action, log_prob, entropy = agent.act(state)
            next_state, reward, done, info = env.step(action)
            score += reward
            next_state = stack_frames(state, next_state, False)
            agent.step(state, log_prob, entropy, reward, done, next_state)
            state = next_state
            if done:
                break
        scores_window.append(score)       # save most recent score
        scores.append(score)              # save most recent score

        clear_output(True)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(np.arange(len(scores)), scores)
        plt.ylabel('Score')
        plt.xlabel('Episode #')
        plt.show()
        print('\rEpisode {}\tAverage Score: {:.2f}'.format(
            i_episode, np.mean(scores_window)), end="")

    return scores


scores = train(100)

"""# run learnt agent"""

score = 0
state = stack_frames(None, env.reset(), True)
while True:
    env.render()
    action, _, _ = agent.act(state)
    next_state, reward, done, _ = env.step(action)
    score += reward
    state = stack_frames(state, next_state, False)
    if done:
        print("You Final score is:", score)
        break
env.close()
