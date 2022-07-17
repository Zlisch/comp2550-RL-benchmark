from cmath import pi
from math import pi, cos, sin, atan2

import numpy as np
import pygame
from Box2D import *
from tf_agents.specs import array_spec

from BMTask import State
from observations.Observations import Observation
from rendering import RenderEngine


class DoubleRayCastObservation(Observation):
    """    
    Perceptual observation using rays cast around the agent.
    Each ray has 12 channels. 4 for each kind of object.    
    When the ray first hits a particular kind of object,
    The distance and normal angle are taken.
    This is also done for when the ray exits the object.
    This extra information from behind objects allows for
    more detailed scene info.
    The entry point is found by the raycast forwards and the
    exit point is found by the raycast backwards
    """

    def __init__(self, numrays: int = 100, raydistance: int = 25):
        """                
        """
        self.numrays = numrays
        self.raydistance = raydistance

        self.raypoints = []

        for i in range(0, numrays):
            raypointx = cos((i / numrays) * 2 * pi) * self.raydistance
            raypointy = sin((i / numrays) * 2 * pi) * self.raydistance
            self.raypoints.append((raypointx, raypointy))

    def observation_spec(self):
        """
        """
        return array_spec.BoundedArraySpec(
            shape=(self.numrays * 12,), dtype=np.float64, minimum=0.0, maximum=1.0, name='observation')

    def compute_observation(self, state: State):
        """
        Carries out a series of ray casts around the agent
        """

        observation = np.array([], dtype=np.float64)

        raystart = state.agent.position
        for i in range(0, self.numrays):
            rayend = (self.raypoints[i][0] + raystart[0], self.raypoints[i][1] + raystart[1])

            # Do forwards:
            forwardcallback = DoubleRayCastObservation.RaycastForwards(state)
            state.world.RayCast(forwardcallback, raystart, rayend)

            # Do backwards:
            backwardcallback = DoubleRayCastObservation.RaycastBackwards(staticBody=forwardcallback.staticHit,
                                                                         safeBody=forwardcallback.safeHit,
                                                                         dangerBody=forwardcallback.dangerHit)
            state.world.RayCast(backwardcallback, rayend, raystart)

            # Collate raycast data into a vector:
            vec = np.zeros(dtype=np.float64, shape=(12,))
            # Static:
            vec[0] = forwardcallback.staticHitDis
            vec[1] = forwardcallback.staticHitNormal
            vec[2] = backwardcallback.staticHitDis
            vec[3] = backwardcallback.staticHitNormal

            # Safe:
            vec[4] = forwardcallback.safeHitDis
            vec[5] = forwardcallback.safeHitNormal
            vec[6] = backwardcallback.safeHitDis
            vec[7] = backwardcallback.safeHitNormal

            # Danger:
            vec[8] = forwardcallback.dangerHitDis
            vec[9] = forwardcallback.dangerHitNormal
            vec[10] = backwardcallback.dangerHitDis
            vec[11] = backwardcallback.dangerHitNormal

            # Add vector to observation                 
            observation = np.append(observation, vec)

        return observation

    def render_observation(self, state: State, surf: pygame.Surface):

        surf.fill(RenderEngine.BACKGROUND_COLOR)

        RenderEngine.render_shape(surf, state.agent, RenderEngine.AGENT_COLOR)

        raystart = state.agent.position
        for i in range(0, self.numrays):
            rayend = (self.raypoints[i][0] + raystart[0], self.raypoints[i][1] + raystart[1])

            # Do forwards:
            forwardcallback = DoubleRayCastObservation.RaycastForwards(state)
            state.world.RayCast(forwardcallback, raystart, rayend)

            # Do backwards:
            backwardcallback = DoubleRayCastObservation.RaycastBackwards(staticBody=forwardcallback.staticHit,
                                                                         safeBody=forwardcallback.safeHit,
                                                                         dangerBody=forwardcallback.dangerHit)
            state.world.RayCast(backwardcallback, rayend, raystart)

            def to_center(p: b2Vec2):
                """ Helper Function """
                if p == None:
                    return (0, 0)
                else:
                    c = RenderEngine.vertices2coords([(p[0], p[1])], surf.get_width(), surf.get_height())
                    return (c[0][0], c[0][1])

            def add_and_center(p1: b2Vec2, p2: b2Vec2):
                """ Another helper """
                if (p1 == None) or (p2 == None):
                    return (0, 0)
                else:
                    c = RenderEngine.vertices2coords([(p1[0] + 0.5 * p2[0], p1[1] + 0.5 * p2[1])], surf.get_width(),
                                                     surf.get_height())
                    return (c[0][0], c[0][1])

            # Draw small circles where the ray hits:                        
            pygame.draw.circle(surf, center=to_center(forwardcallback.staticHitPos), radius=1.5, color=(0, 0, 0))
            pygame.draw.circle(surf, center=to_center(backwardcallback.staticHitPos), radius=1.5, color=(0, 0, 0))

            pygame.draw.circle(surf, center=to_center(forwardcallback.safeHitPos), radius=1.5, color=(0, 0, 255))
            pygame.draw.circle(surf, center=to_center(backwardcallback.safeHitPos), radius=1.5, color=(0, 0, 255))

            pygame.draw.circle(surf, center=to_center(forwardcallback.dangerHitPos), radius=1.5, color=(255, 0, 0))
            pygame.draw.circle(surf, center=to_center(backwardcallback.dangerHitPos), radius=1.5, color=(255, 0, 0))

            # Draw normals where the ray hits:            
            pygame.draw.aaline(surf,
                               start_pos=to_center(forwardcallback.staticHitPos),
                               end_pos=add_and_center(forwardcallback.staticHitPos, forwardcallback.staticHitNormVec),
                               color=(0, 0, 0))
            pygame.draw.aaline(surf,
                               start_pos=to_center(backwardcallback.staticHitPos),
                               end_pos=add_and_center(backwardcallback.staticHitPos, backwardcallback.staticHitNormVec),
                               color=(0, 0, 0))

            pygame.draw.aaline(surf,
                               start_pos=to_center(forwardcallback.safeHitPos),
                               end_pos=add_and_center(forwardcallback.safeHitPos, forwardcallback.safeHitNormVec),
                               color=(0, 0, 255))
            pygame.draw.aaline(surf,
                               start_pos=to_center(backwardcallback.safeHitPos),
                               end_pos=add_and_center(backwardcallback.safeHitPos, backwardcallback.safeHitNormVec),
                               color=(0, 0, 255))

            pygame.draw.aaline(surf,
                               start_pos=to_center(forwardcallback.dangerHitPos),
                               end_pos=add_and_center(forwardcallback.dangerHitPos, forwardcallback.dangerHitNormVec),
                               color=(255, 0, 0))
            pygame.draw.aaline(surf,
                               start_pos=to_center(backwardcallback.dangerHitPos),
                               end_pos=add_and_center(backwardcallback.dangerHitPos, backwardcallback.dangerHitNormVec),
                               color=(255, 0, 0))

        pass

    class RaycastBackwards(b2RayCastCallback):
        """
        Manages ray cast backwards from raypoint to agent
        """

        def __init__(self, staticBody: b2Body, safeBody: b2Body, dangerBody: b2Body, return_render_info: bool = False,
                     **kwargs):

            b2RayCastCallback.__init__(self)
            self.staticBody = staticBody
            self.safeBody = safeBody
            self.dangerBody = dangerBody

            # Fractional distances:
            self.staticHitDis = 1.0
            self.safeHitDis = 1.0
            self.dangerHitDis = 1.0

            # Normal angle in radians:
            self.staticHitNormal = 0.0
            self.safeHitNormal = 0.0
            self.dangerHitNormal = 0.0

            # The following are helpful for displaying
            # the info that the agent can see
            # Hit points:
            self.staticHitPos = None
            self.dangerHitPos = None
            self.safeHitPos = None

            # Normal Vectors:
            self.staticHitNormVec = None
            self.dangerHitNormVec = None
            self.safeHitNormVec = None

        def ReportFixture(self, fixture, point, normal, fraction):

            body = fixture.body
            if body == self.staticBody:
                self.staticHitDis = 1 - fraction  # to account for backwardsness
                self.staticHitNormal = atan2(normal[1], normal[0]) / (pi)  # should this be adjusted?
                self.staticHitNormVec = normal

            if body == self.safeBody:
                self.safeHitDis = 1 - fraction
                self.safeHitNormal = atan2(normal[1], normal[0]) / (pi)
                self.safeHitPos = point
                self.safeHitNormVec = normal

            if body == self.dangerBody:
                self.dangerHitDis = 1 - fraction
                self.dangerHitNormal = atan2(normal[1], normal[0]) / (pi)
                self.dangerHitPos = point
                self.dangerHitNormVec = normal

            return 1.0

    class RaycastForwards(b2RayCastCallback):
        """
        Manages ray cast forwards from agent to raypoint
        """

        def __init__(self, state: State, **kwargs):
            b2RayCastCallback.__init__(self)
            self.staticHit: b2Body = None
            self.safeHit: b2Body = None
            self.dangerHit: b2Body = None

            # Fractional distances:
            self.staticHitDis = 1.0
            self.safeHitDis = 1.0
            self.dangerHitDis = 1.0

            # Normal angle in radians:
            # Not sure what this value should be initialised to
            self.staticHitNormal = 0.0
            self.safeHitNormal = 0.0
            self.dangerHitNormal = 0.0

            # The following are helpful for displaying
            # the info that the agent can see
            # Hit points:
            self.staticHitPos = None
            self.dangerHitPos = None
            self.safeHitPos = None

            # Normal Vectors:
            self.staticHitNormVec = None
            self.dangerHitNormVec = None
            self.safeHitNormVec = None

            self.state = state

        def ReportFixture(self, fixture, point, normal, fraction):

            body = fixture.body
            if self.staticHit == None:
                if body in self.state.static_objects:
                    self.staticHit = body
                    self.staticHitDis = fraction
                    self.staticHitNormal = atan2(normal[1], normal[0]) / (pi)
                    self.staticHitPos = point
                    self.staticHitNormVec = normal

            if self.safeHit == None:
                if body in self.state.safe_objects:
                    self.safeHit = body
                    self.safeHitDis = fraction
                    self.safeHitNormal = atan2(normal[1], normal[0]) / (pi)
                    self.safeHitPos = point
                    self.safeHitNormVec = normal

            if self.dangerHit == None:
                if body in self.state.danger_objects:
                    self.dangerHit = body
                    self.dangerHitDis = fraction
                    self.dangerHitNormal = atan2(normal[1], normal[0]) / (pi)
                    self.dangerHitPos = point
                    self.dangerHitNormVec = normal

            if (self.staticHit != None) & (self.safeHit != None) & (self.dangerHit != None):
                # stop when all objects have been found (or it will stop anyway if nothing is hit)
                return 0.0

            return 1.0
            