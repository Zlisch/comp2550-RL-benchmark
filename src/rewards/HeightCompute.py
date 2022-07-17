from BMTask import State


class HeightCompute():
    @classmethod
    def compute_height(cls, state: State):
        return state.agent.position[1]