# Template stuff:
from typing import List

# Box2D stuff:
from Box2D import *

from BMTemplate import Template


# The Shield Template
class Escape(Template):

    def template_name(self) -> str:
        return 'Escape'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:        
        roof = b2BodyDef(   position=(0, 15),
                            fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(5, 1)),
                                                    density=self.object_density,
                                                    friction=self.object_friction,
                                                    restitution=self.object_restitution),
                            type=b2_staticBody )

        return [roof]

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:

        # 2 boxes, a ball, and a plank:
        tool = b2BodyDef(   position=(6 * (variant - 0.5), 7 - 7 * (variant - 0.5)**2),
                            fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(1, 2)),
                                                    density=self.object_density,
                                                    friction=self.object_friction,
                                                    restitution=self.object_restitution),
                            angle = variant * 2, 
                            type=b2_dynamicBody )

        return [tool]

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        # 2 boxes, a ball, and a plank:

        danger_wall_left = b2BodyDef(   position=(-6, 8),
                                        fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(1, 8)),
                                                                density=self.object_density,
                                                                friction=self.object_friction,
                                                                restitution=self.object_restitution),
                                        type=b2_dynamicBody )
        
        danger_wall_right = b2BodyDef(  position=(6, 8),
                                        fixtures=b2FixtureDef(  shape=b2PolygonShape(box=(1, 8)),
                                                                density=self.object_density,
                                                                friction=self.object_friction,
                                                                restitution=self.object_restitution),
                                        type=b2_dynamicBody )
            
        return [danger_wall_left, danger_wall_right]
