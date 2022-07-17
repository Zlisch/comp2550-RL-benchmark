from typing import Set, Optional

import pygame

from Action import Action
from BMTask import State
from agents.Agent import Agent


class HumanAgent(Agent):
    """
    A simple implementation which take human (keyboard) input as action.
    """

    def __init__(self):
        self.pressed: Set[int] = set()
        self.awaiting = True

    def reset(self):
        self.awaiting = True

    def agent_name(self) -> str:
        return 'Human'

    def take_action(self, state: State) -> Optional[Action]:
        # Loop through events:
        action = Action.STAY
        for event in pygame.event.get():
            # Control agent:
            if event.type == pygame.KEYDOWN:
                self.pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.pressed.remove(event.key)
        # update action map according to the pressed keys
        if pygame.K_w in self.pressed:
            action = action if (action.value < 3) else Action(action.value - 3)
        if pygame.K_s in self.pressed:
            action = action if (action.value >= 6) else Action(action.value + 3)
        if pygame.K_a in self.pressed:
            action = action if (action.value % 3 == 0) else Action(action.value - 1)
        if pygame.K_d in self.pressed:
            action = action if (action.value % 3 == 2) else Action(action.value + 1)
        if self.awaiting and action is Action.STAY:
            return None
        self.awaiting = False
        return action

    def update_reward(self, reward: float):
        pass
