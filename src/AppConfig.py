import argparse


class Config:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Run benchmark application with parameters')
        parser.add_argument('t', metavar='template_name', type=str,
                            help='the name of the template [roof/seesaw...]')
        parser.add_argument('--v', metavar='variant', type=float, default=0.0,
                            help='optional: variant number of the task [0.0, 1.0]; will use 0.0 if not specified')
        parser.add_argument('--a', metavar='agent_name', type=str, default='human',
                            help='optional: the name of the agent, will use human agent if not specified')
        parser.add_argument('--r', metavar='reward_function_name', type=str, default='zero',
                            help='optional: the name of the reward function, will use zero if not specified')
        parser.add_argument('--render-image', action="store_true", default=False,
                            help='optional: default to false. If used, images of current episode will be rendered into '
                                 'the specified path')
        parser.add_argument('--render-path', metavar='render_path', nargs='?', type=str,
                            default='../assets/images/rendered/',
                            help='optional: default to \'../assets/images/rendered/\'. '
                                 'A folder containing rendered images '
                                 'will be generated in the specified path.')
        args = parser.parse_args()
        self.agent_name: str = args.a
        self.temp_name: str = args.t
        self.variant: float = args.v
        self.reward_func_name: str = args.r
        self.render_image: bool = args.render_image
        self.render_path: str = args.render_path
