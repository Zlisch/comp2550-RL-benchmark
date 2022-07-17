import pygame
import pygame.gfxdraw
from tf_agents.environments import tf_py_environment

from AppConfig import Config
from BMTask import State
from agents.MCSAgent import MCSAgent
from agents.TrainableAgent import TrainableAgent
from rendering.ImageSaver import ImageSaver
from agents import Agents
from agents.Agent import Agent
from rendering import RenderEngine
from rewards import RewardFunctions
from rewards.BMRewardFunction import RewardFunction
from templates import Templates
from training.TensorFlowEnvironment import Sandbox


class Application:
    """ 
    The new application entry for starting the RL playground.
    """
    # basic configuration of the screen
    MAX_FPS = 60
    SCR_WIDTH, SCR_HEIGHT = 800, 600

    def __init__(self):
        # init pygame for the application
        pygame.init()
        # font render of the pygame
        # Note (Lachlan): '../assets/arial.ttf' does not work for me, I run from 2500-rl-benchmark
        try:
            self.font = pygame.font.Font('../assets/arial.ttf', 20)
        except FileNotFoundError:
            self.font = pygame.font.Font('assets/arial.ttf', 20)
        # initialize pygame parameters
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((Application.SCR_WIDTH, Application.SCR_HEIGHT))
        # create image renderer
        self.image_saver = ImageSaver()
        # declare fields
        self.template = None
        self.variant = 0

    def run(self, config: Config):
        """run the application from the given args"""
        agent = Agents.get_agent_by_name(config.agent_name)
        self.template = Templates.get_template_by_name(config.temp_name)
        self.variant = config.variant
        reward_func = RewardFunctions.get_reward_function_by_name(config.reward_func_name)
        # give access to reward function to MCS agent
        if isinstance(agent, MCSAgent):
            agent.set_reward_func(reward_func)
        # set up image renderer to render frames of current template
        self.image_saver.init(config.render_image, config.render_path, self.template.template_name())
        # setup the world
        pygame.display.set_caption(self.template.template_name() + " [" + str(config.variant) + "]")
        world = self.template.create_world(self.variant)
        self.loop(world, agent, reward_func)

    def loop(self, state: State, agent: Agent, reward_func: RewardFunction):
        """
        Main application loop function
        """
        total_reward = 0
        agent.reset()
        if isinstance(agent, TrainableAgent):
            train_py_env = Sandbox(1,
                                   template=self.template,
                                   variant_range=(self.variant, self.variant),
                                   reward_function=reward_func,
                                   observation=agent.get_observation(),
                                   discount_factor=0.95)
            train_env = tf_py_environment.TFPyEnvironment(train_py_env)
            agent.train(0.5e3, train_env.time_step_spec())
        # Render loop:
        while True:
            # Handle quit event
            for _ in pygame.event.get(eventtype=pygame.QUIT):
                quit()
            # Take action from the agent
            action = agent.take_action(state)
            # progress the simulation if action is valid
            if action is not None:
                # Apply action & step simulation
                state.apply_action(action)
                # The reward of the action
                reward = reward_func.compute(state)
                agent.update_reward(reward)
                # update reward
                total_reward = total_reward + reward
            # Tick clock:
            self.clock.tick(Application.MAX_FPS)
            # Render the world to the surface:
            self.render(state, total_reward)
            # Save current frame using the image saver; only do this if action is valid
            if action is not None:
                self.image_saver.save(self.screen, self.MAX_FPS)

    def render(self, state: State, total_reward: float):
        """
        Render all elements in the game into the screen with total reward
        """
        # let render engine to render basic stuff
        RenderEngine.render_state(self.screen, state)
        # Render reward value:
        text_shape = self.font.render('Total Reward: ' + str(total_reward), False, (0, 0, 0))
        self.screen.blit(text_shape, (0, 0))
        # Update the display:
        pygame.display.flip()
        pygame.display.update()


if __name__ == "__main__":
    Application().run(Config())
