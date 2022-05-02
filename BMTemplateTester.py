#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Template stuff:
from BMTemplate import BMTemplate
from Seesaw import Seesaw

# Pygame stuff:
import pygame
import pygame.gfxdraw
from pygame.locals import (QUIT, KEYDOWN, KEYUP)

# Box2D stuff:
from Box2D.Box2D import *    

# Human testing for Templates!
class BMTemplateTester:
    
    # Rendering Backend:
    # Screen center offset, zoom, width and height
    SCR_OFFSETX, SCR_OFFSETY = 0, 20
    SCR_ZOOM = 12
    SCR_WIDTH, SCR_HEIGHT = 800, 600

    # Box2D parameters:
    VEL_ITERS, POS_ITERS = 6, 2
    TIME_STEP = 1 / 80
    

    # Rendering Colours:
    RENDER_COLS = { 'static': (40, 40, 40),
                    'dynamicBlue': (20, 20, 180), 
                    'dynamicRed': (180, 20, 20), 
                    'agent': (80, 180, 20)  }

    def __init__(self, template: BMTemplate):

        pygame.init()
        pygame.display.set_caption("Template Test")

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((BMTemplateTester.SCR_WIDTH, BMTemplateTester.SCR_HEIGHT))
        
        self.template = template

        self.agentVel = b2Vec2(0.0, 0.0)
        
        self.world = self.template.createWorld()        
        
    # Driver:
    def run(self):

        # Render loop:
        while True:
            # Handle input and events
            # The fact that input is handled first means the agent can knock into things properly
            self.handleInput()

            # Step Simulation
            self.stepSim()
            
            # Draw Simulation:
            self.drawSim()
            

    def handleInput(self):        

        # Loop through events:
        for event in pygame.event.get():
            # Quit:
            if event.type == pygame.QUIT:
                quit()

            # Control agent:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.agentVel += (0, 6)
                if event.key == pygame.K_s:
                    self.agentVel += (0, -6)
                if event.key == pygame.K_a:
                    self.agentVel += (-6, 0)
                if event.key == pygame.K_d:
                    self.agentVel += (6, 0)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.agentVel -= (0, 6)
                if event.key == pygame.K_s:
                    self.agentVel -= (0, -6)
                if event.key == pygame.K_a:
                    self.agentVel -= (-6, 0)
                if event.key == pygame.K_d:
                    self.agentVel -= (6, 0)

        self.template.agent.linearVelocity = self.agentVel
        

    def stepSim(self):        
        # Tell Box2D to update the simulation
        self.world.Step(    BMTemplateTester.TIME_STEP, 
                            BMTemplateTester.VEL_ITERS, 
                            BMTemplateTester.POS_ITERS  )   
        self.clock.tick(60)
             

    def drawSim(self):

        self.screen.fill((255, 255, 255))                

        # Iterate through objects and draw them:                
        # Agent:        
        self.drawShape(self.template.agent, BMTemplateTester.RENDER_COLS['agent'])

        # Dynamic Blues:
        dynamicBlueCol = BMTemplateTester.RENDER_COLS['dynamicBlue']                
        for b in self.template.dynamicBlues:            
            self.drawShape(b, dynamicBlueCol)

        # Dynamic Reds:        
        dynamicRedCol = BMTemplateTester.RENDER_COLS['dynamicRed']
        for b in self.template.dynamicReds:            
            self.drawShape(b, dynamicRedCol) 

        # Statics:
        staticCol = BMTemplateTester.RENDER_COLS['static']
        for b in self.template.statics:            
            self.drawShape(b, staticCol)                                                     
                    
        pygame.display.update()
    

    # Rendering Backend
    # Draw a body's shape:
    def drawShape(self, b: b2Body, col):
        for f in b.fixtures: 
            shp = f.shape
            if shp.type == b2Shape.e_circle:   
                pos = BMTemplateTester.verToScr([b.GetWorldPoint(shp.pos)])[0]                                                                 
                pygame.gfxdraw.filled_circle(   self.screen,
                                                int(pos[0]),
                                                int(pos[1]),
                                                int(shp.radius * BMTemplateTester.SCR_ZOOM),  
                                                col   ) 
                pygame.gfxdraw.aacircle(    self.screen,
                                            int(pos[0]),
                                            int(pos[1]),
                                            int(shp.radius * BMTemplateTester.SCR_ZOOM),
                                            col  )                             
            elif shp.type == b2Shape.e_polygon:                        
                pygame.gfxdraw.aapolygon(   self.screen,
                                            BMTemplateTester.verToScr([b.GetWorldPoint(v) for v in shp.vertices]),
                                            col   )
                pygame.gfxdraw.filled_polygon(  self.screen,
                                                BMTemplateTester.verToScr([b.GetWorldPoint(v) for v in shp.vertices]),
                                                col   )  


    
    # Convert vertex coords in world to screen coords:
    def verToScr(vertices):
        return [    (   +(BMTemplateTester.SCR_ZOOM * (v[0] - BMTemplateTester.SCR_OFFSETX)) + (BMTemplateTester.SCR_WIDTH / 2), 
                        -(BMTemplateTester.SCR_ZOOM * (v[1] - BMTemplateTester.SCR_OFFSETY)) + (BMTemplateTester.SCR_HEIGHT / 2)    )
                    for v in vertices  ]        
    

if __name__ == "__main__":
    templateTest = BMTemplateTester(Seesaw()) # Choose Template to test here:
    templateTest.run()
