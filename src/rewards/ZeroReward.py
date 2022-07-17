from BMTask import State
from rewards.BMRewardFunction import RewardFunction


class ZeroRewardFunction(RewardFunction):
    """A basic implementation which always return 0 reward for all states. """

    def function_name(self) -> str:
        return 'Zero'

    def compute(self, state: State) -> float:
        return 0
