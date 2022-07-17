import os
from abc import ABC, abstractmethod
from typing import Optional

from tf_agents.agents import TFAgent
from tf_agents.trajectories import time_step as ts
from tf_agents.utils import common

from observations.Observations import Observation


class TrainableAgent(ABC):

    @abstractmethod
    def get_observation(self) -> Optional[Observation]:
        pass

    @abstractmethod
    def get_model(self) -> TFAgent:
        pass

    @abstractmethod
    def train(self,
              learning_rate: float,
              time_step_spec: ts.TimeStep):
        pass

    def save_policy(self, path: str, name: str):
        pass

    def load_policy(self, path: str):
        pass
