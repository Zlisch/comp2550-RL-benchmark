from Box2D.Box2D import b2Vec2
import numpy as np
from Action import Action
from BMTask import State

from agents.Agent import Agent
from observations.ForwardRaycastObservation import ForwardRaycastObservation

class HeuristicAvoidAgent(Agent):
    """
    Choose an action that maximize its distance from the nearest 
    dangerous object.
    """
    def __init__(self) -> None:
        super().__init__()
        self.options = [Action.LEFT_UP, Action.LEFT, Action.LEFT_DOWN, Action.RIGHT, Action.RIGHT_DOWN, Action.RIGHT_UP, Action.DOWN, Action.STAY, Action.UP]
        self.last_reward = 0

    def reset(self):
        self.last_reward = 0

    def agent_name(self) -> str:
        return "HeuristicAvoidAgent"

    def take_action(self, state: State) -> Action:

        forwardRaycastResult = ForwardRaycastObservation(state)
        scores = np.zeros(9, dtype=np.float64)
        for i in range(0, len(self.options)):
            scores[i] = self.score(self.options[i], forwardRaycastResult)
        index_max = 0
        scr = scores[0]
        for i in range(0, len(self.options)):
            if (scores[i]) > scr:
                scr = scores[i]
                index_max = i
        return self.options[index_max]

    def score(self, action: Action, observation: ForwardRaycastObservation):

        reds = observation.get_red_dis_angles()
        blues = observation.get_blue_dis_angles()
        statics = observation.get_static_dis_angles()

        def cal_sum_distances(objs, pos: b2Vec2, color: str):
            sum = 0
            for other in objs:
                if (other[1] - pos[1] > 0):
                    sum += ((other[0] - pos[0])**2 + (other[1] - pos[1])**2)**0.5
            return sum

        def cal_min_distances(objs, pos: b2Vec2, color: str):
            min = 0
            min = ((objs[0][0] - pos[0])**2 + (objs[0][1] - pos[1])**2)**0.5
            min_obj = objs[0]
            for other in objs:
                if (other[1] - pos[1] > 0):
                    tmp = ((other[0] - pos[0])**2 + (other[1] - pos[1])**2)**0.5
                    if tmp < min:
                        min = tmp
                        min_obj = other
            return [min_obj[0],min_obj[1], min, color]

        min_static_curr = cal_min_distances(statics, observation.pos, "static")

        if (abs(min_static_curr[0] - observation.pos[0]) - abs(min_static_curr[1] - observation.pos[1]) < 0 
        and abs(min_static_curr[1] - observation.pos[1]) < 1):
            # print("cannot move up")
            newPos = [action.get_velocity()[0] + observation.pos[0], observation.pos[1]]
        else:
            newPos = [action.get_velocity()[0] + observation.pos[0], action.get_velocity()[1] + observation.pos[1]]

        dis_sum_reds = cal_sum_distances(reds, newPos, "red")
        dis_sum_blues = cal_sum_distances(blues, newPos, "blue")
        min_static = cal_min_distances(statics, newPos, "static")
        dis_min_statics = 0.1 * min_static[2]
        score = dis_sum_reds + dis_sum_reds * action.get_velocity()[1] + dis_min_statics

        if (dis_sum_reds < 1.0 and dis_sum_blues < 1.0):
            # if not stuck with moving upwards
            if (abs(min_static[0] - newPos[0]) - abs(min_static[1] - newPos[1]) > 0):
                score = action.get_velocity()[1]

        return score

    def update_reward(self, reward: float):
        self.last_reward = reward
