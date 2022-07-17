# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The Tower Template
class Tower(Template):

    def template_name(self) -> str:
        return 'Tower'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        return []

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        # Seesaw:
        # A box around the agent:                
        left_wall_1 = b2BodyDef(position=(-2, 7),
                                fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 7)),
                                                      density=self.object_density,
                                                      friction=self.object_friction,
                                                      restitution=self.object_restitution),
                                type=b2_dynamicBody)
        right_wall_1 = b2BodyDef(position=(2, 7),
                                 fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 7)),
                                                       density=self.object_density,
                                                       friction=self.object_friction,
                                                       restitution=self.object_restitution),
                                 type=b2_dynamicBody)

        left_wall_2 = b2BodyDef(position=(-3, 17),
                                fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 2)),
                                                      density=self.object_density,
                                                      friction=self.object_friction,
                                                      restitution=self.object_restitution),
                                type=b2_dynamicBody)
        right_wall_2 = b2BodyDef(position=(3, 17),
                                 fixtures=b2FixtureDef(shape=b2PolygonShape(box=(0.5, 2)),
                                                       density=self.object_density,
                                                       friction=self.object_friction,
                                                       restitution=self.object_restitution),
                                 type=b2_dynamicBody)

        return [left_wall_1, right_wall_1, left_wall_2, right_wall_2]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        # Red Slat 1:
        slat_1 = b2BodyDef(position=(-2 * variant, 14.5),
                           fixtures=b2FixtureDef(shape=b2PolygonShape(box=(4, 0.5)),
                                                 density=self.object_density,
                                                 friction=self.object_friction,
                                                 restitution=self.object_restitution),
                           type=b2_dynamicBody)

        slat_2 = b2BodyDef(position=(2 * variant, 20),
                           fixtures=b2FixtureDef(shape=b2PolygonShape(box=(4, 0.5)),
                                                 density=self.object_density,
                                                 friction=self.object_friction,
                                                 restitution=self.object_restitution),
                           type=b2_dynamicBody)

        # Extra ball because I am feeling reckless:
        red_ball = b2BodyDef(position=(0, 17),
                             linearVelocity=((variant - 0.5) * 15, 1 + 3 * variant),
                             fixtures=b2FixtureDef(shape=b2CircleShape(radius=1 + variant),
                                                   density=self.object_density,
                                                   friction=self.object_friction,
                                                   restitution=self.object_restitution),
                             type=b2_dynamicBody)

        return [slat_1, slat_2, red_ball]
