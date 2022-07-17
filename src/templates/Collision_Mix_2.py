# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# Can produce many variantion by changing the shape (circle or rectangle)
class CollisionMix2(Template):
    def template_name(self) -> str:
        return "CollisionMix2"

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        ramp = b2BodyDef(position=(-6, 17),
                         shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (12, 0), (12, 1)]),
                         type=b2_staticBody)
        ramp_left_holder = b2BodyDef(position=(-7, 12),
                                     shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (1, 0), (1, 1)]),
                                     type=b2_staticBody)
        ramp_right_holder = b2BodyDef(position=(5, 8),
                                      shapes=b2PolygonShape(vertices=[(0, 1.0), (0, 0), (1, 0), (1, 1)]),
                                      type=b2_staticBody)
        return [ramp, ramp_left_holder, ramp_right_holder]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        blue_stick_left = b2BodyDef(position=(-8, 16), angle=0,
                                    fixtures=b2FixtureDef(shape=b2PolygonShape(box=(3, 1)),
                                                          density=self.object_density / 50,
                                                          friction=self.object_friction,
                                                          restitution=self.object_restitution),
                                    type=b2_dynamicBody)
        blue_ball_right = b2BodyDef(position=(5, 13), angle=0,
                                    fixtures=b2FixtureDef(shape=b2CircleShape(radius=2),
                                                          density=self.object_density / 50,
                                                          friction=self.object_friction,
                                                          restitution=self.object_restitution),
                                    type=b2_dynamicBody)
        return [blue_stick_left, blue_ball_right]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        red_ball_left_small = b2BodyDef(position=(8.5, 26), angle=0,
                                        fixtures=b2FixtureDef(shape=b2CircleShape(radius=1.8),
                                                              density=self.object_density / 50,
                                                              friction=10,
                                                              restitution=self.object_restitution),
                                        type=b2_dynamicBody)
        red_ball_left = b2BodyDef(position=(-8, 21), angle=0,
                                  fixtures=b2FixtureDef(shape=b2CircleShape(radius=2.2),
                                                        density=self.object_density / 50,
                                                        friction=10,
                                                        restitution=self.object_restitution),
                                  type=b2_dynamicBody)
        red_ball_right_small = b2BodyDef(position=(-8.3, 24), angle=0,
                                         fixtures=b2FixtureDef(shape=b2CircleShape(radius=1.6),
                                                               density=self.object_density / 50,
                                                               friction=10,
                                                               restitution=self.object_restitution),
                                         type=b2_dynamicBody)
        red_ball_right = b2BodyDef(position=(7, 21), angle=0,
                                   fixtures=b2FixtureDef(shape=b2CircleShape(radius=3),
                                                         density=self.object_density / 50,
                                                         friction=10,
                                                         restitution=self.object_restitution),
                                   type=b2_dynamicBody)
        return [red_ball_left, red_ball_right, red_ball_left_small, red_ball_right_small]
