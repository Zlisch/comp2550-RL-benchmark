""" Imports: """
# Tensorflow Stuff:
from typing import Optional

import tensorflow as tf
from tensorflow import keras
from keras import layers
from tf_agents.agents import TFAgent
from tf_agents.agents.dqn import dqn_agent
from tf_agents.networks import sequential
from tf_agents.specs import tensor_spec
from tf_agents.utils import common

from tf_agents.trajectories import time_step as ts

from numpy import ndarray

from Action import Action, action_spec
from agents.ImageBasedAgent import ImageBasedAgent


class ImageDQNAgent(ImageBasedAgent):

    def __init__(self):
        super(ImageDQNAgent, self).__init__()
        # Agent model:
        self.model = None
        self.step: Optional[ts.TimeStep] = None
        self.last_reward = 0

    def train(self,
              learning_rate: float,
              time_step_spec: ts.TimeStep):
        """ Create Agent Q-Net: """
        # Hidden Layers:
        h_layers = (30, 40, 30)
        # Action Specification:
        action_tensor_spec = tensor_spec.from_spec(action_spec())
        num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1

        def dense_layer(num_units):
            """ Helper function to generate dense layers in Q-net """
            return layers.Dense(num_units,
                                activation=tf.keras.activations.relu,
                                kernel_initializer=tf.keras.initializers.VarianceScaling(
                                    scale=2.0, mode='fan_in', distribution='truncated_normal'
                                ))

        # Create the dense layers:
        dense_layers = [dense_layer(units) for units in h_layers]

        # Create the output layers:
        output_layer = layers.Dense(num_actions,
                                    activation=None,
                                    kernel_initializer=tf.keras.initializers.RandomUniform(
                                        minval=-0.03, maxval=0.03
                                    ),
                                    bias_initializer=keras.initializers.Constant(-0.2))

        q_net = sequential.Sequential(dense_layers + [output_layer])
        """ Create Agent: """
        # Agent learning optimizer:
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        # Counter:
        train_step_counter = tf.Variable(0)
        # Agent model:
        self.model = dqn_agent.DqnAgent(optimizer=optimizer,
                                        time_step_spec=time_step_spec,
                                        action_spec=action_spec(),
                                        q_network=q_net,
                                        epsilon_greedy=0.1,
                                        td_errors_loss_fn=common.element_wise_squared_loss,
                                        train_step_counter=train_step_counter)
        self.model.initialize()

    def reset(self):
        super(ImageDQNAgent, self).reset()
        self.step = None
        self.last_reward = 0

    def get_model(self) -> TFAgent:
        return self.model

    def update_reward(self, reward: float):
        self.last_reward = reward

    def agent_name(self) -> str:
        return "DQN-image"

    def take_action_from_image(self, image: ndarray) -> Action:
        if self.step is None:
            self.step = ts.restart(image)
        else:
            self.step = ts.transition(observation=image, reward=self.last_reward, discount=0.9)
        action_step = self.get_model().policy.action(self.step)
        action = Action(getattr(action_step, 'action'))
        return action
