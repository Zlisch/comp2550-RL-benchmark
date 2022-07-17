# Tensorflow Stuff
from typing import Tuple, Text, Optional

import pygame
import tensorflow as tf
from tf_agents.typing import types
from tf_agents.environments import PyEnvironment
from tf_agents.trajectories import time_step as ts
import numpy as np

# BM stuff:
from BMTemplate import Template
from BMTask import State
from Action import Action, action_spec
from rendering import RenderEngine
from rewards.BMRewardFunction import RewardFunction
from observations.Observations import Observation


# discount_factor = 0.95


class Sandbox(PyEnvironment):

    def __init__(self,
                 max_iter: int,
                 template: Template,
                 variant_range: Tuple[float, float],
                 reward_function: RewardFunction,
                 observation: Observation,
                 discount_factor: float):
        super().__init__()
        self.max_iter = max_iter
        self.iter_counter = 0
        self.discount_factor = discount_factor
        # Represents the 9 movement directions of the agent:
        self._action_spec = action_spec()
        self.observation = observation
        # Initialise the state using the world of the template with a variant within the range:
        self.template = template
        self.variant_range = variant_range
        # Set the reward function for the environment:
        self.reward = reward_function
        # declare state
        self.state = None
        self._episode_ended = False

    def observation_spec(self) -> types.NestedArraySpec:
        return self.observation.observation_spec()

    def action_spec(self) -> types.NestedArraySpec:
        return self._action_spec

    def get_info(self) -> types.NestedArray:
        raise NotImplementedError()

    def get_state(self) -> State:
        raise NotImplementedError()

    def set_state(self, state: State) -> None:
        raise NotImplementedError()

    def _step(self, action: types.NestedArray) -> ts.TimeStep:
        if self._episode_ended:
            # The last action ended the episode. Ignore the current action and start
            # a new episode.
            return self.reset()
        # Apply the action of the agent to the state:
        # The physics step is also done here
        action_item = Action(action)
        # print(action_item)
        # print('apply', str(action_item))
        self.state.apply_action(action_item)  # the action needs to be converted
        self.iter_counter += 1
        reward_value = self.reward.compute(self.state)
        obs = self.observation.compute_observation(self.state)
        if self.state.check_termination():
            self._episode_ended = True
            return ts.termination(observation=obs, reward=reward_value)
        elif self.iter_counter >= self.max_iter:
            self._episode_ended = True
            return ts.termination(observation=obs, reward=reward_value)
        return ts.transition(reward=reward_value, observation=obs, discount=self.discount_factor)

    def _reset(self) -> ts.TimeStep:
        lower, upper = self.variant_range
        variant = (np.random.random() * (upper - lower)) + lower
        self.state = self.template.create_world(variant)
        self.iter_counter = 0
        self._episode_ended = False
        self.observation.reset()
        obs = self.observation.compute_observation(self.state)
        return ts.restart(observation=obs)

    def render(self, mode: Text = 'rgb_array') -> Optional[types.NestedArray]:
        """ Facilitates viewership of the training process """
        # Check that the window has not been closed:
        canvas = pygame.Surface((800, 608))
        RenderEngine.render_state(canvas, self.state)
        return np.transpose(np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2))
