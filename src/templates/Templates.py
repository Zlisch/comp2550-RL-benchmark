"""
Submit template here when it is created
"""
from typing import List

from BMTemplate import Template
from templates.Heavy_Obstacle_Template import HeavyObstacle
from templates.Pinball_Template import Pinball
from templates.PureAvoidance_Template import PureAvoidance
from templates.Roof_Template import Roof
from templates.Seesaw_Template import Seesaw
from templates.Falling_Ball_Template import FallingBall
from templates.Tower_Template import Tower
from templates.SeesawTunnel_Template import SeesawTunnel
from templates.Friction_Balance_Blue import FrictionBalanceBlue
from templates.Friction_Balance_2 import FrictionBalance2
from templates.Friction_Balance_Ball import FrictionBalanceBall
from templates.Collision_Ball_1 import CollisionBall1
from templates.Collision_Ball_2 import CollisionBall2
from templates.Collision_Mix_1 import CollisionMix1
from templates.Collision_Mix_2 import CollisionMix2
from templates.Shield_Template import Shield
from templates.Escape_Template import Escape
from templates.Blank_Template import Blank


def register_template(template: Template):
    """register a template"""
    REGISTRY[template.template_name().lower()] = template


def get_template_by_name(template_name: str) -> Template:
    """get template instance by name and ignoring case"""
    return REGISTRY[template_name.lower()]


def get_all_templates() -> List[Template]:
    """get list of all available templates excluding blank template"""
    return [t for t in REGISTRY.values() if t.template_name() != 'Blank']

# available templates
REGISTRY = dict()
# Adds all templates here
register_template(Roof())
register_template(Seesaw())
register_template(Tower())
register_template(SeesawTunnel())
register_template(FrictionBalanceBlue())
register_template(FrictionBalance2())
register_template(Blank())
register_template(FrictionBalanceBall())
register_template(CollisionBall1())
register_template(CollisionBall2())
register_template(CollisionMix1())
register_template(CollisionMix2())
register_template(PureAvoidance())
register_template(HeavyObstacle())
register_template(FallingBall())
register_template(Pinball())
register_template(Shield())
register_template(Escape())
