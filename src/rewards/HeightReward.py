import BMEnvironment
from BMTask import State
from rewards.PenaltyReward import PenaltyRewardFunction


class HeightAndDangerRewardFunction(PenaltyRewardFunction):
    """No only reduce reward for touching danger objects but give positive reward when at higher position"""

    def function_name(self):
        return 'Height_Danger'

    def compute(self, state: State) -> float:
        danger = super().compute(state)
        height = state.agent.position.y / 40.0
        # fixme this code does not looks right; we probably don't need time factor here
        time = pow(float(state.steps) / float(BMEnvironment.BMEnv.MAX_ITERS), 2)

        return danger + ((height - time) * 2)
