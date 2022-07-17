# Tensorflow Stuff
from typing import Tuple

import training as tf
from tf_agents.environments import py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
import numpy as np

# BM stuff:
from BMTemplate import Template
from BMTask import State
from Action import Action
from rendering import RenderEngine
from rewards.BMRewardFunction import RewardFunction
from observations.Observations import Observation

# Box2D stuff:
from Box2D import *

# Pygame stuff:
import pygame

# from BMApplication import Application


class BMEnv(py_environment.PyEnvironment):
    """ 
    Defines an environment in which a tf-agent can learn.
    Follows the implementation guide from tensorflow very closely.  
    """
    MAX_ITERS = (1 / State.TIME_STEP) * 9
    
    def __init__(   self, 
                    template: Template, 
                    variantRange: Tuple[float, float],
                    reward_fn: RewardFunction, 
                    observation_fn: Observation):  
        """
        Initialises the benchmark learning environment
        """

        # Represents the 9 movement directions of the agent:
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=8, name='action')
        
        # Represents the image which the agent receives as an observation:        
        self._observation_spec = observation_fn.observation_spec()

        # Initialise the state using the world of the template with a variant within the range:
        self.template = template        
        self.variantRange = variantRange
        variant = (np.random.random() * (self.variantRange[1] - self.variantRange[0])) + self.variantRange[0]
        self.state = self.template.create_world(variant)        

        # Set the reward function for the environment:
        self.reward = reward_fn

        # Set the observation function for the environment:
        self.observation = observation_fn

        # This appears to be conventional:
        self._episode_ended = False

        # Iterations of the timestep:
        self.iters = 0            

        # If rendering, then set that up:
        # init pygame for the application
        pygame.init()                

        self.screen = None
        self.surf = None                    

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        """ 
        Reset the state of the world
        """
        variant = (np.random.random() * (self.variantRange[1] - self.variantRange[0])) + self.variantRange[0]
        self.state = self.template.create_world(variant)
        self._episode_ended = False
        self.iters = 0

        return ts.restart(  observation = self.observation.compute_observation(self.state),      )
    
    def _step(self, action):
        """ 
        Steps the environment forward in time, implementing the action
        taken by the agent 
        Returns: 
        - The new state
        - The reward value associated to the new state
        - The new observation for the agent
        """
        
        if self._episode_ended:
            return self.reset()        

        # Apply the action of the agent to the state:
        # The physics step is also done here
        self.state.apply_action(Action(action)) # the action needs to be converted                        
        self.iters += 1 

        # print("Apply Action Time: " + str(timetaken))       
        
        reward = self.reward.compute(self.state)

        # if reward maginitude is very high then end the episode:
        if (reward > 50) or (reward < -50) or (self.iters > BMEnv.MAX_ITERS):            
            self._episode_ended = True
            return ts.termination(  observation = self.observation.compute_observation(self.state),
                                    reward=reward)

        # otherwise continue normally:
        return ts.transition(   reward = reward,
                                observation = self.observation.compute_observation(self.state), 
                                discount = 1.0  ) 
        

        """
        # If the agent has reached the top, then the episode should end with high reward     
        if self.state.agent.position.y > 36: # 36 is arbitrary for now
            self._episode_ended = True
            return ts.termination(  observation = self.observation.compute_observation(self.state),
                                    reward = 100.0  )
        # Otherwise the episode may end due to time constraints:
        if self.iters > BMEnv.MAX_ITERS:            
            self._episode_ended = True
            return ts.termination(  reward = self.reward.compute(self.state),
                                    observation = self.observation.compute_observation(self.state)  )                                        
        # Otherwise continue as normal:
        else:
            return ts.transition(   reward = self.reward.compute(self.state),
                                    observation = self.observation.compute_observation(self.state), 
                                    discount = 1.0  )    
        """    

    def render(self, mode):

        """ Facilitates viewership of the training process """
        # Check that the window has not been closed:             

        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((800, 600))
            self.surf = pygame.Surface(self.screen.get_size())
            
        # Use the application render code to render the world to the surface:
        if mode=='render_observation':
            self.observation.render_observation(state=self.state, surf=self.surf)  
        else:
            RenderEngine.render_state(self.surf, self.state)

        
        return np.transpose(
            np.array(pygame.surfarray.pixels3d(self.surf)), axes=(1, 0, 2)
        )

        

