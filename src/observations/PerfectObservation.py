from abc import abstractmethod
from BMTask import State
from observations.Observations import Observation
import pygame
from rendering.RenderEngine import *
import numpy as np
from tf_agents.specs import array_spec


class PerfectObservation(Observation):

    def __init__(self, state: State):
        self.pos = state.agent.position
        self.black_objs = [(obj.position[0], obj.position[1], STATIC_OBJECT_COLOR) for obj in state.static_objects]
        self.red_objs = [(obj.position[0], obj.position[1], STATIC_OBJECT_COLOR) for obj in state.danger_objects]
        self.blue_objs = [(obj.position[0], obj.position[1], STATIC_OBJECT_COLOR) for obj in state.safe_objects]
        self.numrays = len(self.black_objs) + len(self.red_objs) + len(self.blue_objs)

    def reset(self):
        self.black_objs = []
        self.red_objs = []
        self.blue_objs = []
        self.numrays = 0

    def observation_spec(self):
        """
        Returns an array_spec which interfaces with the py-environment standard
        """
        return array_spec.BoundedArraySpec(
            shape=(self.numrays * 3,), dtype=np.float64, minimum=0.0, maximum=1.0, name='observation')

    def compute_observation(self, state: State):
        """
        Carries out the computation on the state which
        derives the observation
        """
        return self.black_objs + self.red_objs + self.blue_objs

    def render_observation(self, state: State, surf: pygame.Surface):
        """ 
        Renders a representation of the observation to the given surface.
        Aim to illustrate what information the agent has access to
        """
        pass