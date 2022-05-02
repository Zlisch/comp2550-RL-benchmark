# Template stuff:
from BMTemplate import BMTemplate

# Box2D stuff:
from Box2D import *

# (For now) a demonstration on how to create a custom BMTemplate
# ! Do not forget to add the 'type' argument in each def !

# The Seesaw Template
class Seesaw(BMTemplate):        

    # Override to create a unique template:
    def createTemplate(self):

        print("")
        print("Creating Seesaw Template")
        print("")

        # Create object definitions which make up the template:
        # Pillar:        
        pillarDef = b2BodyDef(  position = (0, 10), 
                                shapes = b2PolygonShape(box=(1, 5)), 
                                type = b2_staticBody  )
        pillarTopDef = b2BodyDef(   position = (0, 15), 
                                    shapes = b2CircleShape(radius=1), 
                                    type = b2_staticBody  )        

        # Seesaw:
        balanceDef = b2BodyDef( position = (0, 17), 
                                fixtures = b2FixtureDef(    shape = b2PolygonShape(box = (7, 0.5)), 
                                                            density = 1.0,
                                                            friction = 0.5,
                                                            restitution = 0.3   ), 
                                type = b2_dynamicBody   )                           
        
        # Small Red Ball:
        redBallDef = b2BodyDef( position = (3, 20), 
                                fixtures = b2FixtureDef(    shape = b2CircleShape(radius=1), 
                                                            density = 1.0,
                                                            friction = 0.5,
                                                            restitution = 0.3   ), 
                                type = b2_dynamicBody)
        
        # Big Red Box:
        redBoxDef = b2BodyDef(  position = (-4, 20), 
                                fixtures = b2FixtureDef(    shape = b2PolygonShape(box=(2.5, 1.5)),
                                                            density = 1.0,
                                                            friction = 0.5,
                                                            restitution = 0.3   ), 
                                type = b2_dynamicBody)

        # Add these definitions to the relevant lists:
        # Add statics:
        self.staticDefs.append(pillarDef)
        self.staticDefs.append(pillarTopDef)

        # Add dynamic blues:
        self.dynamicBlueDefs.append(balanceDef)

        # Add dynamic reds:
        self.dynamicRedDefs.append(redBallDef)
        self.dynamicRedDefs.append(redBoxDef)

    