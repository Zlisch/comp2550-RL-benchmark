import csv
import gc
import os
import time

import imageio
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import tf_py_environment
from tf_agents.metrics import tf_metrics
from tf_agents.policies import random_tf_policy, TFPolicy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.specs import tensor_spec
from tf_agents.utils import common

from BMTemplate import Template
from agents import Agents
from agents.Agent import Agent
from agents.TrainableAgent import TrainableAgent
from rewards import RewardFunctions
from templates import Templates
from training.TensorFlowEnvironment import Sandbox
from training.TrainingConfig import TrainingConfig

""" Hyper parameters: """

# Number of episodes
discount_factor = 0.95

# Optimizer learning rate:
# learning_rate = 1e-3
learning_rate = 0.5e-3

# Number of training episodes between evaluations:
log_interval = 50

initial_collect_steps = 50
collect_steps_per_iteration = 100
replay_buffer_max_length = 100000

batch_size = 128


def compute_return(policy, env, py_env, filename: str = None, fps=60):
    """ Creates a video where actions are mapped out according to the given policy """
    if filename is None:
        return run_evaluation(policy, env, py_env)
    else:
        filename = filename + ".mp4"
        with imageio.get_writer(filename, fps=fps) as video:
            video.append_data(py_env.render(mode='render_normal'))
            return run_evaluation(policy, env, py_env, video)


def run_evaluation(policy, env, py_env, video=None):
    """Run simulation of evaluation"""
    episode_return = 0.0
    steps = 0
    time_step = env.reset()
    while not time_step.is_last():
        action_step = policy.action(time_step)
        time_step = env.step(action_step)
        episode_return += time_step.reward
        steps = steps + 1
        if video is not None:
            video.append_data(py_env.render(mode='render_normal'))
    return steps, float(episode_return[0])


class Trainer:
    def __init__(self):
        self.max_iter_eval = 10
        self.max_iter_train = 5000
        self.max_depth = 1000
        self.variant_range = (0.0, 1.0)
        self.train_reward_fn = RewardFunctions.get_reward_function_by_name('zero')
        self.eval_reward_fn = RewardFunctions.get_reward_function_by_name('zero')
        self.export_video = False

    def run(self, config: TrainingConfig):
        self.max_iter_train = config.train_iteration
        self.max_iter_eval = config.eval_iteration
        self.max_depth = config.max_depth
        self.train_reward_fn = RewardFunctions.get_reward_function_by_name(config.train_reward_func_name)
        self.eval_reward_fn = RewardFunctions.get_reward_function_by_name(config.eval_reward_func_name)
        self.variant_range = (config.lower_variant, config.upper_variant)
        self.export_video = config.export_video
        templates = Templates.get_all_templates()
        if config.temp_name_list != '':
            templates = [Templates.get_template_by_name(s) for s in config.temp_name_list.split(',')]
        agent = Agents.get_agent_by_name(config.agent_name)
        csv_path = '../experiment_result/' + agent.agent_name()
        if not os.path.exists(csv_path):
            os.makedirs(csv_path)
        # run templates
        for template in templates:
            agent.reset()
            eval_result = self.run_template(agent, template)
            # generate csv result file
            csv_name = csv_path + '/' + template.template_name() + '.csv'
            with open(csv_name, mode='w', newline='', encoding='utf-8') as csv_file:
                fields = ['index', 'steps', 'episode_reward', 'average_reward']
                writer = csv.DictWriter(csv_file, fieldnames=fields)
                writer.writeheader()
                index = 0
                for steps, episode_return in eval_result:
                    avg_return = episode_return / steps
                    writer.writerow({'index': str(index),
                                     'steps': str(steps),
                                     'episode_reward': str(episode_return),
                                     'average_reward': str(avg_return)})
                    index = index + 1

    def run_template(self, agent: Agent, temp: Template):
        video_path = '../videos/' + agent.agent_name() + '/' + temp.template_name()
        if not isinstance(agent, TrainableAgent):
            raise Exception("Only trainable agent can be selected")
        """ Create Environments: """

        # Choose observation function:
        observation_fn = agent.get_observation()

        # Training Environment:
        train_py_env = Sandbox(self.max_depth,
                               template=temp,
                               variant_range=self.variant_range,
                               reward_function=self.train_reward_fn,
                               observation=observation_fn,
                               discount_factor=discount_factor)

        # Evaluation Environment:
        eval_py_env = Sandbox(self.max_depth,
                              template=temp,
                              variant_range=self.variant_range,
                              reward_function=self.eval_reward_fn,
                              observation=observation_fn,
                              discount_factor=discount_factor)

        # Convert to TF environments:
        train_env = tf_py_environment.TFPyEnvironment(train_py_env)
        eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

        agent.train(learning_rate, train_env.time_step_spec())
        model = agent.get_model()

        """ Replay Buffer """

        collect_data_spec = tensor_spec.from_spec(model.collect_data_spec)

        replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(data_spec=collect_data_spec,
                                                                       batch_size=train_env.batch_size,
                                                                       max_length=replay_buffer_max_length)

        """ Drivers: """
        metric = tf_metrics.AverageReturnMetric()

        observers = [metric, replay_buffer.add_batch]

        random_policy = random_tf_policy.RandomTFPolicy(action_spec=model.action_spec,
                                                        time_step_spec=train_env.time_step_spec())

        dynamic_step_driver.DynamicStepDriver(env=train_env,
                                              policy=random_policy,
                                              observers=observers,
                                              num_steps=initial_collect_steps).run(time_step=train_env.reset())

        dataset = replay_buffer.as_dataset(
            num_parallel_calls=8,
            sample_batch_size=batch_size,
            num_steps=2).prefetch(3)
        # dataset
        # print(dataset)

        iterator = iter(dataset)

        """ Train Agent: """

        start_time = time.time()

        model.train = common.function(model.train)

        model.train_step_counter.assign(0)

        # avg_return = compute_avg_return(train_env, model.policy, num_eval_episodes)
        returns = []

        train_env.reset()

        collect_driver = dynamic_step_driver.DynamicStepDriver(env=train_env,
                                                               observers=observers,
                                                               policy=model.collect_policy,
                                                               num_steps=collect_steps_per_iteration)
        print('Training on ' + temp.template_name())
        for i in range(self.max_iter_train):
            collect_driver.run(maximum_iterations=self.max_depth)
            experience, _ = next(iterator)
            train_loss = model.train(experience).loss
            if i % log_interval == 0:
                print('training index {0}: loss = {1}'.format(i, train_loss))
        time_taken = time.time() - start_time
        print("Training Time: " + str(time_taken))
        start_time = time.time()
        if not os.path.exists(video_path):
            os.makedirs(video_path)
        for i in range(self.max_iter_eval):
            eval_env.reset()
            export_path = video_path + "/eval-" + str(i) if self.export_video else None
            steps, episode_return = compute_return(model.collect_policy,
                                                   eval_env,
                                                   eval_py_env,
                                                   export_path)
            avg_return = episode_return / steps
            # avg_return = compute_avg_return(eval_env, model.policy, num_eval_episodes)
            print('evaluation index {0}: Average Return = {1}'.format(i, avg_return))
            returns.append((steps, episode_return))
        time_taken = time.time() - start_time
        print("Evaluation Time: " + str(time_taken))
        del replay_buffer
        del dataset
        gc.collect()
        return returns


if __name__ == "__main__":
    Trainer().run(TrainingConfig())
