from random import random
from Action import Action
from BMTask import State
from agents.Agent import Agent
import numpy as np

class DistributionAgent(Agent):
    """
    This agent accepts a distribution of probabilities (9 of them) 
    to take its actions according to.
    For example:
    dist = [0.25, 0.5, 0.25, 0, 0, 0, 0, 0, 0]
    Means mostly move upwards, but sometimes move left and up, or right and up.    
    """
    def __init__(self, dist: list[float]):
        distsum = sum(dist)
        dist = [float(x / distsum) for x in dist] # normalise
        intervals = np.zeros(10)        
        cumsum = 0.0    
        for i in range(1, 10):
            cumsum += dist[i - 1]
            intervals[i] = cumsum
            
        self.intervals = intervals

    def agent_name(self) -> str:
        return 'DistributionAgent' 
    
    def take_action(self, state: State) -> Action:        
        randomChoice = random()
        action = 0

        for i in range(1, 10):
            if ((self.intervals[i - 1] <= randomChoice) & (randomChoice < self.intervals[i])):
                return Action(i - 1)

    def update_reward(self, reward: float):
        """The reward which agent received from the last action """
        pass
        

            

        