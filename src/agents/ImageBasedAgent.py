from abc import ABC, abstractmethod
from typing import Optional

from numpy import ndarray

from Action import Action
from BMTask import State
from agents.Agent import Agent
from agents.TrainableAgent import TrainableAgent

from observations.ImageObservation import ImageObservation
from observations.Observations import Observation


class ImageBasedAgent(Agent, TrainableAgent, ABC):
    RAW_WIDTH = 241
    RAW_HEIGHT = 481
    IMAGE_WIDTH = 40
    IMAGE_HEIGHT = 80
    FRAMES = 3

    def __init__(self):
        self.width = ImageBasedAgent.RAW_WIDTH
        self.height = ImageBasedAgent.RAW_HEIGHT
        self.scaled_width = ImageBasedAgent.IMAGE_WIDTH
        self.scaled_height = ImageBasedAgent.IMAGE_HEIGHT
        self.frames = ImageBasedAgent.FRAMES
        self.observation = ImageObservation(self.frames, self.width, self.height, self.scaled_width, self.scaled_height)

    def reset(self):
        self.observation.reset()

    def take_action(self, state: State) -> Action:
        return self.take_action_from_image(self.observation.compute_observation(state))

    def get_observation(self) -> Optional[Observation]:
        return self.observation

    @abstractmethod
    def take_action_from_image(self, image: ndarray) -> Action:
        pass
