# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The Friction_Balance_2 Template
class FrictionBalance2(Template):

    def template_name(self) -> str:
        return 'FrictionBalance2'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        # Ramps
        ramp = b2BodyDef(position=(-5, 15),
                         shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (2, 0), (2, 1)]),
                         type=b2_staticBody)
        return [ramp]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        # Need physics reasoning for working parameters
        blue_right = b2BodyDef(position=(6, 20), angle=0,
                               fixtures=b2FixtureDef(shape=b2PolygonShape(box=(3.4, 1)),
                                                     density=self.object_density / 10,
                                                     friction=100,
                                                     restitution=self.object_restitution),
                               type=b2_dynamicBody)

        blue_left = b2BodyDef(position=(-6, 20.15), angle=0,
                              fixtures=b2FixtureDef(shape=b2PolygonShape(box=(3.4, 1)),
                                                    density=self.object_density / 10,
                                                    friction=100,
                                                    restitution=self.object_restitution),
                              type=b2_dynamicBody)
        blue_stick = b2BodyDef(position=(0, 20), angle=0,
                               fixtures=b2FixtureDef(shape=b2PolygonShape(box=(3.7, 2)),
                                                     density=self.object_density / 40,
                                                     friction=100,
                                                     restitution=self.object_restitution),
                               type=b2_dynamicBody)
        return [blue_left, blue_right, blue_stick]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        # Small Red Ball:
        red_stick = b2BodyDef(position=(0, 22),
                              fixtures=b2FixtureDef(shape=b2PolygonShape(box=(3, 1)),
                                                    density=self.object_density,
                                                    friction=100,
                                                    restitution=self.object_restitution),
                              type=b2_dynamicBody)

        red_ball = b2BodyDef(position=(0, 25),
                             fixtures=b2FixtureDef(shape=b2CircleShape(radius=1.5),
                                                   density=self.object_density,
                                                   friction=100,
                                                   restitution=self.object_restitution),
                             type=b2_dynamicBody)
        return [red_stick, red_ball]
