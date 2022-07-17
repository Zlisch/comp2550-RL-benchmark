import pygame
from numpy import ndarray
from tf_agents.specs import array_spec

from BMTask import State
from observations.Observations import Observation
from rendering import RenderEngine
import numpy as np


class ImageObservation(Observation):

    def __init__(self,
                 frames: int,
                 raw_width: int,
                 raw_height: int,
                 image_width: int,
                 image_height: int):
        self.frames = frames
        self.raw_width = raw_width
        self.raw_height = raw_height
        self.image_width = image_width
        self.image_height = image_height
        # init cache
        self.cache = np.zeros((self.frames, self.image_width * self.image_height), dtype=np.float32)
        self.is_clean = True

    def reset(self):
        self.cache = np.zeros((self.frames, self.image_width * self.image_height), dtype=np.float32)
        self.is_clean = True

    def observation_spec(self):
        size = self.frames * self.image_width * self.image_height
        return array_spec.BoundedArraySpec(shape=(size,), dtype=np.float32,
                                           minimum=0.0, maximum=1.0, name='observation')

    def compute_observation(self, state: State) -> ndarray:
        canvas = pygame.Surface((self.raw_width, self.raw_height))
        RenderEngine.render_state(canvas, state)
        scaled_canvas = pygame.transform.scale(canvas, (self.image_width, self.image_height))
        current_frame = pygame.surfarray.array2d(scaled_canvas).flatten()
        normalized_frame = np.vectorize(lambda x: x / 16777215.0)(current_frame)
        if self.is_clean:
            for i in range(0, len(self.cache)):
                self.cache[i] = normalized_frame
            self.is_clean = False
        else:
            for i in range(len(self.cache) - 1, 0, -1):
                self.cache[i] = self.cache[i - 1]
            self.cache[0] = normalized_frame
        return self.cache.flatten()

    def render_observation(self, state: State, surf: pygame.Surface):
        pass

