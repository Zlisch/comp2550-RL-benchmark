from math import exp

from BMTask import State
from rewards.BMRewardFunction import RewardFunction


class EvaluateRewardFunction(RewardFunction):
    """The reward function will penalize touching red objects and award touching target object """

    def function_name(self) -> str:
        return 'Evaluate'

    def compute(self, state: State) -> float:
        if any([contact in state.danger_objects for contact in state.agent_contacts]):
            return -1000.0
        elif state.target_object in state.agent_contacts:
            return 1000.0
        h = state.agent.position.y
        return 1 / (1 + exp(-h / 10.0)) - 1
