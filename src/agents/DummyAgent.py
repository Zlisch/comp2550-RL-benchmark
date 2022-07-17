from numpy import ndarray
from tf_agents.agents import TFAgent
from tf_agents.trajectories import time_step as ts

from Action import Action
from agents.HumanAgent import HumanAgent
from agents.ImageBasedAgent import ImageBasedAgent


class DummyAgent(ImageBasedAgent):
    def get_model(self) -> TFAgent:
        pass

    def train(self, learning_rate: float, time_step_spec: ts.TimeStep):
        pass

    def __init__(self):
        super().__init__()
        self.human = HumanAgent()

    def take_action_from_image(self, image: ndarray) -> Action:
        print(image)
        return self.human.take_action(None)

    def agent_name(self) -> str:
        return "Dummy"

    def update_reward(self, reward: float):
        pass
