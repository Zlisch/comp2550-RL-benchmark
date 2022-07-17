import numpy as np
import pygame
from BMTask import State
from observations.DoubleRaycastObservation import DoubleRayCastObservation


class ForwardRaycastObservation(DoubleRayCastObservation):

    def __init__(self, state: State) -> None:
        super().__init__(30, 20)
        self.pos = state.agent.position
        self.observation = np.array([], dtype=np.float64)
        self.compute_observation(state)

    def observation_spec(self):
        return super().observation_spec()

    def compute_observation(self, state: State):

        self.observation = np.array([], dtype=np.float64)

        raystart = state.agent.position
        for i in range(0, self.numrays):
            rayend = (self.raypoints[i][0] + raystart[0], self.raypoints[i][1] + raystart[1])

            # Do forwards:
            forwardcallback = DoubleRayCastObservation.RaycastForwards(state)
            state.world.RayCast(forwardcallback, raystart, rayend)

            # Add wrapper to observation                 
            self.observation = np.append(self.observation, forwardcallback)

        return self.observation

    def render_observation(self, state: State, surf: pygame.Surface):
        return super().render_observation(state, surf)

    def get_red_dis_angles(self):

        red_dis_angles = []
        for i in range(0, self.numrays):

            if self.observation[i].dangerHitPos != None:

                red_dis_angles.append(self.observation[i].dangerHitPos)
                # red_dis_angles.append([self.observation[i].dangerHitPos, self.observation[i].dangerHitNormVec])
        return red_dis_angles

    def get_blue_dis_angles(self):

        blue_dis_angles = []
        for i in range(0, self.numrays):

            if self.observation[i].safeHitPos != None:

                blue_dis_angles.append(self.observation[i].safeHitPos)
                # blue_dis_angles.append([self.observation[i].safeHitPos, self.observation[i].safeHitNormVec])
        return blue_dis_angles

    def get_static_dis_angles(self):

        static_dis_angles = []
        for i in range(0, self.numrays):

            if self.observation[i].staticHitPos != None:

                static_dis_angles.append(self.observation[i].staticHitPos)
                # static_dis_angles.append([self.observation[i].staticHitPos, self.observation[i].staticHitNormVec])
        return static_dis_angles