# Abstract class stuff:
import abc 
from abc import ABC, abstractmethod
from typing import Any, List

# Box2D stuff:
# from Box2D import (b2PolygonShape, b2World, b2FixtureDef, b2CircleShape, b2_staticBody, b2_dynamicBody, b2_kinematicBody, b2Body, b2Vec2, b2Fixture, b2BodyDef)
from Box2D.Box2D import *

class BMTemplate(ABC):    

    # World is enclosed into a [-10. 10] x [0, 40] box bounded by these walls:
    wallDefs =  [   b2BodyDef(position = (0, -1), shapes = b2PolygonShape(box=(10, 1)), type = b2_staticBody), 
                    b2BodyDef(position = (-11, 20), shapes = b2PolygonShape(box=(1, 22)), type = b2_staticBody), 
                    b2BodyDef(position = (11, 20), shapes = b2PolygonShape(box=(1, 22)), type = b2_staticBody), 
                    b2BodyDef(position = (0, 41), shapes = b2PolygonShape(box=(10, 1)), type = b2_staticBody)  ]

    # Agent properties, included here just for code structure:
    agentDef = b2BodyDef(   position = (0, 3), 
                            fixtures = b2FixtureDef(    shape=b2CircleShape(radius=0.5),                                                                            
                                                        friction=0.5,
                                                        restitution=0.3,
                                                        density=3.0 ),                                                 
                            linearVelocity = (0, 0),
                            type = b2_dynamicBody )

    # Define the components of a template:
    def __init__(self):

        self.bodyDefs: List[b2BodyDef]
         
        self.world = b2World(gravity=(0, -10), doSleep=True)

        # Declare statics and dynamics:
        self.statics: List[b2_staticBody]
        self.dynamicBlues: List[b2_dynamicBody]
        self.dynamicReds: List[b2_dynamicBody]
        self.agent: b2_dynamicBody

        # Declare staticDefs and dynamicDefs:
        self.staticDefs: List[b2BodyDef]
        self.dynamicBlueDefs: List[b2BodyDef]
        self.dynamicRedDefs: List[b2BodyDef]                

        # Instantiate empty lists:
        self.statics = []
        self.dynamicBlues = []
        self.dynamicReds = []
        self.staticDefs = []
        self.dynamicBlueDefs = []
        self.dynamicRedDefs = []

        # Environment Constants:
        # Add walls to static defs        
        for d in BMTemplate.wallDefs:
            self.staticDefs.append(d)

        # The agent is also a constant, but this is done elsewhere                    

        self.createTemplate()  # Call the unique template's overrided create method
                
    # Where each template will override and add its own 
    # dynamic / static bodies to the list of bodyDefs.
    # It is important that every bodyDef which is added 
    # to the '...Defs' lists is given a 'type' argument
    @abstractmethod
    def createTemplate(self):
        pass

    """ The next thing to do might be to add an abstract method for 
        slightly perturbing the original template so we can have a set 
        for each, like in PHYRE """

    # Creates a new b2World based on the template
    def createWorld(self) -> b2World:
        # Do world instantiation things:
        self.world = b2World(gravity=(0, -10), doSleep=True)

        # Add bodies:
        self.world = self.addToWorld(self.world)

        return self.world
        
    # Adds the bodies in this template to an existing b2World
    def addToWorld(self, world: b2World) -> b2World:
        # Statics:
        for d in self.staticDefs:
            self.statics.append(world.CreateBody(d))

        # Dynamic Blues:
        for d in self.dynamicBlueDefs:
            self.dynamicBlues.append(world.CreateBody(d))

        # Dynamic Reds:
        for d in self.dynamicRedDefs:
            self.dynamicReds.append(world.CreateBody(d))
        
        # Agent:
        self.agent = world.CreateBody(self.agentDef)

        return world    
    
    # Query a position in the world for what is there:
    # Returns a one-hot vector representing the presence of objects:
    # (static, dynamicRed, dynamicBlue, agent)
    def queryPoint(self, point: b2Vec2):
        ret = (0, 0, 0, 0)
        
        # Statics:                
        for b in self.statics:   
            exitloop = False
            for f in b.fixtures:  
                if f.TestPoint(point):            
                    ret += (1, 0, 0, 0)
                    exitloop = True
                    break   # exit loop
            if exitloop: break
        
        # Dynamic Reds:        
        for b in self.dynamicReds:   
            exitloop = False
            for f in b.fixtures:  
                if f.TestPoint(point):            
                    ret += (0, 1, 0, 0)
                    exitloop = True
                    break   # exit loop
            if exitloop: break

        # Dynamic Blues:
        for b in self.dynamicBlues:   
            exitloop = False
            for f in b.fixtures:  
                if f.TestPoint(point):            
                    ret += (9, 0, 1, 0)
                    exitloop = True
                    break   # exit loop
            if exitloop: break

        # Agent:
        if self.agent.fixtures[0].TestPoint(point):
            ret += (0, 0, 0, 1)

        return ret

