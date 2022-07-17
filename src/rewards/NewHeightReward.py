from math import ceil, floor
from rewards.BMRewardFunction import RewardFunction
from BMTask import State
from BMEnvironment import BMEnv

from math import ceil

class NewHeightReward(RewardFunction):

    def __init__(self, freq: float = 0.4):
        self.freq = freq        

    def function_name(self):
        return 'NewHeightReward'

    def compute(self, state: State) -> float:        

        # Return very negative reward for hitting a red object
        red_hit = False
        for contact_edge in state.agent.contacts:
            contact = contact_edge.contact
            for f in [contact.fixtureA, contact.fixtureB]:
                b = f.body
                if b in state.danger_objects:
                    if contact.touching:
                        red_hit = True
                        break        
        if red_hit: return -1000 + (state.steps / 2)
        
        # Return very positive reward for reaching the top
        if state.agent.position.y > 36:
            return 1000
                  
        # the + <small value> here means no extra reward for being slow
        if state.agent.position.y > state.agentHighPoint:             
            # print("Progress: " + str(state.agentHighPoint))
            state.agentHighPoint = ceil(state.agent.position.y / self.freq) * self.freq
            # Higher reward for higher height + sooner, but maintain sparseness
            # return 1 + (3 * (state.agentHighPoint / 40) * (2 - (state.steps / BMEnv.MAX_ITERS)))
            return 2
        else:
            # print("High Point: " + str(state.agentHighPoint))
            # print("Agent y: " + str(state.agent.position.y))
            # print("")
            return -0.1                    