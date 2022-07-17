from agents.Agent import Agent
from agents.DummyAgent import DummyAgent
from agents.HumanAgent import HumanAgent
from agents.ImageDQNAgent import ImageDQNAgent
from agents.HeuristicAvoidAgent import HeuristicAvoidAgent
from agents.HeuristicPushAgent import HeuristicPushAgent
from agents.DistributionAgent import DistributionAgent


def register_agent(agent: Agent):
    """register an agent"""
    REGISTRY[agent.agent_name().lower()] = agent


def get_agent_by_name(agent_name: str) -> Agent:
    """get agent instance by name and ignoring case"""
    return REGISTRY[agent_name.lower()]


# available agents (model)
REGISTRY = dict()
# register new agents here
register_agent(HumanAgent())
register_agent(DummyAgent())
register_agent(ImageDQNAgent())
register_agent(HeuristicAvoidAgent())
register_agent(HeuristicPushAgent())
register_agent(DistributionAgent([0.3, 0.4, 0.3, 0.1, 0, 0.1, 0, 0, 0]))