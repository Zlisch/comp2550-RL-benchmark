# Template stuff:
from typing import List

from BMTemplate import Template

# Box2D stuff:
from Box2D import *


# The Blank Template
class Blank(Template):
    """The Blank Template contain nothing. """
    def template_name(self) -> str:
        return 'Blank'

    def generate_static_objects(self, variant: float) -> List[b2BodyDef]:                
        return []

    def generate_safe_objects(self, variant: float) -> List[b2BodyDef]:                
        return []

    def generate_danger_objects(self, variant: float) -> List[b2BodyDef]:                
        return []
