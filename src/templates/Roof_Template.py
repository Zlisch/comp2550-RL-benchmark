# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The Roof Template
class Roof(Template):

    def template_name(self) -> str:
        return 'Roof'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        # Ramps:
        ramp_left = b2BodyDef(position=(-10, 20 + (4 * (variant - 0.5))),
                              shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (8.0, -2.0), (8.0, -1.0)]),
                              type=b2_staticBody)
        ramp_right = b2BodyDef(position=(10, 20 - (4 * (variant - 0.5))),
                               shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (-8.0, -2.0), (-8.0, -1.0)]),
                               type=b2_staticBody)
        return [ramp_left, ramp_right]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        # Pillar:
        roof_left = b2BodyDef(position=(-2, 6), angle=-0.15,
                              fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 6)),
                                                    density=self.object_density,
                                                    friction=self.object_friction,
                                                    restitution=self.object_restitution),
                              type=b2_dynamicBody)

        roof_right = b2BodyDef(position=(2, 6), angle=0.15,
                               fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 6)),
                                                     density=self.object_density,
                                                     friction=self.object_friction,
                                                     restitution=self.object_restitution),
                               type=b2_dynamicBody)
        return [roof_left, roof_right]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        # Small Red Balls:
        red_ball_left = b2BodyDef(position=(-8, 33),
                                  linearVelocity=(variant * 2, variant * 3),
                                  fixtures=b2FixtureDef(shape=b2CircleShape(radius=1),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                  type=b2_dynamicBody)

        red_ball_right = b2BodyDef(position=(8, 29),
                                   linearVelocity=(-variant * 2 + 1, variant * 2),
                                   fixtures=b2FixtureDef(shape=b2CircleShape(radius=1),
                                                         density=self.object_density,
                                                         friction=self.object_friction,
                                                         restitution=self.object_restitution),
                                   type=b2_dynamicBody)
        return [red_ball_left, red_ball_right]
