import argparse


class TrainingConfig:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Run benchmark application with parameters')
        parser.add_argument('a', metavar='agent_name', type=str,
                            help='the name of the agent for training & testing')
        parser.add_argument('--t', metavar='template_name_list', type=str, default='',
                            help='optional: list of template name split by ","; will use all templates if not given')
        parser.add_argument('--lv', metavar='lower_variant_range', type=float, default=0.0,
                            help='optional: lower bound of variant number [0.0, 1.0]; will use 0.0 if not specified')
        parser.add_argument('--uv', metavar='upper_variant_range', type=float, default=1.0,
                            help='optional: upper bound of variant number [0.0, 1.0]; will use 1.0 if not specified')
        parser.add_argument('--d', metavar="max_step_depth", type=int, default=1000,
                            help='optional: max step depth for one iteration; default=1000')
        parser.add_argument('--i', metavar="iteration_num", type=int, default=5000,
                            help='optional: number of training iteration; default=5000')
        parser.add_argument('--e', metavar="evaluation_num", type=int, default=10,
                            help='optional: number of evaluation iteration; default=10')
        parser.add_argument('--r', metavar='reward_function_name', type=str, default='zero',
                            help='optional: the name of the reward function in training phase, '
                                 'will use zero if not specified')
        parser.add_argument('--er', metavar='reward_function_name', type=str, default='zero',
                            help='optional: the name of the reward function in evaluation phase, '
                                 'will use zero if not specified')
        parser.add_argument('--video', metavar="video_flag", type=bool, default=False,
                            help='optional: export all evaluation video or not, default false')
        args = parser.parse_args()
        self.agent_name: str = args.a
        self.temp_name_list: str = args.t
        self.lower_variant: float = args.lv
        self.upper_variant: float = args.uv
        self.max_depth: int = args.d
        self.train_iteration: int = args.i
        self.eval_iteration: int = args.e
        self.train_reward_func_name: str = args.r
        self.eval_reward_func_name: str = args.er
        self.export_video: bool = args.video
