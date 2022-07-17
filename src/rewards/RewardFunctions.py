from rewards.BMRewardFunction import RewardFunction
from rewards.EvaluateRewardFunction import EvaluateRewardFunction
from rewards.HeightReward import HeightAndDangerRewardFunction
from rewards.PenaltyReward import PenaltyRewardFunction
from rewards.ZeroReward import ZeroRewardFunction
from rewards.NewHeightReward import NewHeightReward


def register_reward_function(reward_function: RewardFunction):
    """register a reward function"""
    REGISTRY[reward_function.function_name().lower()] = reward_function


def get_reward_function_by_name(function_name: str) -> RewardFunction:
    """get reward function instance by name and ignoring case"""
    return REGISTRY[function_name.lower()]


# available reward functions
REGISTRY = dict()
# Adds all reward functions here
register_reward_function(ZeroRewardFunction())
register_reward_function(PenaltyRewardFunction())
register_reward_function(HeightAndDangerRewardFunction())
register_reward_function(EvaluateRewardFunction())
register_reward_function(NewHeightReward())
