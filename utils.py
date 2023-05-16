import pygame, os
from settings import *

def rotate_around_center(surf, angle):
    rotated_image = pygame.transform.rotate(surf, -angle)
    new_rect = rotated_image.get_rect(center=surf.get_rect().center)

    return rotated_image, new_rect

def rotate_around_center_mask(surf, angle):
    rotated_image = pygame.transform.rotate(surf, -angle)
    new_rect = rotated_image.get_rect(center=surf.get_rect().center)

    return rotated_image, new_rect, pygame.mask.from_surface(rotated_image)

def scale_image(image, scale):
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))

def get_image_path(filename):
    return os.path.join(PATHIMG, filename)
