from rewards.BMRewardFunction import RewardFunction
from BMTask import State

class SimpleRewardFunction(RewardFunction):
    def function_name(self) -> str:
        return 'Simple'

    def compute(self, state: State) -> float:
        red_hit = False
        for contact_edge in state.agent.contacts:
            contact = contact_edge.contact
            for f in [contact.fixtureA, contact.fixtureB]:
                b = f.body
                if b in state.danger_objects:
                    if contact.touching:
                        red_hit = True
                        break        
        return -100.0 if red_hit else 0.0 
