# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


class Pinball(Template):
    def template_name(self) -> str:
        return "Pinball"

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        objects = []
        for i in range(0, 6):
            objects.append(b2BodyDef(position=(-10 + i * 4, 30),
                                     shapes=b2CircleShape(radius=0.7),
                                     type=b2_staticBody))
        for i in range(0, 5):
            objects.append(b2BodyDef(position=(-8 + i * 4, 25),
                                     shapes=b2CircleShape(radius=0.7),
                                     type=b2_staticBody))
        for i in range(0, 6):
            objects.append(b2BodyDef(position=(-10 + i * 4, 20),
                                     shapes=b2CircleShape(radius=0.7),
                                     type=b2_staticBody))
        for i in range(0, 5):
            objects.append(b2BodyDef(position=(-8 + i * 4, 15),
                                     shapes=b2CircleShape(radius=0.7),
                                     type=b2_staticBody))
        return objects

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        return []

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        objects = []
        for i in range(0, 6):
            objects.append(b2BodyDef(position=(-8 + (variant - 0.5) + i * 3, 37), angle=0,
                                     fixtures=b2FixtureDef(shape=b2CircleShape(radius=0.9),
                                                           density=self.object_density,
                                                           friction=self.object_friction,
                                                           restitution=self.object_restitution),
                                     type=b2_dynamicBody))
        return objects
