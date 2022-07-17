# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The Seesaw Template
class Seesaw(Template):

    def template_name(self) -> str:
        return 'Seesaw'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        # Pillar:
        pillar_def = b2BodyDef(position=((variant - 0.5) * 3, 20),
                               shapes=b2PolygonShape(vertices=[(-1, 5), (1, 5), (5, -5), (-5, -5)]),
                               type=b2_staticBody)
        pillar_top_def = b2BodyDef(position=((variant - 0.5) * 3, 25),
                                   shapes=b2CircleShape(radius=1),
                                   type=b2_staticBody)
        return [pillar_def, pillar_top_def]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        # Seesaw:
        balance_def = b2BodyDef(position=(0, 27),
                                fixtures=b2FixtureDef(shape=b2PolygonShape(box=(7, 0.5)),
                                                      density=self.object_density,
                                                      friction=self.object_friction,
                                                      restitution=self.object_restitution),
                                type=b2_dynamicBody)
        return [balance_def]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        # Red Ball:
        red_ball_def = b2BodyDef(position=(3, 30),
                                 linearVelocity=(-variant, variant),
                                 fixtures=b2FixtureDef(shape=b2CircleShape(radius=2 - variant),
                                                       density=self.object_density,
                                                       friction=self.object_friction,
                                                       restitution=self.object_restitution),
                                 type=b2_dynamicBody)
        # Big Red Box:
        red_box_def = b2BodyDef(position=(-4, 30),
                                linearVelocity=(2 * variant, 2 * variant),
                                fixtures=b2FixtureDef(shape=b2PolygonShape(box=(2.0 + variant, 1.5)),
                                                      density=self.object_density,
                                                      friction=self.object_friction,
                                                      restitution=self.object_restitution),
                                type=b2_dynamicBody)
        return [red_ball_def, red_box_def]
