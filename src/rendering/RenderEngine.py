from typing import List, Tuple

import pygame
import pygame.gfxdraw
from Box2D import b2Body, b2Shape
from pygame.surface import Surface

from BMTask import State

# Scaling Parameters
OFFSET_X = 0
OFFSET_Y = 20
ZOOM = 12
# Rendering Colours:
BACKGROUND_COLOR = (255, 255, 255)
AGENT_COLOR = (80, 180, 20)
TARGET_OBJECT_COLOR = (40, 40, 40)  # currently target object (top wall) share same color as other walls
STATIC_OBJECT_COLOR = (40, 40, 40)
SAFE_OBJECT_COLOR = (20, 20, 180)
DANGER_OBJECT_COLOR = (180, 20, 20)


def render_state(canvas: Surface, state: State):
    """
    Render all elements in the state into the canvas
    """
    canvas.fill(BACKGROUND_COLOR)
    # Iterate through objects and draw them:
    # Agent:
    render_shape(canvas, state.agent, AGENT_COLOR)
    # Target Object:
    render_shape(canvas, state.target_object, TARGET_OBJECT_COLOR)
    # Dynamic Blues:
    for shape in state.safe_objects:
        render_shape(canvas, shape, SAFE_OBJECT_COLOR)
    # Dynamic Reds:
    for shape in state.danger_objects:
        render_shape(canvas, shape, DANGER_OBJECT_COLOR)
    # Statics:
    for shape in state.static_objects:
        render_shape(canvas, shape, STATIC_OBJECT_COLOR)


# Draw a body's shape:
def render_shape(canvas: Surface, shape: b2Body, color: Tuple[int, int, int]):
    """ Render given shape into the screen """
    width = canvas.get_width()
    height = canvas.get_height()
    for fixture in shape.fixtures:
        s = fixture.shape
        if s.type == b2Shape.e_circle:
            pos = vertices2coords([shape.GetWorldPoint(s.pos)], width, height)[0]
            pygame.gfxdraw.filled_circle(canvas,
                                         int(pos[0]),
                                         int(pos[1]),
                                         int(s.radius * ZOOM),
                                         color)
            pygame.gfxdraw.aacircle(canvas,
                                    int(pos[0]),
                                    int(pos[1]),
                                    int(s.radius * ZOOM),
                                    color)
        elif s.type == b2Shape.e_polygon:
            vertices = [shape.GetWorldPoint(v) for v in s.vertices]
            coords = vertices2coords(vertices, width, height)
            pygame.gfxdraw.aapolygon(canvas, coords, color)
            pygame.gfxdraw.filled_polygon(canvas, coords, color)


def vertices2coords(vertices: List[Tuple[float, float]],
                    width: float,
                    height: float) -> List[Tuple[float, float]]:
    return custom_vertices2coords(vertices, ZOOM, OFFSET_X, OFFSET_Y, width, height)


def custom_vertices2coords(vertices: List[Tuple[float, float]],
                           zoom: float,
                           offset_x: float,
                           offset_y: float,
                           width: float,
                           height: float) -> List[Tuple[float, float]]:
    """Convert vertex coords in world to screen coords"""
    return [(+(zoom * (v[0] - offset_x)) + (width / 2), -(zoom * (v[1] - offset_y)) + (height / 2)) for v in vertices]
