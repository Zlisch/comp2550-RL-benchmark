from typing import List

from Box2D import *

from Action import Action


class State:
    """
    A state representation of the game world
    """
    # Box2D parameters:
    VEL_ITERS, POS_ITERS = 6, 2
    TIME_STEP = 1 / 60

    def __init__(self,
                 agent: b2BodyDef,
                 target_object: b2BodyDef,
                 static_objects: List[b2BodyDef],
                 safe_objects: List[b2BodyDef],
                 danger_objects: List[b2BodyDef]):
        # initialize scenario world
        self.world: b2World = b2World(gravity=(0, -10), doSleep=True)
        # create agent in the world
        self.agent: b2Body = self.world.CreateBody(agent)
        # create target object in the world
        self.target_object = self.world.CreateBody(target_object)
        # create static objects in the world:
        self.static_objects: List[b2Body] = [self.world.CreateBody(x) for x in static_objects]
        # create blue dynamic objects in the world:
        self.safe_objects: List[b2Body] = [self.world.CreateBody(x) for x in safe_objects]
        # create red dynamic objects in the world:
        self.danger_objects: List[b2Body] = [self.world.CreateBody(x) for x in danger_objects]
        # list of objects where is contacting agent
        self.agent_contacts = []
        self.update_contacts()
        # total simulated steps
        # fixme move it to reward function
        self.agentHighPoint = 0

        self.steps = 0

    def apply_action(self, action: Action):
        """ Apply the given action into the state and progress the state """
        self.agent.linearVelocity = action.get_velocity()
        self.world.Step(State.TIME_STEP, State.VEL_ITERS, State.POS_ITERS)
        # update contacts
        self.update_contacts()
        # update step
        self.steps += 1

    def update_contacts(self):
        """
        Update the list of body which currently touching agent.
        This method will be automatically called when apply action to the state.
        """
        self.agent_contacts = []
        for contact_edge in self.agent.contacts:
            contact = contact_edge.contact
            if contact.touching:
                body_a = contact.fixtureA.body
                body_b = contact.fixtureB.body
                self.agent_contacts.append(body_b if body_a == self.agent else body_a)

    def check_termination(self) -> bool:
        """Check if the task should terminate (touched target or danger objects)"""
        if self.target_object in self.agent_contacts:
            return True
        return any([contact in self.danger_objects for contact in self.agent_contacts])
