"""
train_SAC.py
Train an SAC agent with improved hyperparameters, more steps, EvalCallback.
Use env_SAC with reward shaping.
"""

import os
from stable_baselines3 import SAC
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback
import pandas as pd

from env_SAC import droneEnv

log_dir = "tmp_sac/"
os.makedirs(log_dir, exist_ok=True)

env = droneEnv(render_every_frame=False, mouse_target=False, width=900, height=900)
env = Monitor(env, log_dir)

eval_env = droneEnv(render_every_frame=False, mouse_target=False, width=900, height=900)

model = SAC(
    "MlpPolicy", env, verbose=1, tensorboard_log=log_dir,
    learning_rate=1e-4,  # lower learning rate
    batch_size=256,
    buffer_size=500000,
    tau=0.02,
    gamma=0.99,
    policy_kwargs={"net_arch":[256,256]}
)

eval_callback = EvalCallback(eval_env, best_model_save_path='./sac_logs/',
                             log_path='./sac_logs/', eval_freq=50000,
                             deterministic=True, render=False)

model.learn(total_timesteps=6000000, callback=eval_callback)

model.save("sac_improved_model.zip")
