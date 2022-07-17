from abc import ABC
from abc import abstractmethod

from BMTask import State
from BMTemplate import Template

from tf_agents.specs import array_spec
import numpy as np

from BMTask import State

import pygame


class Observation(ABC):
    """
    Abstraction which facilitates multiple different 
    approaches to the agent observation / perception
    """

    def reset(self):
        pass

    @abstractmethod
    def observation_spec(self):
        """
        Returns an array_spec which interfaces with the py-environment standard
        """
        pass

    @abstractmethod
    def compute_observation(self, state: State):
        """
        Carries out the computation on the state which
        derives the observation
        """
        pass

    @abstractmethod
    def render_observation(self, state: State, surf: pygame.Surface):
        """ 
        Renders a representation of the observation to the given surface.
        Aim to illustrate what information the agent has access to
        """
        pass

