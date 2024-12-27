"""
train_DQN.py
Train a DQN agent with improved parameters, more steps, and evaluation callback.
Ensure env_DQN is updated with reward shaping.
"""

import os
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor
import gym
import sys

# Assume env_DQN.py is in the same directory
from env_DQN import droneEnv

# Create log dir
log_dir = "tmp_dqn/"
os.makedirs(log_dir, exist_ok=True)

# Create and wrap the environment
env = droneEnv(False, False, width=900, height=900)
env = Monitor(env, log_dir)

eval_env = droneEnv(False, False, width=900, height=900)

model = DQN(
    "MlpPolicy", env, verbose=1, tensorboard_log=log_dir,
    learning_rate=5e-5,  # improved hyperparam
    batch_size=128,
    buffer_size=1000000,
    exploration_fraction=0.2,
    gamma=0.99,
    policy_kwargs={"net_arch": [256,256]}
)

eval_callback = EvalCallback(eval_env, best_model_save_path='./dqn_logs/',
                             log_path='./dqn_logs/', eval_freq=50000,
                             deterministic=True, render=False)

model.learn(total_timesteps=1000000, callback=eval_callback)

model.save("dqn_improved_model.zip")