# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The Friction_Balance_Blue Template
class FrictionBalanceBlue(Template):

    def template_name(self) -> str:
        return 'FrictionBalanceBlue'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        # Ramps
        ramp_long = b2BodyDef(position=(-4, 33),
                              shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (14, 0), (14, 1)]),
                              type=b2_staticBody)
        ramp_short = b2BodyDef(position=(-10, 26),
                               shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (5, 0), (5, 1)]),
                               type=b2_staticBody)
        ramp_support = b2BodyDef(position=(-0.5, 11),
                                 shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (1, 0), (1, 1)]),
                                 type=b2_staticBody)
        return [ramp_long, ramp_short, ramp_support]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        # Need physics reasoning for more reasonable parameters
        blue_left = b2BodyDef(position=(7, 22), angle=0,
                              fixtures=b2FixtureDef(shape=b2PolygonShape(box=(4, 2.2)),
                                                    density=self.object_density / 50,
                                                    friction=10,
                                                    restitution=self.object_restitution),
                              type=b2_dynamicBody)

        blue_right = b2BodyDef(position=(-6, 22), angle=0,
                               fixtures=b2FixtureDef(shape=b2PolygonShape(box=(4, 2.2)),
                                                     density=self.object_density / 50,
                                                     friction=10,
                                                     restitution=self.object_restitution),
                               type=b2_dynamicBody)
        blue_stick = b2BodyDef(position=(0, 22), angle=0,
                               fixtures=b2FixtureDef(shape=b2PolygonShape(box=(2, 7)),
                                                     density=self.object_density / 50,
                                                     friction=10,
                                                     restitution=self.object_restitution),
                               type=b2_dynamicBody)
        return [blue_left, blue_right, blue_stick]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        red_ball = b2BodyDef(position=(0, 31), angle=0,
                             fixtures=b2FixtureDef(shape=b2CircleShape(radius=2),
                                                   density=self.object_density / 5,
                                                   friction=10,
                                                   restitution=self.object_restitution),
                             type=b2_dynamicBody)
        return [red_ball]
