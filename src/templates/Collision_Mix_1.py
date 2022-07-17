# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


class CollisionMix1(Template):
    def template_name(self) -> str:
        return "CollisionMix1"

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        ramp_left_short = b2BodyDef(position=(-10, 32),
                                    shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (6, 0), (6, 1)]),
                                    type=b2_staticBody)
        ramp_right_long = b2BodyDef(position=(0, 30),
                                    shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (10, 0), (10, 1)]),
                                    type=b2_staticBody)
        ramp_ball_holder = b2BodyDef(position=(-7, 16),
                                     shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (1, 0), (1, 1)]),
                                     type=b2_staticBody)
        ramp_stick_holder = b2BodyDef(position=(-1, 24),
                                      shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (1, 0), (1, 1)]),
                                      type=b2_staticBody)
        return [ramp_left_short, ramp_right_long, ramp_ball_holder, ramp_stick_holder]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        blue_ball = b2BodyDef(position=(-7, 20), angle=0,
                              fixtures=b2FixtureDef(shape=b2CircleShape(radius=3),
                                                    density=self.object_density / 100,
                                                    friction=self.object_friction,
                                                    restitution=self.object_restitution),
                              type=b2_dynamicBody)
        blue_stick = b2BodyDef(position=(-2, 25), angle=0,
                               fixtures=b2FixtureDef(shape=b2PolygonShape(box=(5, 1)),
                                                     density=self.object_density / 100,
                                                     friction=self.object_friction,
                                                     restitution=self.object_restitution),
                               type=b2_dynamicBody)
        return [blue_ball, blue_stick]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        red_ball = b2BodyDef(position=(-1.5, 34), angle=0,
                             fixtures=b2FixtureDef(shape=b2CircleShape(radius=2.5),
                                                   density=self.object_density / 50,
                                                   friction=10,
                                                   restitution=self.object_restitution),
                             type=b2_dynamicBody)
        return [red_ball]
