from abc import ABC, abstractmethod
from typing import Optional

from tf_agents.agents import TFAgent
from tf_agents.trajectories import time_step as ts

from Action import Action
from BMTask import State
from observations.Observations import Observation


class Agent(ABC):
    """
    The abstract agent class which provide action according to given world.
    """

    def reset(self):
        """Reset all information in the agent. """
        pass

    @abstractmethod
    def agent_name(self) -> str:
        """The name of the agent"""
        pass

    @abstractmethod
    def take_action(self, state: State) -> Optional[Action]:
        """
        The implementation of the agent which generate action.
        The return action can be None; in this case, the simulation will not progress to the next step.
        Note: if want the agent to stay at current position, use Action.STAY instead!
        An trained agent in the testing environment should NOT return None action.
        """
        pass

    @abstractmethod
    def update_reward(self, reward: float):
        """Update the reward which agent received from the last action """
        pass
