# Abstract class stuff:

from abc import ABC, abstractmethod
from typing import List

# Box2D stuff:
from Box2D.Box2D import *

from BMTask import State


class Template(ABC):
    """ Defines a physically dynamic benchmark template which
        serves as a basis for custom template creation.
        Walls enclose an explorable area between (-10, 0) to (10, 40)
        The agent is positioned at (0, 3) in default
    """

    # The origin coords inner x of the scenario, at left side of the scenario.
    SCENARIO_ORIGIN_X = -10
    # The origin coords inner y of the scenario, at bottom side of the scenario.
    SCENARIO_ORIGIN_Y = 0
    # The inner width of the scenario
    SCENARIO_WIDTH = 20
    # The inner height of the scenario
    SCENARIO_HEIGHT = 40
    # The thickness of the boundary wall
    BOUNDARY_THICKNESS = 1
    # The global physical properties of all movable objects
    OBJECT_DENSITY = 0.3
    OBJECT_FRICTION = 0.5
    OBJECT_RESTITUTION = 0.3
    # The properties of the agent
    AGENT_INIT_X = 0
    AGENT_INIT_Y = 1
    AGENT_RADIUS = 0.5
    AGENT_DENSITY = 3.0
    AGENT_FRICTION = 0.5
    AGENT_RESTITUTION = 0.3

    def __init__(self):
        # Scenario property; copy from the constant class field, but subclass should not change those values
        self.origin_x = Template.SCENARIO_ORIGIN_X
        self.origin_y = Template.SCENARIO_ORIGIN_Y
        self.width = Template.SCENARIO_WIDTH
        self.height = Template.SCENARIO_HEIGHT
        self.thickness = Template.BOUNDARY_THICKNESS
        # The global physical properties of all movable objects; copy from the constant class field
        self.object_density = Template.OBJECT_DENSITY
        self.object_friction = Template.OBJECT_FRICTION
        self.object_restitution = Template.OBJECT_RESTITUTION
        # agent property
        self.agent_x = Template.AGENT_INIT_X
        self.agent_y = Template.AGENT_INIT_Y
        self.agent_radius = Template.AGENT_RADIUS
        self.agent_density = Template.AGENT_DENSITY
        self.agent_friction = Template.AGENT_FRICTION
        self.agent_restitution = Template.AGENT_RESTITUTION

    def create_world(self, variant: float = 0.0, debug: bool = False) -> State:
        """
        Create a new BMTask from the template with given variant number (optional) between [0.0, 1.0].
        Different variant number can be used to specify configuration of the objects in a task.
        If variant number is not specified, it will use 0.0.
        """
        if debug:
            print('Generating task from template', self.template_name(), 'with variant', variant)
        # generate task agent
        agent = self.generate_agent(variant)
        # generate target static object (top wall)
        target_object = self.generate_target_object(variant)
        # generate walls & other static objects
        static_objects = self.generate_walls(variant)
        static_objects.extend(self.generate_static_objects(variant))
        # generate safe objects (in blue)
        safe_objects = self.generate_safe_objects(variant)
        # generate danger objects (in red)
        danger_objects = self.generate_danger_objects(variant)
        return State(agent, target_object, static_objects, safe_objects, danger_objects)

    def generate_agent(self, variant: float) -> b2BodyDef:
        """Generate the definition of the agent for a new task"""
        return b2BodyDef(position=(self.agent_x, self.agent_y),
                         fixtures=b2FixtureDef(shape=b2CircleShape(radius=self.agent_radius),
                                               density=self.agent_density,
                                               friction=self.agent_friction,
                                               restitution=self.agent_restitution),
                         linearVelocity=(0, 0),
                         type=b2_dynamicBody)

    def generate_target_object(self, variant: float) -> b2BodyDef:
        """Generate the target object in the environment (usually the wall at the top)"""
        return b2BodyDef(position=(self.origin_x + self.width / 2,
                                   self.origin_y + self.height + self.thickness / 2),
                         shapes=b2PolygonShape(box=(self.width / 2, self.thickness / 2)),
                         type=b2_staticBody)

    def generate_walls(self, variant: float) -> List[b2BodyDef]:
        """
        Generate the definition of the walls for a new task.
        Avoid to overwrite this method because we want to have the same boundary between different template & tasks.
        Excluded top wall here because it is the target object.
        """
        horizontal_wall = b2PolygonShape(box=(self.width / 2, self.thickness / 2))
        vertical_wall = b2PolygonShape(box=(self.thickness / 2, self.height / 2 + self.thickness))
        # World is enclosed into a (-10, 0) to (10, 40) box bounded by these walls:
        return [b2BodyDef(position=(self.origin_x + self.width / 2,
                                    self.origin_y - self.thickness / 2),
                          shapes=horizontal_wall,
                          type=b2_staticBody),
                b2BodyDef(position=(self.origin_x - self.thickness / 2,
                                    self.origin_y + self.height / 2),
                          shapes=vertical_wall,
                          type=b2_staticBody),
                b2BodyDef(position=(self.origin_x + self.width + self.thickness / 2,
                                    self.origin_y + self.height / 2),
                          shapes=vertical_wall,
                          type=b2_staticBody)
                ]

    # Each template will override and add its own
    # following abstract methods to generate objects in a new task.

    @abstractmethod
    def template_name(self) -> str:
        """Get name of the template, should be a constant. Do not contain space in the name! """
        pass

    @abstractmethod
    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:
        """Generate a list of static objects for a new task"""
        pass

    @abstractmethod
    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:
        """Generate a list of dynamic safe objects (in blue) for a new task"""
        pass

    @abstractmethod
    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:
        """Generate a list of dynamic danger objects (in red) for a new task"""
        pass
