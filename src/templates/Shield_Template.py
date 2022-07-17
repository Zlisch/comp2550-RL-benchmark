# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The Shield Template
class Shield(Template):

    def template_name(self) -> str:
        return 'Shield'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:        
        return []

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:

        # 2 boxes, a ball, and a plank:
        safe_shield = b2BodyDef(position=(12 * (variant - 0.5), 26 - (3 * (variant - 0.5)**2)),
                                fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(4, 0.5)),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                type=b2_dynamicBody )


        return [safe_shield]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        # 2 boxes, a ball, and a plank:

        danger_ball_1 = b2BodyDef(  position=(-8.4, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody )
        danger_ball_2 = b2BodyDef(  position=(-6.3, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody )

        danger_ball_3 = b2BodyDef(  position=(-4.2, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody )     

        danger_ball_4 = b2BodyDef(  position=(-2.1, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody ) 

        danger_ball_5 = b2BodyDef(  position=(0.0, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody )
        danger_ball_6 = b2BodyDef(  position=(2.1, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody ) 

        danger_ball_7 = b2BodyDef(  position=(4.2, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody ) 

        danger_ball_8 = b2BodyDef(  position=(6.3, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody ) 

        danger_ball_9 = b2BodyDef(  position=(8.4, 34),
                                    fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.0),
                                                            density=self.object_density,
                                                            friction=self.object_friction,
                                                            restitution=self.object_restitution),
                                    type=b2_dynamicBody ) 

            
        return [danger_ball_1, danger_ball_2, danger_ball_3, danger_ball_4, danger_ball_5, danger_ball_6,
                danger_ball_7, danger_ball_8, danger_ball_9]
