# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


class HeavyObstacle(Template):

    def template_name(self) -> str:
        return 'HeavyObstacle'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        vertical_bar = b2BodyDef(position=(0, 20),
                                 shapes=b2PolygonShape(box=(0.5, 10.0)),
                                 type=b2_staticBody)
        step_left = b2BodyDef(position=(-9, 20),
                              shapes=b2PolygonShape(box=(1.0, 0.5)),
                              type=b2_staticBody)
        step = b2BodyDef(position=(0, 20),
                         shapes=b2PolygonShape(box=(2.0, 0.5)),
                         type=b2_staticBody)
        step_right = b2BodyDef(position=(9, 20),
                               shapes=b2PolygonShape(box=(1.0, 0.5)),
                               type=b2_staticBody)
        return [vertical_bar, step_left, step, step_right]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        left_block = b2BodyDef(position=(-5.5, 25), angle=0,
                               fixtures=b2FixtureDef(shape=b2PolygonShape(box=(4.5, 3.0 - variant * 2.0)),
                                                     density=self.object_density,
                                                     friction=self.object_friction,
                                                     restitution=self.object_restitution),
                               type=b2_dynamicBody)

        right_block = b2BodyDef(position=(5.5, 25), angle=0,
                                fixtures=b2FixtureDef(shape=b2PolygonShape(box=(4.5, 1.0 + variant * 2.0)),
                                                      density=self.object_density,
                                                      friction=self.object_friction,
                                                      restitution=self.object_restitution),
                                type=b2_dynamicBody)
        return [left_block, right_block]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        return []
