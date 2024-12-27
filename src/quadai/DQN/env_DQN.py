"""
env_DQN.py
A custom environment for DQN, adding small intermediate rewards for getting closer to the target.
"""

import os
import gym
from gym import spaces
import numpy as np
import pygame
from math import sin, cos, pi, sqrt
from pygame.locals import *

class droneEnv(gym.Env):
    def __init__(self, render_every_frame, mouse_target, width=900, height=900):
        super(droneEnv, self).__init__()
        self.render_every_frame = render_every_frame
        self.mouse_target = mouse_target

        self.width = width
        self.height = height

        pygame.init()
        if render_every_frame:
            self.screen = pygame.display.set_mode((self.width, self.height))
        self.FramePerSec = pygame.time.Clock()

        self.player = pygame.Surface((10,10))
        self.player.fill((255,0,0))

        self.target = pygame.Surface((10,10))
        self.target.fill((0,255,0))

        self.gravity = 0.08
        self.thruster_amplitude = 0.04
        self.diff_amplitude = 0.0006
        self.thruster_mean = 0.04
        self.mass = 1
        self.arm = 25

        self.action_space = spaces.Discrete(5) # 0: nothing, 1:Up,2:Down,3:Right rotate,4:Left rotate
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)

        self.reset()

    def reset(self):
        (self.a, self.ad, self.add)=(0,0,0)
        (self.x, self.xd, self.xdd)=(self.width/2,0,0)
        (self.y, self.yd, self.ydd)=(self.height/2,0,0)
        self.xt = np.random.randint(self.width/4, 3*self.width/4)
        self.yt = np.random.randint(self.height/4, 3*self.height/4)

        self.time = 0
        self.time_limit = 20
        self.prev_dist = sqrt((self.xt - self.x)**2 + (self.yt - self.y)**2)

        if self.render_every_frame:
            self.render("yes")

        return self._get_obs()

    def _get_obs(self):
        angle_to_up = self.a / 180 * pi
        velocity = sqrt(self.xd**2 + self.yd**2)
        angle_velocity = self.ad
        dist_to_target = sqrt((self.xt - self.x)**2+(self.yt - self.y)**2)/500
        angle_to_target = np.arctan2(self.yt - self.y, self.xt - self.x)
        angle_target_and_velocity = angle_to_target - np.arctan2(self.yd, self.xd)
        return np.array([angle_to_up, velocity, angle_velocity, dist_to_target, angle_to_target, angle_target_and_velocity, dist_to_target], dtype=np.float32)

    def step(self, action):
        self.time += 1/60
        done = False
        self.reward = 0.0

        old_dist = sqrt((self.x - self.xt)**2 + (self.y - self.yt)**2)

        thruster_left = self.thruster_mean
        thruster_right = self.thruster_mean

        if action == 1:
            thruster_left += self.thruster_amplitude
            thruster_right += self.thruster_amplitude
        elif action == 2:
            thruster_left -= self.thruster_amplitude
            thruster_right -= self.thruster_amplitude
        elif action == 3:
            thruster_left += self.diff_amplitude
            thruster_right -= self.diff_amplitude
        elif action == 4:
            thruster_left -= self.diff_amplitude
            thruster_right += self.diff_amplitude

        self.xdd = 0
        self.ydd = self.gravity
        self.add = 0

        self.xdd += (-(thruster_left+thruster_right)*sin(self.a*pi/180)/self.mass)
        self.ydd += (-(thruster_left+thruster_right)*cos(self.a*pi/180)/self.mass)
        self.add += self.arm*(thruster_right-thruster_left)/self.mass

        self.xd += self.xdd
        self.yd += self.ydd
        self.ad += self.add
        self.x += self.xd
        self.y += self.yd
        self.a += self.ad

        dist = sqrt((self.x - self.xt)**2+(self.y - self.yt)**2)

        # Basic reward: a small positive reward if we got closer to target
        if dist < old_dist:
            self.reward += 0.1

        # If reached target
        if dist < 50:
            self.reward += 100
            done = True

        # If too far or out of time
        if dist > 1000:
            self.reward -= 1000
            done = True

        if self.time > self.time_limit:
            done = True

        if self.render_every_frame:
            self.render("yes")

        return self._get_obs(), self.reward, done, {}

    def render(self, mode):
        pygame.event.get()
        self.screen.fill((0,0,0))
        self.screen.blit(self.target,(self.xt-5,self.yt-5))
        rotated_player = pygame.transform.rotate(self.player,self.a)
        self.screen.blit(rotated_player,(self.x-5,self.y-5))
        pygame.display.update()
        self.FramePerSec.tick(60)

    def close(self):
        pass
