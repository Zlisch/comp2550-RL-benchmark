from BMTask import State
from rewards.BMRewardFunction import RewardFunction


class PenaltyRewardFunction(RewardFunction):
    """Apply negative reward if the agent is touching danger objects. """

    def function_name(self) -> str:
        return 'Penalty'

    def compute(self, state: State) -> float:
        red_hit = any([contact in state.danger_objects for contact in state.agent_contacts])
        # -1 is enough to always overturn the positive part of the reward:
        return -0.5 if red_hit else 0.0
