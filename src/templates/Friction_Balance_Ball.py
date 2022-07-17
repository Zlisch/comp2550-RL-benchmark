# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


class FrictionBalanceBall(Template):
    def template_name(self) -> str:
        return "FrictionBalanceBall"

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        ramp_left = b2BodyDef(position=(-4, 17),
                              shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (1, 0), (1, 1)]),
                              type=b2_staticBody)
        ramp_right = b2BodyDef(position=(4, 17),
                               shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (1, 0), (1, 1)]),
                               type=b2_staticBody)
        return [ramp_left, ramp_right]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        blue_stick_left = b2BodyDef(position=(-5, 20), angle=0,
                                    fixtures=b2FixtureDef(shape=b2PolygonShape(box=(5, 1.0)),
                                                          density=self.object_density / 50,
                                                          friction=self.object_friction,
                                                          restitution=self.object_restitution),
                                    type=b2_dynamicBody)
        blue_stick_right = b2BodyDef(position=(5, 20), angle=0,
                                     fixtures=b2FixtureDef(shape=b2PolygonShape(box=(5, 1.0)),
                                                           density=self.object_density / 50,
                                                           friction=self.object_friction,
                                                           restitution=self.object_restitution),
                                     type=b2_dynamicBody)
        return [blue_stick_left, blue_stick_right]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        red_ball_big = b2BodyDef(position=(0, 27), angle=0,
                                 fixtures=b2FixtureDef(shape=b2CircleShape(radius=5),
                                                       density=self.object_density / 50,
                                                       friction=10,
                                                       restitution=self.object_restitution),
                                 type=b2_dynamicBody)
        red_ball_left = b2BodyDef(position=(-9, 24), angle=0,
                                  fixtures=b2FixtureDef(shape=b2CircleShape(radius=2.8),
                                                        density=self.object_density / 50,
                                                        friction=10,
                                                        restitution=self.object_restitution),
                                  type=b2_dynamicBody)
        red_ball_right = b2BodyDef(position=(6, 33), angle=0,
                                   fixtures=b2FixtureDef(shape=b2CircleShape(radius=3.5),
                                                         density=self.object_density / 50,
                                                         friction=10,
                                                         restitution=self.object_restitution),
                                   type=b2_dynamicBody)
        return [red_ball_big, red_ball_left, red_ball_right]
