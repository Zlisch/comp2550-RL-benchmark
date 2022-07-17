""" Imports: """
# Tensorflow Stuff:
import training as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import py_driver
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import sequential
from tf_agents.policies import py_tf_eager_policy
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import reverb_replay_buffer
from tf_agents.replay_buffers import reverb_utils
from tf_agents.trajectories import trajectory
from tf_agents.specs import tensor_spec
from tf_agents.utils import common  

# BM stuff:
import BMEnvironment
import StateQuery
import templates.Seesaw_Template
import templates.Roof_Template
import templates.Blank_Template
import templates.Tower_Template
import rewards.RewardFunctions
import observations.Observations

from Box2D import *
from BMTask import State

import time


""" Hyper parameters: """

num_iterations = 20000

initial_collect_steps = 100
collect_steps_per_iteration = 1
replay_buffer_max_length = 100000

batch_size = 64
learning_rate = 1e-3
log_interval = 200

num_eval_episodes = 10 
eval_interval = 1000

env = tf_py_environment.TFPyEnvironment(  BMEnvironment.BMEnv(  template=templates.Tower_Template.Tower(),
                                                                reward_fn=rewards.RewardFunctions.Height_and_Danger_RewardFunction(),
                                                                observation_fn=observations.Observations.DoubleRayCastObservation(50, 20),
                                                                variant=0.5,
                                                                rendering=False ) )

reward_list = []
number_of_episodes = 2

print("querypoint stress test:")

world = b2World(gravity=(0, -10), doSleep=True)

body = b2BodyDef(position=(-2, 20),
                                linearVelocity = (2, 2),
                                fixtures=b2FixtureDef(shape=b2PolygonShape(vertices = [(-3, -2), (1, 1), (4, -1)]),
                                                      density=1.0,
                                                      friction=0.5,
                                                      restitution=0.5),
                                type=b2_dynamicBody)

world.CreateBody(body)           

point = (-6, 20)

shape=b2PolygonShape(vertices = [(-3, -2), (1, 1), (4, -1)])

prevtime = time.time()
within = False
for i in range(0, 10000):
  within = StateQuery.queryPointShape(shape, point, body.position)

print("Result: " + str(within))

timetaken = time.time() - prevtime
timetaken *= 10**3

print("Time: " + str(timetaken))

for _ in range(number_of_episodes):        
  reward_t = 0
  steps_t = 0
  episode_reward = 0

  env.reset()
  print("Env Reset")
  
  while True:    
    # action = tf.random.uniform([1], 0, 9, dtype=tf.int32)
    action = 0
    next_time_step = env.step(action)
    if env.current_time_step().is_last():
      break    
    episode_reward += next_time_step.reward.numpy()
  reward_list.append(episode_reward)

print(reward_list)