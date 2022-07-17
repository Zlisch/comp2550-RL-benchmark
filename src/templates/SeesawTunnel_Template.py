# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The SeesawTunnel Template
class SeesawTunnel(Template):

    def template_name(self) -> str:
        return 'SeesawTunnel'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        # Pillar:
        pillar_def_1 = b2BodyDef(position=((variant - 0.5) * 7 - 2, 10),
                                 shapes=b2PolygonShape(vertices=[(-1, 5), (1, 5), (1, -5), (-1, -5)]),
                                 type=b2_staticBody)
        pillar_top_def_1 = b2BodyDef(position=((variant - 0.5) * 7 - 2, 15),
                                     shapes=b2CircleShape(radius=1),
                                     type=b2_staticBody)

        pillar_def_2 = b2BodyDef(position=((variant - 0.5) * 6 + 2, 10),
                                 shapes=b2PolygonShape(vertices=[(-1, 5), (1, 5), (1, -5), (-1, -5)]),
                                 type=b2_staticBody)
        pillar_top_def_2 = b2BodyDef(position=((variant - 0.5) * 6 + 2, 15),
                                     shapes=b2CircleShape(radius=1),
                                     type=b2_staticBody)

        return [pillar_def_1, pillar_top_def_1, pillar_def_2, pillar_top_def_2]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        # Seesaw:
        balance_def = b2BodyDef(position=(0, 17),
                                fixtures=b2FixtureDef(shape=b2PolygonShape(box=(8, 0.5)),
                                                      density=self.object_density,
                                                      friction=self.object_friction,
                                                      restitution=self.object_restitution),
                                type=b2_dynamicBody)
        return [balance_def]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        # Red Ball:
        red_ball_def = b2BodyDef(position=(3, 25),
                                 linearVelocity=(-variant * 2, variant * 3),
                                 fixtures=b2FixtureDef(shape=b2CircleShape(radius=2 + variant),
                                                       density=self.object_density,
                                                       friction=self.object_friction,
                                                       restitution=self.object_restitution),
                                 type=b2_dynamicBody)

        return [red_ball_def]
