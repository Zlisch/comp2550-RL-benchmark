import os

import pygame
from PIL import Image


class ImageSaver:
    """
    Customizable image renderer. Can be used to set up render frame rates, object 
    opacities, and cropped frames. You should use and expand this class to help 
    with producing good visualizations.
    """

    def __init__(self):
        self.image_render = False
        self.render_path = '../../assets/images/rendered/'
        self.image_count = 0
        self.render_fps = 10
        self.fps_helper_count = 0

    def init(self, image_render: bool, render_path: str, template_name: str, render_fps: int = 10):
        """
        If using image renderer, set up output path and create target folder. 
        If not, do nothing.
        """
        self.image_render = image_render
        self.render_path = render_path
        self.render_fps = render_fps
        # if using image renderer, create output folder of current template
        if self.image_render:
            self.render_path += template_name + "/"
            if not os.path.exists(self.render_path):
                os.makedirs(self.render_path)

    def render(self, screen: pygame.Surface):
        """
        Render the whole raw screen as specified in BMApplication module. FPS 
        as world FPS.
        """
        # fixme this function seems never used yet
        if self.image_render:
            pygame.image.save(screen, self.render_path + str(self.image_count) + ".jpg")
            self.image_count += 1

    def save(self, screen: pygame.Surface, world_fps: int):
        """
        Render the current state, without reward text information. Customized FPS.
        """
        if self.image_render:
            # world_fps should >= render fps
            if world_fps < self.render_fps:
                self.render_fps = world_fps
            step = int(world_fps / self.render_fps)
            if self.fps_helper_count % step == 0:
                pygame.image.save(screen, self.render_path + str(self.image_count) + ".jpg")
                raw = Image.open(self.render_path + str(self.image_count) + ".jpg")
                cropped = raw.crop((250, 30, 550, 570))
                cropped.save(self.render_path + str(self.image_count) + ".jpg")
                self.image_count += 1
            # update fps helper counter per world frame
            self.fps_helper_count += 1
