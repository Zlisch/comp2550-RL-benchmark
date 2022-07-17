from enum import IntEnum
from typing import Tuple
import numpy as np

# This should be low to make the tasks hard
from tf_agents.specs import array_spec

MOVEMENT_UNIT = 6  # the constant number indicating what's the distance of movement for a single action.
DIAGONAL_FACTOR = 0.7  # diagonal move distance will be reduced with this factor


def action_spec():
    return array_spec.BoundedArraySpec(shape=(), dtype=np.int32, minimum=0, maximum=8, name='action')


class Action(IntEnum):
    """
    The action space of the agent; the agent must give one of action from the following 9 actions at each timestamp.
    The index of the action are formed in the left-to-right and up-to-bottom order.
    """
    LEFT_UP = 0
    UP = 1
    RIGHT_UP = 2
    LEFT = 3
    STAY = 4
    RIGHT = 5
    LEFT_DOWN = 6
    DOWN = 7
    RIGHT_DOWN = 8

    def get_velocity(self) -> Tuple[float, float]:
        """
        Get the effect velocity to the agent of this action.
        """
        if self is Action.LEFT_UP:
            return -DIAGONAL_FACTOR * MOVEMENT_UNIT, +DIAGONAL_FACTOR * MOVEMENT_UNIT
        if self is Action.UP:
            return 0, +MOVEMENT_UNIT
        if self is Action.RIGHT_UP:
            return +DIAGONAL_FACTOR * MOVEMENT_UNIT, +DIAGONAL_FACTOR * MOVEMENT_UNIT
        if self is Action.LEFT:
            return -MOVEMENT_UNIT, 0
        if self is Action.RIGHT:
            return +MOVEMENT_UNIT, 0
        if self is Action.LEFT_DOWN:
            return -DIAGONAL_FACTOR * MOVEMENT_UNIT, -DIAGONAL_FACTOR * MOVEMENT_UNIT
        if self is Action.DOWN:
            return 0, -MOVEMENT_UNIT
        if self is Action.RIGHT_DOWN:
            return +DIAGONAL_FACTOR * MOVEMENT_UNIT, -DIAGONAL_FACTOR * MOVEMENT_UNIT
        return 0, 0

    @classmethod
    def get_actions(cls):
        return [Action.LEFT_UP, Action.UP, Action.RIGHT_UP, Action.LEFT, Action.RIGHT, Action.LEFT_DOWN, Action.DOWN, Action.RIGHT_DOWN]
