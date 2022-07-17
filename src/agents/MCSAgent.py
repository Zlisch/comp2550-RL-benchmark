import re
from typing import DefaultDict

from pygame.constants import TIMER_RESOLUTION
from Action import Action
from BMTask import State
from agents.Agent import Agent
from observations.PerfectObservation import PerfectObservation
from rendering.RenderEngine import *
from rewards.BMRewardFunction import RewardFunction


class MCSAgent(Agent):

    def __init__(self):
        self.actions = []  # if empty, run MCS to generate. If non-empty, directly apply the stored actions.
        self.simulation_no = 100

    def agent_name(self) -> str:
        return "MCSAgent"

    def set_reward_func(self, reward_func: RewardFunction):
        # will be called in the driver setup
        self.reward_func = reward_func

class MonteCarloTreeSearchNode():
    
    TIMER_RESOLUTION = pygame.TIMER_RESOLUTION

    def __init__(self, state: State, reward_func: RewardFunction, parent=None, parent_action=None):
        self.observation = PerfectObservation(state)
        self.reward_func = reward_func
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = DefaultDict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def get_legal_actions(self): 
        '''
        Constructs a list of all
        possible actions from current state.
        Returns a list.
        '''
        return Action.get_actions()

    def is_game_over(self):
        '''
        If the agent has arrived the top the game is over.
        Returns true if over otherwise false.
        '''
        return OFFSET_Y * 2 - self.observation.pos[1] < 5

    def game_result(self):
        '''
        Returns 1 if reach the top otherwise -1.
        '''
        if OFFSET_Y * 2 - self.observation.pos[1] < 5:
            return 1
        return -1

    def move(self, action: Action):
        '''
        Update the state based on given action.
        '''
        # can't do this discretizing the physics is a totally new topic.