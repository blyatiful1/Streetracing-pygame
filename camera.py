from utils import *
from settings import *
from track import Track
import pygame

class CameraGroup(pygame.sprite.Group):
    def __init__(self, car, track):
        super().__init__()
        self.display = pygame.display.get_surface()

        self.car = car

        self.offset = pygame.math.Vector2(0, 0)

        self.half_width = self.display.get_width() / 2
        self.half_height = self.display.get_height() / 2

        self.track = track
        self.track_rect = track.get_rect()

    def custom_draw(self):
        self.center_target(self.car)

        self.display.blit(self.track.surface, self.offset)
        
        for sprite in self.sprites():
            sprite.draw(self.display, self.offset)

        self.car.draw(self.display, self.offset)

    def center_target(self, target):
        self.offset.x = self.half_width - target.rect.centerx
        self.offset.y = self.half_height - target.rect.centery

        self.offset.x = min(0, self.offset.x)
        self.offset.y = min(0, self.offset.y)

        self.offset.x = max(-(self.track_rect.width - self.display.get_width()), self.offset.x)
        self.offset.y = max(-(self.track_rect.height - self.display.get_height()), self.offset.y)

    def temp_draw(self):
        pygame.draw.rect(self.display, red, self.track.finish_rect.move(self.offset.x, self.offset.y))

        pygame.draw.rect(self.display, green, self.track.start_rect.move(self.offset.x, self.offset.y))

        self.track.draw_border(self.display, self.offset)

        self.car.draw_debug(self.display, self.offset)     
        