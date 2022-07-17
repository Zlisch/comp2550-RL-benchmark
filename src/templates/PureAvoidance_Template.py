# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The Roof Template
class PureAvoidance(Template):

    def template_name(self) -> str:
        return 'PureAvoidance'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        
        static_box_1 = b2BodyDef(   position=(-7 + (15 * variant), 13),
                                    shapes=b2PolygonShape(box=(3, 1)),                                    
                                    angle = variant + 0.3,
                                    type=b2_staticBody)

        static_box_2 = b2BodyDef(   position=(7 - (14 * variant), 9),
                                    shapes=b2PolygonShape(box=(1, 1)),                                    
                                    angle = variant - 0.3,
                                    type=b2_staticBody)

        static_ball = b2BodyDef(   position=(-3, 24),
                                    shapes=b2CircleShape(radius=0.7),                                                                        
                                    type=b2_staticBody)
        
        return [static_box_1, static_box_2, static_ball]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:

        # 2 boxes, a ball, and a plank:

        safe_box_1 = b2BodyDef( position=(-5 + (3 * variant), 20 + (3 * variant)),
                                fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(1.5, 2)),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                linearVelocity=(-4, (variant - 0.3) * 8),    
                                angularVelocity= (variant - 0.4) * 3,
                                type=b2_dynamicBody )
        
        safe_box_2 = b2BodyDef( position=(-5 - (3 * variant), 30 - (3 * variant)),
                                fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(2, 2)),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                linearVelocity=(4, (variant) * 5),   
                                angularVelocity= (variant - 0.8) * 3,                            
                                type=b2_dynamicBody )

        safe_ball = b2BodyDef(  position=(2 + (3 * variant), 27 + (3 * variant)),
                                fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.5),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                linearVelocity=(-4, (variant - 0.5) * 3),                                   
                                type=b2_dynamicBody )

        safe_plank = b2BodyDef( position=(2 + (3 * variant), 33 - (3 * variant)),
                                fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(4, 1)),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                linearVelocity=(4, (variant) * 3),   
                                angularVelocity= (variant - 0.1) * 3,                            
                                type=b2_dynamicBody )


        return [safe_box_1, safe_box_2, safe_ball, safe_plank]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        # 2 boxes, a ball, and a plank:

        danger_box_1 = b2BodyDef( position=(-3 + (3 * variant), 35 + (3 * variant)),
                                fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(3, 1)),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                linearVelocity=(4, (variant - 0.3) * 8),    
                                angularVelocity= (variant - 0.9) * 7,
                                type=b2_dynamicBody )
        
        danger_box_2 = b2BodyDef( position=(-3 + (8 * variant), 30 - (3 * variant)),
                                fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(2, 1)),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                linearVelocity=(-4, (variant) * 5),   
                                angularVelocity= (variant - 0.2) * 9,                            
                                type=b2_dynamicBody )

        danger_ball = b2BodyDef(  position=(2 - (3 * variant), 18 - (3 * variant)),
                                fixtures=b2FixtureDef(  shape=b2CircleShape(radius=1.5),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),
                                linearVelocity=(8 * (variant - 0.5), (variant - 0.1) * 15),                                   
                                type=b2_dynamicBody )

        danger_plank = b2BodyDef( position=(-5, 15),
                                fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(3, 0.8)),
                                                        density=self.object_density,
                                                        friction=self.object_friction,
                                                        restitution=self.object_restitution),                                   
                                angularVelocity= (variant - 0.5) * 8,                            
                                type=b2_dynamicBody )
        
        return [danger_box_1, danger_box_2, danger_ball, danger_plank]
