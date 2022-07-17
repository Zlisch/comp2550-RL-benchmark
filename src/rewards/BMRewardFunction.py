from abc import ABC, abstractmethod

from BMTask import State


class RewardFunction(ABC):
    """
    The abstract class which represents reward function which used to evaluate the performance of the agent.
    """

    @abstractmethod
    def function_name(self) -> str:
        """The name of the reward function"""
        pass

    @abstractmethod
    def compute(self, state: State) -> float:
        """Compute the reward for the current world state. """
        pass
