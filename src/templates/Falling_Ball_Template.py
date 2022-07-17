# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


class FallingBall(Template):

    def template_name(self) -> str:
        return 'FallingBall'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        vertical_bar_l = b2BodyDef(position=(-3, 8),
                                   shapes=b2PolygonShape(box=(0.5, 8.0)),
                                   type=b2_staticBody)
        vertical_bar_m = b2BodyDef(position=(0, 9),
                                   shapes=b2PolygonShape(box=(0.5, 7.0)),
                                   type=b2_staticBody)
        vertical_bar_r = b2BodyDef(position=(3, 8),
                                   shapes=b2PolygonShape(box=(0.5, 8.0)),
                                   type=b2_staticBody)
        step_bar = b2BodyDef(position=(-4.5, 20),
                             shapes=b2PolygonShape(box=(0.5, 0.5)),
                             type=b2_staticBody)
        return [vertical_bar_l, vertical_bar_m, vertical_bar_r, step_bar]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        return [b2BodyDef(position=(6, 30), angle=0,
                          fixtures=b2FixtureDef(shape=b2CircleShape(radius=3.2 + variant / 2),
                                                density=self.object_density,
                                                friction=self.object_friction,
                                                restitution=self.object_restitution),
                          type=b2_dynamicBody)]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        return [b2BodyDef(position=(1.5, 19), angle=0,
                          fixtures=b2FixtureDef(shape=b2CircleShape(radius=2.7),
                                                density=self.object_density,
                                                friction=self.object_friction,
                                                restitution=self.object_restitution),
                          type=b2_dynamicBody)]
